import frappe
from frappe import _

def get_context(context):
    context.no_cache = 1
    context.title = _('Brands')
    context.parents = [{"name": frappe._("Home"), "route": "/"}]