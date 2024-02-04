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
    context.KTypNo = frappe.request.args.get('KTypNo')

    vehicle = query_engine.get_vehicle(context.BrandClass, context.KTypNo)
    
    context.vehicle = vehicle[0]
    context.vehicle['From Year'] = query_engine.convert_yyyymm(context.vehicle['From Year'])
    context.vehicle['To Year'] = query_engine.convert_yyyymm(context.vehicle['To Year'])

    context.categories_tree = query_engine.get_categories_tree()

    context.no_cache = 0
    context.title = f"{ context.vehicle.Manufacturer } { context.vehicle.Model } { context.vehicle.Type }"
    context.parents = [
        {"name": _("Home"), "route": "/"}, 
        {"name": query_engine.title, "route": f"/brands?BrandClass={query_controller.BrandClass}"},
        {"name": _("Models"), "route": f"/brands/models?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&needyear={context.needyear}"}, 
        {"name": _("Types"), "route": f"/brands/models/types?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&KModNo={context.KModNo}&needyear={context.needyear}"}, 
    ]

    