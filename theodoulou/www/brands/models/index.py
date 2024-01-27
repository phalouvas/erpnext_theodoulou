import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Models')
    context.parents = [{"name": frappe._("Home"), "route": "/"}, {"name": frappe._("Brands"), "route": "/brands"}]

    query_engine = TheodoulouQuery()
    # get type and HERNR from query string
    context.vehicle_type = frappe.request.args.get('vehicle_type')
    # if vehicle_type is not in the query string, get it from the cookies
    if not context.vehicle_type:
        context.vehicle_type = frappe.request.cookies.get('vehicle_type')
    HERNR = frappe.request.args.get('HERNR')
    context.needyear = frappe.request.args.get('needyear')    
    # get models
    context.models = query_engine.get_models(context.vehicle_type, HERNR, context.needyear)    
    for model in context.models:
        model.FROM_YEAR = query_engine.convert_yyyymm(model.FROM_YEAR)
        model.TO_YEAR = query_engine.convert_yyyymm(model.TO_YEAR)
    # context.models is not empty then get BRAND from first model
    if context.models:
        context.brand = context.models[0].MANUFACTURER
    # get years
    context.years = query_engine.get_years()
    
    