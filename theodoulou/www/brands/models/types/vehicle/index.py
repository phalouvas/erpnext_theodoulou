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
    context.vehicle_type = frappe.request.args.get('vehicle_type')
    context.vehicle_id = frappe.request.args.get('vehicle_id')
    context.HERNR = frappe.request.args.get('HERNR')
    context.needyear = frappe.request.args.get('needyear')
    context.KMODNR = frappe.request.args.get('KMODNR')

    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Brands"), "route": "/brands"}, 
        {"name": frappe._("Models"), "route": f"/brands/models?vehicle_type={context.vehicle_type}&HERNR={context.HERNR}&needyear={context.needyear}"}, 
        {"name": frappe._("Types"), "route": f"/brands/models/types?vehicle_type={context.vehicle_type}&HERNR={context.HERNR}&KMODNR={context.KMODNR}&needyear={context.needyear}"}, 
    ]

    # get vehicle
    if context.vehicle_type == "PKW":
        vehicle = query_engine.get_vehicle_passenger(context.vehicle_id)
    else:
        vehicle = query_engine.get_vehicle_commercial(context.vehicle_id)
    
    context.vehicle = vehicle[0]
    context.vehicle.FROM_YEAR = query_engine.convert_yyyymm(context.vehicle.FROM_YEAR)
    context.vehicle.TO_YEAR = query_engine.convert_yyyymm(context.vehicle.TO_YEAR)

    context.categories_tree = query_engine.get_product_categories(context.vehicle_type)
    