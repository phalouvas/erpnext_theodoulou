import frappe
from theodoulou.theodoulou.data_engine.motorcycles import MotorcyclesQuery

class TheodoulouController:
    def __init__(self):
        pass

    def get_engine(self):
        vehicle_class = frappe.request.args.get('vehicle_class') or "PC"

        if vehicle_class == 'Motorcycle':
            return MotorcyclesQuery()