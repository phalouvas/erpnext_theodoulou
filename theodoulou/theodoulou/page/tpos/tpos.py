# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from typing import TYPE_CHECKING

import frappe

from frappe.utils import cint
from frappe.utils.nestedset import get_root_of

from frappe.utils.background_jobs import get_queues

from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability

from erpnext.selling.page.point_of_sale.point_of_sale import search_by_term
from erpnext.selling.page.point_of_sale.point_of_sale import get_conditions
from erpnext.selling.page.point_of_sale.point_of_sale import get_root_of
from erpnext.selling.page.point_of_sale.point_of_sale import get_item_group_condition

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

def get_item_alternative(item_code, warehouse, price_list):
	item_alernatives = frappe.db.get_list('Item Alternative',
		filters={
			'item_code': item_code
		},
		fields=['alternative_item_code'],
		as_list=True
	)

	item_alernatives = item_alernatives + frappe.db.get_list('Item Alternative',
		filters={
			'alternative_item_code': item_code,
			'two_way': 1
		},
		fields=['item_code'],
		as_list=True
	)

	item_alternatives = list(set(item_alernatives))

	items = []
	for item_alternative in item_alternatives:
		item_doc = frappe.get_doc("Item", item_alternative[0])
		if not item_doc:
			continue
		item = {
			"description": item_doc.description,
			"is_stock_item": item_doc.is_stock_item,
			"item_code": item_doc.name,
			"item_image": item_doc.image,
			"item_name": item_doc.item_name,
			"stock_uom": item_doc.stock_uom,
			"uom": item_doc.stock_uom,
		}
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
		items.append(item)

	return items

@frappe.whitelist()
def get_items(start, page_length, price_list, item_group, pos_profile, search_term=""):
	warehouse, hide_unavailable_items = frappe.db.get_value(
		"POS Profile", pos_profile, ["warehouse", "hide_unavailable_items"]
	)

	result = []
	
	search_result = []
	if search_term:
		search_result = search_by_term(search_term.strip(), warehouse, price_list) or []
		if search_result:
			for item in search_result['items']:
				result.append(item)

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

	# I want to do run below code if the items_data is having only one item and the search_term is not empty
	if len(items_data) == 1:
		if search_term:
			item_alternatives = get_item_alternative(item_code, warehouse, price_list)
			for item_alternative in item_alternatives:
				result.append(item_alternative)
    
	return {"items": result}
