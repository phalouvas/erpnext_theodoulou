import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery
from theodoulou.theodoulou.data_engine.emotorcycle import eMotorcycleQuery
from theodoulou.theodoulou.data_engine.elcv import eLcvQuery

class ePcQuery(TheodoulouQuery):

    def __init__(self):
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('elcv_brands')
        if data is None:
            data = frappe.db.sql(f"""
                SELECT DISTINCT 
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `100` AS T100
                    JOIN `110` AS T110 ON T100.HerNr = T110.HerNr
                    JOIN `120` AS T120 ON T110.KMODNR = T120.KMODNR
                WHERE T120.MOTART = '040'
                    AND T120.KRSTOFFART = '11'
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('elcv_brands', data)

        if 'show_all' in frappe.request.args:
            pass
        else:
            popular_brands = [21, 35, 36, 183, 184, 74, 77, 80, 84, 88, 93, 111, 121]
            data = [brand for brand in data if brand['HERNR'] in popular_brands]

        emotorcycle_engine = eMotorcycleQuery()
        elcv_engine = eLcvQuery()
        emotorcycle_brands = emotorcycle_engine.get_brands()
        elcv_brands = elcv_engine.get_brands()
        
        return data