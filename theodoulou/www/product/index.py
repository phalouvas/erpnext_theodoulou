import frappe
from frappe import _
from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

def get_context(context):
    context.no_cache = 0
    context.title = _('Product')
    context.parents = [
        {"name": frappe._("Home"), "route": "/"}, 
    ]

    query_engine = TheodoulouQuery()
    context.dlnr = frappe.request.args.get('dlnr')
    context.artnr = frappe.request.args.get('artnr')

    context.product = query_engine.get_product(context.dlnr, context.artnr)