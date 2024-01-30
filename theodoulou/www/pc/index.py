import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Passenger Cars')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]

    query_engine = TheodoulouQuery()

    if 'show_all' in frappe.request.args:
        context.brands = query_engine.get_brands('PKW')
    else:
        popular_brands = [2, 5, 16, 20, 21, 24, 25, 35, 36, 45, 183, 54, 56, 
                        882, 184, 63, 72, 74, 1523, 77, 80, 84, 88, 92, 93, 95, 1820,
                        99, 104, 106, 1138, 107, 109, 111, 120, 121]
        context.brands = query_engine.get_popular_brands('PKW', popular_brands)