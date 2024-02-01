import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery
import math

def get_context(context):

    # Get the cookie value.
    vehicleActiveSelectionName = frappe.request.cookies.get('vehicleActiveSelectionName')

    # If the cookie is empty, throw an exception
    if not vehicleActiveSelectionName:
        frappe.throw(_("Please select a vehicle first."))
    
    vehicle_id = frappe.request.args.get('vehicle_id') or frappe.request.cookies.get('vehicle_id')
    brand_id = frappe.request.args.get('brand_id') or frappe.request.cookies.get('brand_id')
    needyear = frappe.request.args.get('needyear') or frappe.request.cookies.get('needyear')
    model_id = frappe.request.args.get('model_id') or frappe.request.cookies.get('model_id')
    context.node_id = frappe.request.args.get('node_id') or frappe.request.cookies.get('node_id')
    manufacturer_id = frappe.request.args.get('manufacturer_id')
    product_id = frappe.request.args.get('product_id')

    query_engine = TheodoulouQuery()
    context.product_main_info = query_engine.get_product_main_info(manufacturer_id, product_id)
    context.product_criteria = query_engine.get_product_criteria(manufacturer_id, product_id)
    context.product_additional_info = query_engine.get_product_additional_info(manufacturer_id, product_id)
    context.product_cross_reference = query_engine.get_product_cross_reference(manufacturer_id, product_id)
    context.product_vehicles_applicability = query_engine.get_product_vehicles_applicability(manufacturer_id, product_id)
    context.product_media = query_engine.get_product_media(manufacturer_id, product_id)
    context.manufacturer_logo = query_engine.get_manufacturer_logo(manufacturer_id)

    context.categories_tree = query_engine.get_categories_tree("PKW")

    context.no_cache = 0
    context.title = f"{context.product_main_info.MARKE} - {context.product_main_info.ARTNR}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Vehicle"), "route": f"/pc/models/types/vehicle?brand_id={brand_id}&model_id={model_id}&needyear={needyear}&vehicle_id={vehicle_id}"}, 
    ]