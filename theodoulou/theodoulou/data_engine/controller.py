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
        self.VehicleClass = frappe.request.args.get('self.VehicleClass') or "pc"
        super().__init__()


    def get_engine(self):

        if self.VehicleClass == 'motorcycle':
            return MotorcycleQuery()
        
        if self.VehicleClass == 'lcv':
            return LcvQuery()
        
        if self.VehicleClass == 'emotorcycle':
            return eMotorcycleQuery()
        
        if self.VehicleClass == 'elcv':
            return eLcvQuery()
        
        if self.VehicleClass == 'epc':
            return ePcQuery()
        
        if self.VehicleClass == 'bus':
            return BusQuery()
        
        if self.VehicleClass == 'ebus':
            return eBusQuery()
        
        if self.VehicleClass == 'tractor':
            return TractorQuery()
        
        if self.VehicleClass == 'cv':
            return CvQuery()
        
        return PcQuery()
        