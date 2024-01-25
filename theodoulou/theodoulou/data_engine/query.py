import frappe

class TheodoulouQuery():

    def __init__(self):
        self.settings = frappe.get_doc("Theodoulou Settings")
        self.language = self.settings.get_language()
        self.country = self.settings.get_country()

    def get_brands(self, type, NEEDYEAR = 0): 

        data = frappe.db.sql(f"""
            SELECT distinct
                T100.HERNR,  -- ID MANUFACTURER
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
            FROM `110` AS T110
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
            WHERE 1
                AND (CASE
                        WHEN { NEEDYEAR } = 0 OR LENGTH({ NEEDYEAR }) <> 4 THEN 1					
                        WHEN T110.BJVON <= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) AND IFNULL(T110.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) THEN 1
                        ELSE 0
                    END) = 1
                AND T100.{ type } = 1
            ORDER BY NAME;
        """, as_dict=True)

        return data