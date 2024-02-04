import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    vehicle_id = frappe.request.args.get('vehicle_id')

    query_engine = TheodoulouQuery()
    context.vehicles = query_engine.search_vehicles_engines(vehicle_id)

    context.no_cache = 0
    context.title = f"Searching for {vehicle_id}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
    ]