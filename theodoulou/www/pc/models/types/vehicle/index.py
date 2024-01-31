import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    vehicle_id = frappe.request.args.get('vehicle_id')
    brand_id = frappe.request.args.get('brand_id')
    needyear = frappe.request.args.get('needyear')
    model_id = frappe.request.args.get('model_id')

    query_engine = TheodoulouQuery()
    vehicle = query_engine.get_vehicle_passenger(vehicle_id)
    
    context.vehicle = vehicle[0]
    context.vehicle.FROM_YEAR = query_engine.convert_yyyymm(context.vehicle.FROM_YEAR)
    context.vehicle.TO_YEAR = query_engine.convert_yyyymm(context.vehicle.TO_YEAR)

    context.categories_tree = query_engine.get_vehicle_categories_tree("PKW", vehicle_id)

    context.no_cache = 0
    context.title = f"{ context.vehicle.MANUFACTURER } { context.vehicle.MODEL } { context.vehicle.TYPE }"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Models"), "route": f"/pc/models?brand_id={brand_id}&model_id={model_id}&needyear={needyear}"}, 
        {"name": frappe._("Types"), "route": f"/pc/models/types?brand_id={brand_id}&model_id={model_id}&needyear={needyear}"}, 
    ]

    