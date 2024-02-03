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
        self.vehicle_class = frappe.request.args.get('self.vehicle_class') or "pc"
        super().__init__()


    def get_engine(self):

        if self.vehicle_class == 'motorcycle':
            return MotorcycleQuery()
        
        if self.vehicle_class == 'lcv':
            return LcvQuery()
        
        if self.vehicle_class == 'emotorcycle':
            return eMotorcycleQuery()
        
        if self.vehicle_class == 'elcv':
            return eLcvQuery()
        
        if self.vehicle_class == 'epc':
            return ePcQuery()
        
        if self.vehicle_class == 'bus':
            return BusQuery()
        
        if self.vehicle_class == 'ebus':
            return eBusQuery()
        
        if self.vehicle_class == 'tractor':
            return TractorQuery()
        
        if self.vehicle_class == 'cv':
            return CvQuery()
        
        return PcQuery()
        