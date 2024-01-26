import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Vehicle')
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
    ]

    query_engine = TheodoulouQuery()
    # get type and KMODNR from query string
    context.type = frappe.request.args.get('type')
    context.vehicle_id = frappe.request.args.get('ID')
    # get vehicle
    if context.type == "PKW":
        vehicle = query_engine.get_vehicle_passenger(context.vehicle_id)
    else:
        vehicle = query_engine.get_vehicle_commercial(context.vehicle_id)
    
    context.vehicle = vehicle[0]
    context.vehicle.FROM_YEAR = query_engine.convert_yyyymm(context.vehicle.FROM_YEAR)
    context.vehicle.TO_YEAR = query_engine.convert_yyyymm(context.vehicle.TO_YEAR)

    context.categories_tree = query_engine.get_vehicle_categories(context.type, context.vehicle_id)
    