import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):

    # Get the cookie value.
    vehicleActiveSelectionName = frappe.request.cookies.get('vehicleActiveSelectionName')

    # If the cookie is empty, throw an exception
    if not vehicleActiveSelectionName:
        frappe.throw(_("Please select a vehicle first."))
    
    product_id = frappe.request.args.get('product_id')

    query_engine = TheodoulouQuery()
    context.product_analogs = query_engine.get_product_analogs(product_id)

    context.no_cache = 0
    context.title = f"Searching for {product_id}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
    ]