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

    brands = query_engine.get_brands()
    if 'show_all' in frappe.request.args:
        context.brands = brands
    else:
        popular_brands = [2, 5, 16, 20, 21, 24, 25, 35, 36, 45, 183, 54, 56, 882, 184, 63, 72, 74, 1523,
                                77, 80, 84, 88, 92, 93, 95, 1820, 99, 104, 106, 1138, 107, 109, 111, 120, 121,
                                4055, 1131, 2760, 181, 1021, 2554, 185, 138, 4330, 2524, 2559, 4056]
        context.brands = [brand for brand in brands if brand['HERNR'] in popular_brands]
    