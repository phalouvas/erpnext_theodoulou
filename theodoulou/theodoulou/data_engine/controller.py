import frappe
from theodoulou.theodoulou.data_engine.motorcycle import MotorcycleQuery
from theodoulou.theodoulou.data_engine.lcv import LcvQuery

class TheodoulouController:
    def __init__(self):
        pass

    def get_engine(self):
        vehicle_class = frappe.request.args.get('vehicle_class') or "PC"

        if vehicle_class == 'motorcycle':
            return MotorcycleQuery()
        
        if vehicle_class == 'lcv':
            return LcvQuery()