import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    query_engine = TheodoulouQuery()

    context.brand_id = frappe.request.args.get('brand_id')
    context.model_id = frappe.request.args.get('model_id')
    context.needyear = frappe.request.args.get('needyear')    

    context.types = query_engine.get_types_passenger_cars(context.model_id, context.needyear)
    
    for type in context.types:
        type.YEARS = f"{str(type.FROM_YEAR)[:4]} - {str(type.TO_YEAR)[:4]}"
    # context.types is not empty then get BRAND from first type
    if context.types:
        context.brand = context.types[0].MANUFACTURER
        context.model = context.types[0].MODEL

    context.categories_tree = query_engine.get_categories_tree('PKW')

    context.no_cache = 0
    context.title = f"{context.brand} {context.model}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": frappe._("Passenger Cars"), "route": "/pc"}, 
        {"name": frappe._("Models"), "route": f"/pc/models?brand_id={context.brand_id}&context.model_id={context.model_id}&needyear={context.needyear}"}, 
    ]
