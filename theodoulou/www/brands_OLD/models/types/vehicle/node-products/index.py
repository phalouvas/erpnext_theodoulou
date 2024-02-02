import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Products')
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
    ]

    query_engine = TheodoulouQuery()
    context.type = frappe.request.args.get('type')
    context.vehicle_id = frappe.request.args.get('vehicle_id')
    context.node_id = frappe.request.args.get('node_id')

    context.products = query_engine.get_vehicle_products(context.type, context.vehicle_id, context.node_id)