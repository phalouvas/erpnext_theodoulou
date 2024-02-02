import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Brands')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]

    query_engine = TheodoulouQuery()
    context.passenger_cars = query_engine.get_brands('PKW')
    context.commercial_cars = query_engine.get_brands('NKW')
