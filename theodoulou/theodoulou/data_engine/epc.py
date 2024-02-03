import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

class ePcQuery(TheodoulouQuery):

    def __init__(self):
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('epc_brands')
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
                    AND T120.AUFBAUART <> '051'
                    AND T110.Transporter = '0'
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('epc_brands', data)

        if 'show_all' in frappe.request.args:
            popular_data = []
        else:
            popular_brands = [2, 5, 16, 20, 21, 24, 25, 35, 36, 45, 183, 54, 56, 
                        882, 184, 63, 72, 74, 1523, 77, 80, 84, 88, 92, 93, 95, 1820,
                        99, 104, 106, 1138, 107, 109, 111, 120, 121]
            popular_data = [brand for brand in data if brand['HERNR'] in popular_brands]
        
        return data, popular_data