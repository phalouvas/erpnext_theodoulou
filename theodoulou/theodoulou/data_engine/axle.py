import frappe

from theodoulou.theodoulou.data_engine.query import TheodoulouQuery

class AxleQuery(TheodoulouQuery):

    def __init__(self):
        self.title = frappe._('Axles')
        super().__init__()
    
    def get_brands(self):
        data = frappe.cache().get_value('axle_brands')
        if data is None:
            data = frappe.db.sql(f"""
                SELECT DISTINCT 
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `100` AS T100
                WHERE T100.ACHSE = 1
                ORDER BY NAME;
            """, as_dict=True)
            frappe.cache().set_value('axle_brands', data)

        return data
    
    def get_models(self, ManNo, NeedYear = 0):
            
            data = frappe.cache().get_value('axle_models' + '_' + ManNo + '_' + NeedYear)

            if data is None:
                data = frappe.db.sql(f"""
                    SELECT DISTINCT
                        T110.KMODNR AS KModNo,  -- ID MODEL
                        GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                        GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                        T110.BJVON AS FROM_YEAR, -- MODEL PRODUCTING FROM YEAR+MONTH
                        IFNULL(T110.BJBIS, 'now') AS TO_YEAR -- MODEL PRODUCTING TO YEAR+MONTH
                    FROM `110` AS T110
                        JOIN `100` AS T100 ON T100.HerNr = T110.HerNr
                    WHERE 1 
                        AND T100.HERNR = { ManNo }
                        AND (CASE
                                WHEN { NeedYear } = 0 OR LENGTH({ NeedYear }) <> 4 THEN 1					
                                WHEN T110.BJVON <= CAST(CONCAT({ NeedYear },'01') AS UNSIGNED) AND IFNULL(T110.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({ NeedYear },'01') AS UNSIGNED) THEN 1
                                ELSE 0
                            END) = 1
                        AND T110.ACHSE = 1
                    ORDER BY T110.SORTNR;
                """, as_dict=True)
                frappe.cache().set_value('axle_models' + '_' + ManNo + '_' + NeedYear, data)
    
            return data
    
    def get_types(self, BrandClass, KModNo, needyear):
        data = frappe.cache().get_value(f"types_{BrandClass}_{KModNo}_{needyear}")

        if data is None:
            data = frappe.db.sql(f"""
                SELECT
                    T160.ATYPNR AS KTypNo,  -- ID TYPE
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                    GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                    T160.BEZEICHNUNG AS TYPE,  -- NAME TYPE
                    T160.BJVON AS FROM_YEAR, -- TYPE PRODUCTING FROM YEAR+MONTH
                    IFNULL(T160.BJBIS, 'now') AS TO_YEAR -- TYPE PRODUCTING TO YEAR+MONTH								
                FROM `160` AS T160
                    JOIN `110` AS T110 ON T110.KMODNR = T160.KMODNR			
                    JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
                WHERE 1 
                    AND T110.KMODNR = {KModNo}
                    AND (CASE
                            WHEN {needyear} = 0 OR LENGTH({needyear}) <> 4 THEN 1					
                            WHEN T160.BJVON <= CAST(CONCAT({needyear},'01') AS UNSIGNED) AND IFNULL(T160.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT({needyear},'01') AS UNSIGNED) THEN 1
                            ELSE 0
                        END) = 1
                ORDER BY T160.SORTNR;	
            """, as_dict=True)
            frappe.cache().set_value(f"types_{BrandClass}_{KModNo}_{needyear}", data)

        return data
    
    def get_vehicle(self, BrandClass, KTypNo):
        data = frappe.db.sql(f"""
            SELECT			
                T160.ATYPNR AS `TecDoc Type no`, 
                GET_LBEZNR(T100.LBEZNR, {self.language}) AS Manufacturer,  -- NAME MANUFACTURER
                GET_LBEZNR(T110.LBEZNR, {self.language}) AS Model,  -- NAME MODEL
                T160.BEZEICHNUNG AS Type,  -- NAME TYPE					
                T160.BJVON AS `From Year`, 
                IFNULL(T160.BJBIS, 'now') AS `To Year`, 	
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(68, T160.ACHSART, {self.language}), '') AS `Axle type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(95, T160.AUSFUHRUNG, {self.language}), '') AS `Style`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(83, T160.BREMSAUSF, {self.language}), '') AS `Brake type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(214, T160.ACHSKORPER, {self.language}), '') AS `Axle-body`, 
                IFNULL(T160.ZULLASTVON, '') AS `Maximum Axle Load in Kg from`, 
                IFNULL(T160.ZULLASTBIS, '') AS `Maximum Axle Load in Kg to`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(213, T160.RADBEFESTIGUNG, {self.language}), '') AS `Wheel mounting`, 
                IFNULL(T160.SPURWEITE, '') AS `Track width (mm)`, 
                IFNULL(T160.NABENSYSTEM, '') AS `Hub system`, 
                IFNULL(T160.FAHRHOHE_VON, '') AS `Distance between road pavement and vehicle frame from`, 
                IFNULL(T160.FAHRHOHE_BIS, '') AS `Distance between road pavement and vehicle frame to`			
            FROM `160` AS T160		
                JOIN `110` AS T110 ON T110.KMODNR = T160.KMODNR			
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR
            WHERE T160.ATYPNR = {KTypNo};
        """, as_dict=True)

        return data