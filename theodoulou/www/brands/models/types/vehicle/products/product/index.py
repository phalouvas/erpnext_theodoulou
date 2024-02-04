import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.controller import TheodoulouController

def get_context(context):

    # Get the cookie value.
    vehicleActiveSelectionName = frappe.request.cookies.get('vehicleActiveSelectionName')

    # If the cookie is empty, throw an exception
    if not vehicleActiveSelectionName:
        frappe.throw(_("Please select a vehicle first."))

    query_controller = TheodoulouController()
    query_engine = query_controller.get_engine()
    
    context.BrandClass = query_controller.BrandClass
    context.ManNo = frappe.request.args.get('ManNo') or frappe.request.cookies.get('ManNo')
    context.KModNo = frappe.request.args.get('KModNo') or frappe.request.cookies.get('KModNo')
    context.needyear = frappe.request.args.get('needyear') or frappe.request.cookies.get('needyear')
    context.KTypNo = frappe.request.args.get('KTypNo') or frappe.request.cookies.get('KTypNo')
    context.node_id = frappe.request.args.get('node_id') or frappe.request.cookies.get('node_id')
    ArtNo = frappe.request.args.get('ArtNo')

    BrandNo = frappe.request.args.get('BrandNo') or query_engine.dlnr_from_artnr(ArtNo)
    context.product_main_info = query_engine.get_product_main_info(BrandNo, ArtNo)
    context.shopping_cart = query_engine.get_shopping_cart(context.product_main_info.ItemName)
    context.doc = {"offers": False}
    context.product_criteria = query_engine.get_product_criteria(BrandNo, ArtNo)
    context.product_additional_info = query_engine.get_product_additional_info(BrandNo, ArtNo)
    context.product_oe_numbers = query_engine.get_product_oe_numbers(BrandNo, ArtNo)
    context.product_vehicles_applicability = query_engine.get_product_vehicles_applicability(BrandNo, ArtNo)
    context.product_media = query_engine.get_product_media(BrandNo, ArtNo)
    context.manufacturer_logo = query_engine.get_manufacturer_logo(BrandNo)
    context.product_analogs = query_engine.get_product_analogs(ArtNo)

    context.categories_tree = query_engine.get_categories_tree()

    context.no_cache = 0
    context.title = f"{context.product_main_info.MARKE} - {context.product_main_info.ARTNR}"
    context.parents = [
        {"name": _("Home"), "route": "/"}, 
        {"name": query_engine.title, "route": f"/brands?BrandClass={query_controller.BrandClass}"},
        {"name": _("Models"), "route": f"/brands/models?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&needyear={context.needyear}"}, 
        {"name": _("Types"), "route": f"/brands/models/types?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&KModNo={context.KModNo}&needyear={context.needyear}"}, 
        {"name": _("Vehicle"), "route": f"/brands/models/types/vehicle?BrandClass={query_controller.BrandClass}&ManNo={context.ManNo}&KModNo={context.KModNo}&KTypNo={context.KTypNo}&needyear={context.needyear}"},
        {"name": _("Products"), "route": f"/brands/models/types/vehicle/products?node_id={context.product_main_info.node_id}"},
    ]