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
    context.ID = frappe.request.args.get('ID')
    # get vehicle
    if context.type == "PKW":
        vehicle = query_engine.get_vehicle_passenger(context.ID)
    else:
        vehicle = query_engine.get_vehicle_commercial(context.ID)
    
    context.vehicle = vehicle[0]
    context.vehicle.FROM_YEAR = query_engine.convert_yyyymm(context.vehicle.FROM_YEAR)
    context.vehicle.TO_YEAR = query_engine.convert_yyyymm(context.vehicle.TO_YEAR)
    