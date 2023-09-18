# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from typing import TYPE_CHECKING

import frappe

from frappe.utils import cint
from frappe.utils.nestedset import get_root_of

from frappe.utils import convert_utc_to_user_timezone
from frappe.utils.background_jobs import get_queues, get_workers
from frappe.utils.scheduler import is_scheduler_inactive

from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability
from erpnext.accounts.doctype.pos_profile.pos_profile import get_child_nodes, get_item_groups
from erpnext.stock.utils import scan_barcode

from erpnext.selling.page.point_of_sale.point_of_sale import search_for_serial_or_batch_or_barcode_number
from erpnext.selling.page.point_of_sale.point_of_sale import get_conditions
from erpnext.selling.page.point_of_sale.point_of_sale import get_root_of
from erpnext.selling.page.point_of_sale.point_of_sale import get_item_group_condition
from erpnext.selling.page.point_of_sale.point_of_sale import search_for_serial_or_batch_or_barcode_number
from erpnext.selling.page.point_of_sale.point_of_sale import search_for_serial_or_batch_or_barcode_number

if TYPE_CHECKING:
	from rq.job import Job

JOB_COLORS = {"queued": "orange", "failed": "red", "started": "blue", "finished": "green"}


@frappe.whitelist()
def get_info(pos_profile=None) -> list[dict]:
	entry_list = frappe.get_list("POS Opening Entry", filters={"docstatus": 1, "status": "Open", "pos_profile": pos_profile}, fields=["name", "status"])
	if entry_list:
		pos_opening_entry = frappe.get_doc("POS Opening Entry", entry_list[0].name)
		pos_invoice_list = frappe.get_list("POS Invoice")
		pos_invoice = frappe.get_doc("POS Invoice", pos_invoice_list[0].name)
	return entry_list


@frappe.whitelist()
def remove_failed_jobs():
	queues = get_queues()
	for queue in queues:
		fail_registry = queue.failed_job_registry
		for job_id in fail_registry.get_job_ids():
			job = queue.fetch_job(job_id)
			fail_registry.remove(job, delete_job=True)


@frappe.whitelist()
def get_pos_profiles():
	return frappe.get_list("POS Profile", filters={"Disabled": "No"}, fields=["name as label", "name as value"])

def search_by_term(search_term, warehouse, price_list):
	result = search_for_serial_or_batch_or_barcode_number(search_term) or {}
	item_code = result.get("item_code", search_term)
	serial_no = result.get("serial_no", "")
	batch_no = result.get("batch_no", "")
	barcode = result.get("barcode", "")
	if not result:
		return
	item_doc = frappe.get_doc("Item", item_code)
	if not item_doc:
		return
	item = {
		"barcode": barcode,
		"batch_no": batch_no,
		"description": item_doc.description,
		"is_stock_item": item_doc.is_stock_item,
		"item_code": item_doc.name,
		"item_image": item_doc.image,
		"item_name": item_doc.item_name,
		"serial_no": serial_no,
		"stock_uom": item_doc.stock_uom,
		"uom": item_doc.stock_uom,
	}
	if barcode:
		barcode_info = next(filter(lambda x: x.barcode == barcode, item_doc.get("barcodes", [])), None)
		if barcode_info and barcode_info.uom:
			uom = next(filter(lambda x: x.uom == barcode_info.uom, item_doc.uoms), {})
			item.update(
				{
					"uom": barcode_info.uom,
					"conversion_factor": uom.get("conversion_factor", 1),
				}
			)

	item_stock_qty, is_stock_item = get_stock_availability(item_code, warehouse)
	item_stock_qty = item_stock_qty // item.get("conversion_factor", 1)
	item.update({"actual_qty": item_stock_qty})

	price = frappe.get_list(
		doctype="Item Price",
		filters={
			"price_list": price_list,
			"item_code": item_code,
		},
		fields=["uom", "currency", "price_list_rate"],
	)

	def __sort(p):
		p_uom = p.get("uom")
		if p_uom == item.get("uom"):
			return 0
		elif p_uom == item.get("stock_uom"):
			return 1
		else:
			return 2

	# sort by fallback preference. always pick exact uom match if available
	price = sorted(price, key=__sort)
	if len(price) > 0:
		p = price.pop(0)
		item.update(
			{
				"currency": p.get("currency"),
				"price_list_rate": p.get("price_list_rate"),
			}
		)
	return {"items": [item]}

@frappe.whitelist()
def get_items(start, page_length, price_list, item_group, pos_profile, search_term=""):
	warehouse, hide_unavailable_items = frappe.db.get_value(
		"POS Profile", pos_profile, ["warehouse", "hide_unavailable_items"]
	)

	result = []

	if search_term:
		result = search_by_term(search_term, warehouse, price_list) or []
		if result:
			return result

	if not frappe.db.exists("Item Group", item_group):
		item_group = get_root_of("Item Group")

	condition = get_conditions(search_term)
	condition += get_item_group_condition(pos_profile)

	lft, rgt = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"])

	bin_join_selection, bin_join_condition = "", ""
	if hide_unavailable_items:
		bin_join_selection = ", `tabBin` bin"
		bin_join_condition = (
			"AND bin.warehouse = %(warehouse)s AND bin.item_code = item.name AND bin.actual_qty > 0"
		)

	items_data = frappe.db.sql(
		"""
		SELECT
			item.name AS item_code,
			item.item_name,
			item.description,
			item.stock_uom,
			item.image AS item_image,
			item.is_stock_item
		FROM
			`tabItem` item {bin_join_selection}
		WHERE
			item.disabled = 0
			AND item.has_variants = 0
			AND item.is_sales_item = 1
			AND item.is_fixed_asset = 0
			AND item.item_group in (SELECT name FROM `tabItem Group` WHERE lft >= {lft} AND rgt <= {rgt})
			AND {condition}
			{bin_join_condition}
		ORDER BY
			item.name asc
		LIMIT
			{page_length} offset {start}""".format(
			start=cint(start),
			page_length=cint(page_length),
			lft=cint(lft),
			rgt=cint(rgt),
			condition=condition,
			bin_join_selection=bin_join_selection,
			bin_join_condition=bin_join_condition,
		),
		{"warehouse": warehouse},
		as_dict=1,
	)

	if items_data:
		items = [d.item_code for d in items_data]
		item_prices_data = frappe.get_all(
			"Item Price",
			fields=["item_code", "price_list_rate", "currency"],
			filters={"price_list": price_list, "item_code": ["in", items]},
		)

		item_prices = {}
		for d in item_prices_data:
			item_prices[d.item_code] = d

		for item in items_data:
			item_code = item.item_code
			item_price = item_prices.get(item_code) or {}
			item_stock_qty, is_stock_item = get_stock_availability(item_code, warehouse)

			row = {}
			row.update(item)
			row.update(
				{
					"price_list_rate": item_price.get("price_list_rate"),
					"currency": item_price.get("currency"),
					"actual_qty": item_stock_qty,
				}
			)
			result.append(row)

	return {"items": result}
