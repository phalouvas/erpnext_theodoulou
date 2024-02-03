import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.controller import TheodoulouController

def get_context(context):    
    query_controller = TheodoulouController()
    query_engine = query_controller.get_engine()

    context.ManNo = frappe.request.args.get('ManNo')
    context.needyear = frappe.request.args.get('needyear') or '0'
    context.models = query_engine.get_models(context.ManNo, context.needyear)
    for model in context.models:
        model.FROM_YEAR = query_engine.convert_yyyymm(model.FROM_YEAR)
        model.TO_YEAR = query_engine.convert_yyyymm(model.TO_YEAR)
    # context.models is not empty then get BRAND from first model
    if context.models:
        context.title = context.models[0].MANUFACTURER

    # get years
    context.years = query_engine.get_years()

    context.categories_tree = query_engine.get_categories_tree('PKW')
    
    context.no_cache = 0
    context.parents = [{"name": _("Home"), "route": "/"}, {"name": query_engine.title, "route": "/brands?BrandClass=" + query_controller.BrandClass}]