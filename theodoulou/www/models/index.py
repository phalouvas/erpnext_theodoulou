import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Brands')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]

    query_engine = TheodoulouQuery()
    # get type and HERNR from query string
    type = frappe.request.args.get('type')
    HERNR = frappe.request.args.get('HERNR')
    NEEDYEAR = frappe.request.args.get('NEEDYEAR')    
    # get models
    context.models = query_engine.get_models(type, HERNR, NEEDYEAR)
    # context.models is not empty then get BRAND from first model
    if context.models:
        context.brand = context.models[0].MANUFACTURER
    