import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Brands')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]