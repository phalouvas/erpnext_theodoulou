import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.controller import TheodoulouController
import math

def get_context(context):

    # Get the cookie value.
    vehicleActiveSelectionName = frappe.request.cookies.get('vehicleActiveSelectionName')

    # If the cookie is empty, throw an exception
    if not vehicleActiveSelectionName:
        frappe.throw(_("Please select a vehicle first."))

    query_controller = TheodoulouController()
    query_engine = query_controller.get_engine()

    context.BrandClass = query_controller.BrandClass
    context.ManNo = frappe.request.args.get('ManNo') or frappe.request.cookies.get('ManNo')
    context.KModNo = frappe.request.args.get('KModNo') or frappe.request.cookies.get('KModNo')
    context.needyear = frappe.request.args.get('needyear') or frappe.request.cookies.get('needyear')
    context.KTypNo = frappe.request.args.get('KTypNo') or frappe.request.cookies.get('KTypNo')
    context.node_id = frappe.request.args.get('node_id') or frappe.request.cookies.get('node_id')
    context.page = int(frappe.request.args.get('page') or 1)

    products = query_engine.get_products()
    context.products = products['products']
    context.total_products = products['total_products']
    context.last_page = math.ceil(context.total_products / 20)

    context.manufacturers = query_engine.get_products_manufacturers()
    context.categories_tree = query_engine.get_categories_tree()
    context.active_node = query_engine.get_node("PKW", context.node_id)

    context.no_cache = 0
    context.title = f"{context.active_node.NAME}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Vehicle"), "route": f"/pc/models/types/vehicle?brand_id={brand_id}&model_id={model_id}&needyear={needyear}&vehicle_id={vehicle_id}"}, 
    ]