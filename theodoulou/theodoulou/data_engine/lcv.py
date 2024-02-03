import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

class LcvQuery(TheodoulouQuery):

    def __init__(self):
        self.title = frappe._('Long Commercial Vehicles')
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('lcv_brands')
        if data is None:
            data = frappe.db.sql(f"""
                SELECT DISTINCT 
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `100` AS T100
                    JOIN `110` AS T110 ON T100.HerNr = T110.HerNr
                    JOIN `120` AS T120 ON T110.KMODNR = T120.KMODNR
                WHERE T110.Transporter = 1
                    AND T120.MOTART <> '040'
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('lcv_brands', data)

        return data