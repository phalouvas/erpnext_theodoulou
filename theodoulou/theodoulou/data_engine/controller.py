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
        self.BrandClass = frappe.request.args.get('BrandClass') or "pc"
        super().__init__()


    def get_engine(self):

        if self.BrandClass == 'motorcycle':
            return MotorcycleQuery()
        
        if self.BrandClass == 'lcv':
            return LcvQuery()
        
        if self.BrandClass == 'emotorcycle':
            return eMotorcycleQuery()
        
        if self.BrandClass == 'elcv':
            return eLcvQuery()
        
        if self.BrandClass == 'epc':
            return ePcQuery()
        
        if self.BrandClass == 'bus':
            return BusQuery()
        
        if self.BrandClass == 'ebus':
            return eBusQuery()
        
        if self.BrandClass == 'tractor':
            return TractorQuery()
        
        if self.BrandClass == 'cv':
            return CvQuery()
        
        return PcQuery()
        