import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

class MotorcycleQuery(TheodoulouQuery):

    def __init__(self):
        self.title = frappe._('Motorcycles')
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('motorcycle_brands')
        if data is None:
            data = self.frappe_db.sql(f"""
                SELECT DISTINCT 
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `100` AS T100
                    JOIN `110` AS T110 ON T100.HerNr = T110.HerNr
                    JOIN `120` AS T120 ON T110.KMODNR = T120.KMODNR
                WHERE T120.AUFBAUART = '051' 
                    AND T120.MOTART <> '040'
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('motorcycle_brands', data)

        return data
    
    def get_models(self, ManNo, NeedYear = 0):
            
            data = frappe.cache().get_value('motorcycle_models' + '_' + ManNo + '_' + NeedYear)

            if data is None:
                data = self.frappe_db.sql(f"""
                    SELECT DISTINCT
                        T110.KMODNR AS KModNo,  -- ID MODEL
                        GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                        GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                        T110.BJVON AS FROM_YEAR, -- MODEL PRODUCTING FROM YEAR+MONTH
                        IFNULL(T110.BJBIS, 'now') AS TO_YEAR -- MODEL PRODUCTING TO YEAR+MONTH
                    FROM `110` AS T110
                        JOIN `100` AS T100 ON T100.HerNr = T110.HerNr
                        JOIN `120` AS T120 ON T110.KMODNR = T120.KMODNR		
                    WHERE 1 
                        AND T120.AUFBAUART = '051' 
                        AND T120.MOTART <> '040'
                        AND T100.HERNR = { ManNo }
                        AND (CASE
                                WHEN { NeedYear } = 0 OR LENGTH({ NeedYear }) <> 4 THEN 1					
                                WHEN T110.BJVON <= CAST(CONCAT({ NeedYear },'01') AS UNSIGNED) AND IFNULL(T110.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({ NeedYear },'01') AS UNSIGNED) THEN 1
                                ELSE 0
                            END) = 1
                    ORDER BY T110.SORTNR;
                """, as_dict=True)
                frappe.cache().set_value('motorcycle_models' + '_' + ManNo + '_' + NeedYear, data)
    
            return data