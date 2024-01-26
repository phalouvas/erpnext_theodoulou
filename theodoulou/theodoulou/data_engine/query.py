import frappe
import datetime

class TheodoulouQuery():

    def __init__(self):
        self.settings = frappe.get_doc("Theodoulou Settings")
        self.language = self.settings.get_language()
        self.country = self.settings.get_country()

    def convert_yyyymm(self, yyyymm):
        # Convert the integer to string
        year_month = str(yyyymm)

        # Extract the year and month
        year = year_month[:4]
        month = year_month[4:]

        # Format the string as mm.yyyy
        formatted_date = f"{month}.{year}"

        # Assign the formatted date back to the context
        return formatted_date

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
    
    def get_vehicle_passenger(self, ID):
        data = frappe.db.sql(f"""
            SELECT			
			T120.KTYPNR AS `ID`, 
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                GET_LBEZNR(T120.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE					
                T120.BJVON AS `FROM_YEAR`, 
                IFNULL(T120.BJBIS, 'now') AS `TO_YEAR`, 
                IFNULL(T120.KW, '') AS `Engine output in kW`, 
                IFNULL(T120.PS, '') AS `Engine output in HP`, 
                IFNULL(T120.CCMSTEUER, '') AS `Engine capacity in cc (taxation value)`, 
                IFNULL(T120.CCMTECH, '') AS `Engine capacity in cc (technical value)`, 
                IFNULL(T120.LIT, '') AS `Engine capacity in litre *100 (99V99)`, 
                IFNULL(T120.ZYL, '') AS `Number of cylinders`, 
                IFNULL(T120.TUEREN, '') AS `Number of doors`, 
                IFNULL(T120.TANKINHALT, '') AS `Fuel tank capacity`, 
                IFNULL(T120.SPANNUNG, '') AS `Main current voltage`, 
                IFNULL((CASE
                        WHEN T120.ABS = 0 THEN 'NO'
                        WHEN T120.ABS = 1 THEN 'YES'
                        WHEN T120.ABS = 2 THEN 'OPTIONAL'
                        WHEN T120.ABS = 9 THEN 'UNKNOWN'
                        ELSE NULL
                        END), '') AS `ABS`, 
                IFNULL((CASE
                        WHEN T120.ASR = 0 THEN 'NO'
                        WHEN T120.ASR = 1 THEN 'YES'
                        WHEN T120.ASR = 2 THEN 'OPTIONAL'
                        WHEN T120.ASR = 9 THEN 'UNKNOWN'
                        ELSE NULL
                        END), '') AS `ASR`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(80, T120.MOTART, { self.language }), '') AS `Engine type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(97, T120.KRAFTSTOFFAUFBEREITUNGSPRINZIP, { self.language }), '') AS `Fuel mixture formation`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(82, T120.ANTRART, { self.language }), '') AS `Drive type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(83, T120.BREMSART, { self.language }), '') AS `Brake type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(84, T120.BREMSSYS, { self.language }), '') AS `Brake system`, 
                IFNULL(T120.VENTILE_BRENNRAUM, '') AS `Number of valves`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(182, T120.KRSTOFFART, { self.language }), '') AS `Fuel type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(89, T120.KATART, { self.language }), '') AS `Catalyst converter type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(85, T120.GETRART, { self.language }), '') AS `Transmission type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(86, T120.AUFBAUART, { self.language }), '') AS `Body type`,
                IFNULL((SELECT 
                            GROUP_CONCAT(DISTINCT T155.MCODE SEPARATOR ', ')
                        FROM `125` AS T125
                            JOIN `155` AS T155 ON T155.MOTNR = T125.MOTNR
                        WHERE T125.KTYPNR = T120.KTYPNR), '') AS `Engine numbers`
            FROM `120` AS T120		
                JOIN `110` AS T110 ON T110.KMODNR = T120.KMODNR			
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR
            WHERE T120.KTYPNR = { ID };	
        """, as_dict=True)

        return data
    
    def get_vehicle_commercial(self, ID):
        data = frappe.db.sql(f"""
            SELECT			
                T532.NTYPNR AS `ID`, 
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                GET_LBEZNR(T532.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE					
                T532.BJVON AS `FROM_YEAR`, 
                IFNULL(T532.BJBIS, 'now') AS `TO_YEAR`, 			
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(67, T532.BAUART, { self.language }), '') AS `Body Type`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(80, T532.MOTART, { self.language }), '') AS `Engine Type`, 
                IFNULL(T532.KWVON, '') AS `Engine output in kW from`, 
                IFNULL(T532.KWBIS, '') AS `Engine output in kW to`, 
                IFNULL(T532.PSVON, '') AS `Engine output in HP from`, 
                IFNULL(T532.PSBIS, '') AS `Engine output in HP to`, 
                IFNULL(T532.CCMTECH, '') AS `Engine capacity in cc (technical)`, 
                IFNULL(T532.TONNAGE, '') AS `Tonnage in tonnes with 2 decimal spaces`, 
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(65, T532.ACHSCONFIG, { self.language }), '') AS `Axle Configuration`,
                IFNULL((SELECT 
                            GROUP_CONCAT(DISTINCT T155.MCODE SEPARATOR ', ')
                        FROM `537` AS T537
                            JOIN `155` AS T155 ON T155.MOTNR = T537.MOTNR
                        WHERE T537.NTYPNR = T532.NTYPNR), '') AS `Engine numbers`						
            FROM `532` AS T532		
                JOIN `110` AS T110 ON T110.KMODNR = T532.KMODNR			
                JOIN `100` AS T100 ON T100.HERNR = T110.HERNR
            WHERE T532.NTYPNR = { ID };		
        """, as_dict=True)

        return data
    
    def get_vehicle_categories(self, type, ID):

        if type == "PKW":
            VKNZIELART = 2
            TREETYPNR = 1
        else:
            VKNZIELART = 16
            TREETYPNR = 2

        data = frappe.db.sql(f"""
            SELECT DISTINCT	
                T301.STUFE,  -- ACTIVE LEVES
                ELT(T301.STUFE, GET_BEZNR(T301.BEZNR, { self.language }), GET_BEZNR(T301_2.BEZNR, { self.language }), GET_BEZNR(T301_3.BEZNR, { self.language }), GET_BEZNR(T301_4.BEZNR, { self.language }), GET_BEZNR(T301_5.BEZNR, { self.language })) AS STR_TEXT1,
                ELT(T301.STUFE, T301.NODE_ID, T301_2.NODE_ID, T301_3.NODE_ID, T301_4.NODE_ID, T301_5.NODE_ID) AS NODE_ID1,
                ELT(T301.STUFE-1, GET_BEZNR(T301.BEZNR, { self.language }), GET_BEZNR(T301_2.BEZNR, { self.language }), GET_BEZNR(T301_3.BEZNR, { self.language }), GET_BEZNR(T301_4.BEZNR, { self.language }), GET_BEZNR(T301_5.BEZNR, { self.language })) AS STR_TEXT2,
                ELT(T301.STUFE-1, T301.NODE_ID, T301_2.NODE_ID, T301_3.NODE_ID, T301_4.NODE_ID, T301_5.NODE_ID) AS NODE_ID2,
                ELT(T301.STUFE-2, GET_BEZNR(T301.BEZNR, { self.language }), GET_BEZNR(T301_2.BEZNR, { self.language }), GET_BEZNR(T301_3.BEZNR, { self.language }), GET_BEZNR(T301_4.BEZNR, { self.language }), GET_BEZNR(T301_5.BEZNR, { self.language })) AS STR_TEXT3,
                ELT(T301.STUFE-2, T301.NODE_ID, T301_2.NODE_ID, T301_3.NODE_ID, T301_4.NODE_ID, T301_5.NODE_ID) AS NODE_ID3,
                ELT(T301.STUFE-3, GET_BEZNR(T301.BEZNR, { self.language }), GET_BEZNR(T301_2.BEZNR, { self.language }), GET_BEZNR(T301_3.BEZNR, { self.language }), GET_BEZNR(T301_4.BEZNR, { self.language }), GET_BEZNR(T301_5.BEZNR, { self.language })) AS STR_TEXT4,
                ELT(T301.STUFE-3, T301.NODE_ID, T301_2.NODE_ID, T301_3.NODE_ID, T301_4.NODE_ID, T301_5.NODE_ID) AS NODE_ID4,
                ELT(T301.STUFE-4, GET_BEZNR(T301.BEZNR, { self.language }), GET_BEZNR(T301_2.BEZNR, { self.language }), GET_BEZNR(T301_3.BEZNR, { self.language }), GET_BEZNR(T301_4.BEZNR, { self.language }), GET_BEZNR(T301_5.BEZNR, { self.language })) AS STR_TEXT5,
                ELT(T301.STUFE-4, T301.NODE_ID, T301_2.NODE_ID, T301_3.NODE_ID, T301_4.NODE_ID, T301_5.NODE_ID) AS NODE_ID5		
            FROM `301` AS T301
                JOIN `302` AS T302 ON T302.NODE_ID = T301.NODE_ID			
                JOIN `400` AS T400 ON T302.GENARTNR = T400.GENARTNR	
                LEFT JOIN `301` AS T301_2 ON T301_2.NODE_ID = T301.NODE_PARENT_ID
                LEFT JOIN `301` AS T301_3 ON T301_3.NODE_ID = T301_2.NODE_PARENT_ID
                LEFT JOIN `301` AS T301_4 ON T301_4.NODE_ID = T301_3.NODE_PARENT_ID
                LEFT JOIN `301` AS T301_5 ON T301_5.NODE_ID = T301_4.NODE_PARENT_ID			
            WHERE T301.TREETYPNR = { TREETYPNR }
                AND T400.VKNZIELART = { VKNZIELART }
                AND T400.VKNZIELNR = { ID }
            ORDER BY STR_TEXT1, STR_TEXT2, STR_TEXT3, STR_TEXT4, STR_TEXT5;
        """, as_dict=True)

        # Initialize the categories_tree
        categories_tree = {}
        for row in data:
            # Get the current node
            node = categories_tree

            # Loop through the levels
            for level in range(1, row['STUFE'] + 1):
                # Get the text and id for this level
                text = row[f'STR_TEXT{level}']
                id = row[f'NODE_ID{level}']

                # If this node does not exist, create it
                if text not in node:
                    node[text] = {'id': id, 'children': {}}

                # Move to the next level
                node = node[text]['children']

        return categories_tree
    
    def get_vehicle_products(self, type, vehicle_id, node_id):
        if type == "PKW":
            VKNZIELART = 2
            TREETYPNR = 1
        else:
            VKNZIELART = 16
            TREETYPNR = 2
            
        data = frappe.db.sql(f"""
            SELECT DISTINCT
                T400.VKNZIELART,
                T400.VKNZIELNR,
                T400.GENARTNR,
                T400.ARTNR,
                T400.DLNR,
                T001.MARKE AS MARKE,
                T200.ARTNR AS ARTNR,				
                IFNULL(GET_BEZNR(T324.BEZNR, { self.language }), '') AS ASSEMBLY_GROUP,
                CONCAT(IFNULL(GET_BEZNR(T320.BEZNR, { self.language }), ''), IFNULL(CONCAT(' ', GET_BEZNR(T200.BEZNR, { self.language })), '')) AS `NAMEPRODUCT`,
                IFNULL(GET_BEZNR(T323.BEZNR, { self.language }), '') AS STANDARD_GROUP,			
                IFNULL(GET_BEZNR(T325.BEZNR, { self.language }), '') AS PURPOSE_GROUP
            FROM `301` AS T301
                JOIN `302` AS T302 ON T302.NODE_ID = T301.NODE_ID			
                JOIN `400` AS T400 ON T302.GENARTNR = T400.GENARTNR					
                JOIN `320` AS T320 ON T320.GENARTNR = T400.GENARTNR
                JOIN `200` AS T200 ON T200.ARTNR = T400.ARTNR AND T200.DLNR = T400.DLNR						
                JOIN `001` AS T001 ON T001.DLNR = T200.DLNR			
                LEFT JOIN `323` AS T323 ON T323.NARTNR = T320.NARTNR
                LEFT JOIN `324` AS T324 ON T324.BGNR = T320.BGNR
                LEFT JOIN `325` AS T325 ON T325.VERWNR = T320.VERWNR
            WHERE T301.TREETYPNR = { TREETYPNR }	
                AND T301.NODE_ID = { node_id }
                AND T400.VKNZIELART = { VKNZIELART }
                AND T400.VKNZIELNR = { vehicle_id }
            ORDER BY ASSEMBLY_GROUP, NAMEPRODUCT;
        """, as_dict=True)

        return data
    
    def get_product(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT
                -- PRODUCT TABLE
                T200.ARTNR AS `ARTNR`, 
                T200.DLNR AS `DLNR`, 
                IFNULL(GET_BEZNR(T200.BEZNR, { self.language }), '') AS `PREFIXFOR_NAMEPRODUCT`, 
                (CASE
                    WHEN T200.KZSB = 1 THEN 'SELF-SERVICE PACKING'				
                    ELSE ''
                END) AS `KZSB`, 
                (CASE
                    WHEN T200.KZMAT = 1 THEN 'MANDATORY MATERIAL CERTIFICATION'				
                    ELSE ''
                END) AS `KZMAT`, 
                (CASE
                    WHEN T200.KZAT = 1 THEN 'REMANUFACTURED PART'				
                    ELSE ''
                END) AS `KZAT`, 
                (CASE
                    WHEN T200.KZZUB = 1 THEN 'ACCESSORY'				
                    ELSE ''
                END) AS `KZZUB`, 
                IFNULL(T200.LOSGR1, '') AS `LOSGR1`, 
                IFNULL(T200.LOSGR2, '') AS `LOSGR2`,
                -- TRADE GROUPS
                T320.GENARTNR,
                IFNULL(GET_BEZNR(T320.BEZNR, { self.language }), '') AS `NAMEPRODUCT`,
                IFNULL(GET_BEZNR(T323.BEZNR, { self.language }), '') AS STANDARD_GROUP,
                IFNULL(GET_BEZNR(T324.BEZNR, { self.language }), '') AS ASSEMBLY_GROUP,
                IFNULL(GET_BEZNR(T325.BEZNR, { self.language }), '') AS PURPOSE_GROUP,			
                -- ADDITIONAL DATA
                IFNULL((SELECT
                            GROUP_CONCAT(DISTINCT CONCAT('[VPE:',IFNULL(T212.VPE, ''),',MENGEPROVPE:',IFNULL(T212.MENGEPROVPE, ''),',ARTSTAT:',IFNULL(GET_BEZNR_FOR_KEY_TABLE(73, T212.ARTSTAT, { self.language }), ''),',STATUSDAT:',IFNULL(T212.STATUSDAT, ''),']'))
                        FROM `212` AS T212
                        WHERE T212.ARTNR = T200.ARTNR AND T212.DLNR = T200.DLNR), '') AS PACKINFO, -- 212
                IFNULL((SELECT
                            GROUP_CONCAT(DISTINCT T209.EANNR)
                        FROM `209` AS T209
                        WHERE T209.ARTNR = T200.ARTNR AND T209.DLNR = T200.DLNR), '') AS EAN, -- 209
                IFNULL((SELECT
                            GROUP_CONCAT(DISTINCT T207.GEBRNR)
                        FROM `207` AS T207
                        WHERE T207.ARTNR = T200.ARTNR AND T207.DLNR = T200.DLNR
                        ORDER BY T207.SORTNR), '') AS LIST_USERNUMBERS, -- 207
                IFNULL((SELECT
                            GROUP_CONCAT(DISTINCT T204.ERSATZNR)
                        FROM `204` AS T204
                        WHERE T204.ARTNR = T200.ARTNR AND T204.DLNR = T200.DLNR
                        ORDER BY T204.SORT), '') AS LIST_REPLACEDNUMBERS -- 204			
            FROM `200` AS T200
                JOIN `211` AS T211 ON T211.ARTNR = T200.ARTNR AND T211.DLNR = T200.DLNR
                JOIN `320` AS T320 ON T320.GENARTNR = T211.GENARTNR
                LEFT JOIN `323` AS T323 ON T323.NARTNR = T320.NARTNR
                LEFT JOIN `324` AS T324 ON T324.BGNR = T320.BGNR
                LEFT JOIN `325` AS T325 ON T325.VERWNR = T320.VERWNR
            WHERE T200.ARTNR = '{ artnr }'
                AND T200.DLNR = { dlnr };
        """, as_dict=True)

        return data