import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    query_engine = TheodoulouQuery()
    context.vehicle_id = frappe.request.args.get('vehicle_id')
    context.brand_id = frappe.request.args.get('brand_id')
    context.needyear = frappe.request.args.get('needyear')
    context.model_id = frappe.request.args.get('model_id')

    vehicle = query_engine.get_vehicle_passenger(context.vehicle_id)
    
    context.vehicle = vehicle[0]
    context.vehicle.FROM_YEAR = query_engine.convert_yyyymm(context.vehicle.FROM_YEAR)
    context.vehicle.TO_YEAR = query_engine.convert_yyyymm(context.vehicle.TO_YEAR)

    context.categories_tree = query_engine.get_categories_tree("PKW")

    context.no_cache = 0
    context.title = f"{ context.vehicle.MANUFACTURER } { context.vehicle.MODEL } { context.vehicle.TYPE }"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Models"), "route": f"/pc/models?brand_id={context.brand_id}&context.model_id={context.model_id}&needyear={context.needyear}"}, 
        {"name": frappe._("Types"), "route": f"/pc/models/types?brand_id={context.brand_id}&model_id={context.model_id}&needyear={context.needyear}"}, 
    ]

    