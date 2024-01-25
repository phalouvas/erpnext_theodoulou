import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Models')
    context.parents = [{"name": frappe._("Home"), "route": "/"}, {"name": frappe._("Brands"), "route": "/brands"}]

    query_engine = TheodoulouQuery()
    # get type and HERNR from query string
    context.type = frappe.request.args.get('type')
    HERNR = frappe.request.args.get('HERNR')
    context.NEEDYEAR = frappe.request.args.get('NEEDYEAR')    
    # get models
    context.models = query_engine.get_models(context.type, HERNR, context.NEEDYEAR)    
    for model in context.models:
        model.YEARS = f"{str(model.FROM_YEAR)[:4]} - {str(model.TO_YEAR)[:4]}"
    # context.models is not empty then get BRAND from first model
    if context.models:
        context.brand = context.models[0].MANUFACTURER
    # get years
    context.years = query_engine.get_years()
    
    