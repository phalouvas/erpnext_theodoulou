import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    query_engine = TheodoulouQuery()
    context.vehicle_id = frappe.request.args.get('vehicle_id')
    context.needyear = frappe.request.args.get('needyear')
    # get models
    context.models = query_engine.get_models("PKW", context.vehicle_id, context.needyear)    
    for model in context.models:
        model.FROM_YEAR = query_engine.convert_yyyymm(model.FROM_YEAR)
        model.TO_YEAR = query_engine.convert_yyyymm(model.TO_YEAR)
    # context.models is not empty then get BRAND from first model
    if context.models:
        context.title = context.models[0].MANUFACTURER
    # get years
    context.years = query_engine.get_years()
    
    context.no_cache = 0
    context.parents = [{"name": frappe._("Home"), "route": "/"}, {"name": frappe._("Personal Cars"), "route": "/pc"}]
