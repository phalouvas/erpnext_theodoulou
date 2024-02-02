import frappe
from theodoulou.theodoulou.data_engine.motorcycles import MotorcyclesQuery

class TheodoulouController:
    def __init__(self):
        pass

    def get_engine(self):
        vehicle_type = frappe.request.args.get('vehicle_type') or 'PKW'
        vehicle_class = int(frappe.request.args.get('vehicle_class') or 2)
        
        if vehicle_type == 'PKW' and vehicle_class == 3:
            return MotorcyclesQuery()