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
        context.brands = brands[0]
    else:
        context.brands = brands[1]
    