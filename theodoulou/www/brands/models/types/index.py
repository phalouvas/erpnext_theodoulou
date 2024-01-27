import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Types')
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Brands"), "route": "/brands"}, 
    ]

    query_engine = TheodoulouQuery()
    # get type and KMODNR from query string
    context.vehicle_type = frappe.request.args.get('vehicle_type')
    context.KMODNR = frappe.request.args.get('KMODNR')
    context.NEEDYEAR = frappe.request.args.get('NEEDYEAR')
    # get types
    if context.vehicle_type == "PKW":
        context.types = query_engine.get_types_passenger_cars(context.KMODNR, context.NEEDYEAR)
    else:
        context.types = query_engine.get_types_commercial_cars(context.KMODNR, context.NEEDYEAR)
    
    for type in context.types:
        type.YEARS = f"{str(type.FROM_YEAR)[:4]} - {str(type.TO_YEAR)[:4]}"
    # context.types is not empty then get BRAND from first type
    if context.types:
        context.brand = context.types[0].MANUFACTURER
        context.model = context.types[0].MODEL
    # get years
    context.years = query_engine.get_years()
