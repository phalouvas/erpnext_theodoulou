import frappe
import datetime

class TheodoulouQuery():

    def __init__(self):
        self.settings = frappe.get_doc("Theodoulou Settings")
        self.language = self.settings.get_language()
        self.country = self.settings.get_country()

    def get_years(self):
        current_year = datetime.datetime.now().year
        return list(range(1900, current_year + 1))[::-1]

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
    
    def get_models(self, type, HERNR, NEEDYEAR = 0):
            if not NEEDYEAR:
                NEEDYEAR = 0
            data = frappe.db.sql(f"""
                SELECT
                    T110.KMODNR,  -- ID MODEL
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                    GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                    T110.BJVON AS FROM_YEAR, -- MODEL PRODUCTING FROM YEAR+MONTH
                    IFNULL(T110.BJBIS, 'now') AS TO_YEAR -- MODEL PRODUCTING TO YEAR+MONTH
                FROM `110` AS T110
                    JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
                WHERE 1 
                    AND T100.HERNR = { HERNR }
                    AND T110.{ type } = 1
                    AND (CASE
                            WHEN { NEEDYEAR } = 0 OR LENGTH({ NEEDYEAR }) <> 4 THEN 1					
                            WHEN T110.BJVON <= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) AND IFNULL(T110.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) THEN 1
                            ELSE 0
                        END) = 1
                ORDER BY T110.SORTNR;
            """, as_dict=True)
    
            return data
    
    def get_types_passenger_cars(self, KMODNR, NEEDYEAR = 0):
        if not NEEDYEAR:
            NEEDYEAR = 0
        data = frappe.db.sql(f"""
            SELECT
                T120.KTYPNR AS ID,  -- ID TYPE
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                GET_LBEZNR(T120.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE
                T120.BJVON AS FROM_YEAR, -- TYPE PRODUCTING FROM YEAR+MONTH
                IFNULL(T120.BJBIS, 'now') AS TO_YEAR -- TYPE PRODUCTING TO YEAR+MONTH								
            FROM `120` AS T120
                JOIN `110` AS T110 ON T110.KMODNR = T120.KMODNR			
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
            WHERE 1 
                AND T110.KMODNR = { KMODNR }
                AND (CASE
                        WHEN {  NEEDYEAR } = 0 OR LENGTH({  NEEDYEAR }) <> 4 THEN 1					
                        WHEN T120.BJVON <= CAST(CONCAT({  NEEDYEAR },'01') AS UNSIGNED) AND IFNULL(T120.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({  NEEDYEAR },'01') AS UNSIGNED) THEN 1
                        ELSE 0
                    END) = 1
            ORDER BY T120.SORTNR;	
        """, as_dict=True)

        return data
    
    def get_types_commercial_cars(self, KMODNR, NEEDYEAR = 0):
        if not NEEDYEAR:
            NEEDYEAR = 0
        data = frappe.db.sql(f"""
            SELECT
                T532.NTYPNR AS ID,  -- ID TYPE
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                GET_LBEZNR(T532.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE
                T532.BJVON AS FROM_YEAR, -- TYPE PRODUCTING FROM YEAR+MONTH
                IFNULL(T532.BJBIS, 'now') AS TO_YEAR -- TYPE PRODUCTING TO YEAR+MONTH								
            FROM `532` AS T532
                JOIN `110` AS T110 ON T110.KMODNR = T532.KMODNR			
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
            WHERE 1 
                AND T110.KMODNR = { KMODNR }
                AND (CASE
                        WHEN { NEEDYEAR } = 0 OR LENGTH({ NEEDYEAR }) <> 4 THEN 1					
                        WHEN T532.BJVON <= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) AND IFNULL(T532.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({ NEEDYEAR },'01') AS UNSIGNED) THEN 1
                        ELSE 0
                    END) = 1
            ORDER BY T532.SORT;		
        """, as_dict=True)

        return data