import frappe
from theodoulou.theodoulou.data_engine.motorcycle import MotorcycleQuery
from theodoulou.theodoulou.data_engine.lcv import LcvQuery
from theodoulou.theodoulou.data_engine.emotorcycle import eMotorcycleQuery
from theodoulou.theodoulou.data_engine.elcv import eLcvQuery
from theodoulou.theodoulou.data_engine.epc import ePcQuery
from theodoulou.theodoulou.data_engine.pc import PcQuery
from theodoulou.theodoulou.data_engine.bus import BusQuery
from theodoulou.theodoulou.data_engine.ebus import eBusQuery
from theodoulou.theodoulou.data_engine.tractor import TractorQuery
from theodoulou.theodoulou.data_engine.cv import CvQuery

class TheodoulouController:
    def __init__(self):
        pass

    def get_engine(self):
        vehicle_class = frappe.request.args.get('vehicle_class') or "PC"

        if vehicle_class == 'motorcycle':
            return MotorcycleQuery()
        
        if vehicle_class == 'lcv':
            return LcvQuery()
        
        if vehicle_class == 'emotorcycle':
            return eMotorcycleQuery()
        
        if vehicle_class == 'elcv':
            return eLcvQuery()
        
        if vehicle_class == 'epc':
            return ePcQuery()
        
        if vehicle_class == 'bus':
            return BusQuery()
        
        if vehicle_class == 'ebus':
            return eBusQuery()
        
        if vehicle_class == 'tractor':
            return TractorQuery()
        
        if vehicle_class == 'cv':
            return CvQuery()
        
        return PcQuery()
        