import frappe
import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.controller import TheodoulouController

def get_context(context):    
    query_controller = TheodoulouController()
    query_engine = query_controller.get_engine()

    context.BrandClass = query_controller.BrandClass
    context.ManNo = frappe.request.args.get('ManNo')
    context.KModNo = frappe.request.args.get('KModNo')
    context.needyear = frappe.request.args.get('needyear') or '0'

    context.types = query_engine.get_types(context.BrandClass, context.KModNo, context.needyear)
    
    for type in context.types:
        type.YEARS = f"{str(type.FROM_YEAR)[:4]} - {str(type.TO_YEAR)[:4]}"
    # context.types is not empty then get BRAND from first type
    if context.types:
        context.brand = context.types[0].MANUFACTURER
        context.model = context.types[0].MODEL

    context.categories_tree = query_engine.get_categories_tree()

    context.no_cache = 0
    context.title = f"{context.brand} {context.model}"
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
        {"name": query_engine.title, "route": f"/brands?BrandClass={query_controller.BrandClass}"},
        {"name": context.brand, "route": f"/brands/models?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&needyear={context.needyear}"}, 
    ]
