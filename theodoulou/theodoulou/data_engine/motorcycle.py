import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

class MotorcycleQuery(TheodoulouQuery):

    def __init__(self):
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('motorcycles_brands')
        if data is None:
            data = frappe.db.sql(f"""
                SELECT DISTINCT 
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `100` AS T100
                    JOIN `110` AS T110 ON T100.HerNr = T110.HerNr
                    JOIN `120` AS T120 ON T110.KMODNR = T120.KMODNR
                WHERE T120.AUFBAUART = '051' AND T120.MOTART <> '040'
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('motorcycles_brands', data)

        if 'show_all' in frappe.request.args:
            return data
        else:
            popular_brands = [4330, 2524, 16, 2559, 4055, 45, 4056, 1131, 2760, 88, 181, 109, 1021]
            data = [brand for brand in data if brand['HERNR'] in popular_brands]
        
        return data