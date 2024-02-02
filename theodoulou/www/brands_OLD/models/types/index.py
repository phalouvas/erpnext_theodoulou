import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Types')    

    query_engine = TheodoulouQuery()
    # get type and KMODNR from query string
    context.vehicle_type = frappe.request.args.get('vehicle_type')
    context.HERNR = frappe.request.args.get('HERNR')
    context.KMODNR = frappe.request.args.get('KMODNR')
    context.needyear = frappe.request.args.get('needyear')

    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Brands"), "route": "/brands"}, 
        {"name": frappe._("Models"), "route": f"/brands/models?vehicle_type={context.vehicle_type}&HERNR={context.HERNR}&needyear={context.needyear}"}, 
    ]

    # get types
    if context.vehicle_type == "PKW":
        context.types = query_engine.get_types_passenger_cars(context.KMODNR, context.needyear)
    else:
        context.types = query_engine.get_types_commercial_cars(context.KMODNR, context.needyear)
    
    for type in context.types:
        type.YEARS = f"{str(type.FROM_YEAR)[:4]} - {str(type.TO_YEAR)[:4]}"
    # context.types is not empty then get BRAND from first type
    if context.types:
        context.brand = context.types[0].MANUFACTURER
        context.model = context.types[0].MODEL
    # get years
    context.years = query_engine.get_years()