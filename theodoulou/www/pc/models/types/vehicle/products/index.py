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
    context.page = int(frappe.request.args.get('page') or 1)

    query_engine = TheodoulouQuery()
    context.total_products = query_engine.get_vehicle_products_count("PKW", vehicle_id, context.node_id)
    context.last_page = math.ceil(context.total_products / 16)
    context.products = query_engine.get_vehicle_products("PKW", vehicle_id, context.node_id ,context.page)

    context.categories_tree = query_engine.get_categories_tree("PKW")
    context.active_node = query_engine.get_node("PKW", context.node_id)

    context.no_cache = 0
    context.title = f"{context.active_node.NAME}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Vehicle"), "route": f"/pc/models/types/vehicle?brand_id={brand_id}&model_id={model_id}&needyear={needyear}&vehicle_id={vehicle_id}"}, 
    ]