import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.controller import TheodoulouController

def get_context(context):
    context.no_cache = 0
    context.title = _('Motorcycles')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]

    query_controller = TheodoulouController()
    query_engine = query_controller.get_engine()
    context.categories_tree = query_engine.get_categories_tree('PKW')

    all_brands = query_engine.get_brands()
    if 'show_all' in frappe.request.args:
        context.brands = all_brands
    else:
        popular_brands = [4330, 2524, 16, 2559, 4055, 45, 4056, 1131, 2760, 88, 181, 109, 1021]
        context.brands = [brand for brand in all_brands if brand['HERNR'] in popular_brands]