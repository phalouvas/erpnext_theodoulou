import frappe
import datetime

class TheodoulouQuery():

    def __init__(self):
        self.settings = frappe.get_doc("Theodoulou Settings")
        self.language = self.settings.get_language()
        self.country = self.settings.get_country()

    def convert_yyyymm(self, yyyymm):

        if yyyymm is None:
            return '...'

        if yyyymm == 'now':
            return 'now'

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
    
    def get_brand_type_from_vehicle_class(self, BrandClass):
        pc_array = ['pc', 'motorcycle', 'lcv', 'emotorcycle', 'elcv', 'epc']
        cv_array = ['cv', 'bus', 'ebus', 'tractor']
        if BrandClass in pc_array:
            return 'pc'
        elif BrandClass in cv_array:
            return 'cv'
        else:
            frappe.throw("BrandClass not found")

    def get_brands(self, type): 
        # Try to get data from the cache
        data = frappe.cache().get_value('brands_' + type)

        # If data is not in the cache, fetch it from the database
        if data is None:
            data = frappe.db.sql(f"""
                SELECT distinct
                    T100.HERNR,  -- ID MANUFACTURER
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS NAME  -- NAME MANUFACTURER
                FROM `110` AS T110
                    JOIN `100` AS T100 ON T100.HERNR = T110.HERNR			
                WHERE T100.{ type } = 1
                ORDER BY NAME;
            """, as_dict=True)

            # Store data in the cache
            frappe.cache().set_value('brands_' + type, data)

        return data
    
    def get_popular_brands(self, type, popular_brands):
        data = frappe.cache().get_value('popular_brands_' + type)

        if data is None:
            all_brands = self.get_brands(type)
            data = [brand for brand in all_brands if brand['HERNR'] in popular_brands]
            frappe.cache().set_value('popular_brands_' + type, data)

        return data
    
    def get_models(self, type, HERNR, NEEDYEAR = 0):
            
            data = frappe.cache().get_value('models_' + type + '_' + HERNR + '_' + NEEDYEAR)

            if data is None:
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
                frappe.cache().set_value('models_' + type + '_' + HERNR + '_' + NEEDYEAR, data)
    
            return data
    
    def get_types(self, BrandClass, KModNo, needyear):
        type = self.get_brand_type_from_vehicle_class(BrandClass)
        if type == 'pc':
            return self.get_types_passenger_cars(KModNo, needyear)
        elif type == 'cv':
            return self.get_types_commercial_cars(KModNo, needyear)
        else:
            frappe.throw("Type not found")
    
    def get_types_passenger_cars(self, KMODNR, NEEDYEAR = 0):
        data = frappe.cache().get_value('types_passenger_cars_' + KMODNR + '_' + NEEDYEAR)

        if data is None:
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
            frappe.cache().set_value('types_passenger_cars_' + KMODNR + '_' + NEEDYEAR, data)

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
    
    def get_vehicle(self, BrandClass, KTypNo):
        type = self.get_brand_type_from_vehicle_class(BrandClass)
        if type == 'pc':
            return self.get_vehicle_passenger(KTypNo)
        elif type == 'cv':
            return self.get_vehicle_commercial(KTypNo)
        else:
            frappe.throw("Vehicle Type not found")
    
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
    
    def get_node(self, type, node_id):
        data = frappe.db.sql(f"""
            SELECT
                NODE_ID AS ID,
                GET_BEZNR(T301.BEZNR, { self.language }) AS NAME
            FROM `301` AS T301
            WHERE T301.NODE_ID = { node_id }
                AND T301.TREETYPNR = (CASE
                                        WHEN '{ type }' = 'PKW' THEN 1
                                        WHEN '{ type }' = 'LKW' THEN 2
                                        ELSE 0
                                    END);
        """, as_dict=True)

        return data[0]

    def get_categories_tree(self):
        BrandClass = frappe.request.args.get('BrandClass') or frappe.request.cookies.get('BrandClass')
        if BrandClass == "pc":
            LnkTargetType = 2
            TreeTypNo = 1
        elif BrandClass == "motorcycle":
            LnkTargetType = 3
            TreeTypNo = 1
        elif BrandClass == "lcv":
            LnkTargetType = 999
            TreeTypNo = 1
        elif BrandClass == "emotorcycle":
            LnkTargetType = 6
            TreeTypNo = 1
        elif BrandClass == "elcv":
            LnkTargetType = 5
            TreeTypNo = 1
        elif BrandClass == "epc":
            LnkTargetType = 4
            TreeTypNo = 1
        elif BrandClass == "cv":
            LnkTargetType = 16
            TreeTypNo = 2
        elif BrandClass == "bus":
            LnkTargetType = 17
            TreeTypNo = 2
        elif BrandClass == "ebus":
            LnkTargetType = 20
            TreeTypNo = 2
        elif BrandClass == "tractor":
            LnkTargetType = 18
            TreeTypNo = 2
        
        KTypNo = frappe.request.args.get('KTypNo') or frappe.request.cookies.get('KTypNo')
        if KTypNo:
            return self.get_vehicle_categories_tree(TreeTypNo, LnkTargetType, KTypNo)
        else:
            return self.get_all_categories_tree(TreeTypNo)

    def get_all_categories_tree(self, TreeTypNo):

        # Try to get data from the cache
        categories_tree = frappe.cache().get_value(f"categories_tree_{TreeTypNo}")

        # If data is not in the cache, fetch it from the database
        if categories_tree is None:
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
                    LEFT JOIN `301` AS T301_2 ON T301_2.NODE_ID = T301.NODE_PARENT_ID
                    LEFT JOIN `301` AS T301_3 ON T301_3.NODE_ID = T301_2.NODE_PARENT_ID
                    LEFT JOIN `301` AS T301_4 ON T301_4.NODE_ID = T301_3.NODE_PARENT_ID
                    LEFT JOIN `301` AS T301_5 ON T301_5.NODE_ID = T301_4.NODE_PARENT_ID			
                WHERE T301.TREETYPNR = { TreeTypNo }
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

            # Set categories_tree in the cache
            frappe.cache().set_value(f"categories_tree_{TreeTypNo}", categories_tree)

        return categories_tree
    
    def get_vehicle_categories_tree(self, TreeTypNo, LnkTargetType, KTypNo):

        # Try to get data from the cache
        categories_tree = frappe.cache().get_value(f"categories_tree_{TreeTypNo}_{LnkTargetType}_{KTypNo}")

        # If data is not in the cache, fetch it from the database
        if categories_tree is None:
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
                WHERE T301.TREETYPNR = { TreeTypNo }
                    AND T400.VKNZIELART = { LnkTargetType }
                    AND T400.VKNZIELNR = { KTypNo }
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

            # Set categories_tree in the cache
            frappe.cache().set_value(f"categories_tree_{TreeTypNo}_{LnkTargetType}_{KTypNo}", categories_tree)

        return categories_tree
    
    def get_vehicle_products_manufacturers(self, type, vehicle_id, node_id):
        if type == "PKW":
            VKNZIELART = 2
            TREETYPNR = 1
        else:
            VKNZIELART = 16
            TREETYPNR = 2

        data = frappe.cache().get_value('vehicle_products_manufacturers_' + type + '_' + node_id + '_' + vehicle_id)
        if data is None:
            data = frappe.db.sql(f"""
            SELECT DISTINCT
                T001.DLNR,
                T001.MARKE AS MARKE
            FROM `301` AS T301
                JOIN `302` AS T302 ON T302.NODE_ID = T301.NODE_ID			
                JOIN `400` AS T400 ON T302.GENARTNR = T400.GENARTNR					
                JOIN `001` AS T001 ON T001.DLNR = T400.DLNR			
            WHERE T301.TREETYPNR = { TREETYPNR }	
                AND T301.NODE_ID = { node_id }
                AND T400.VKNZIELART = { VKNZIELART }
                AND T400.VKNZIELNR = { vehicle_id }
            ORDER BY T001.MARKE;
        """, as_dict=True)

        return data
    
    def get_vehicle_products_count(self, type, vehicle_id, node_id, manufacturer_id):
        if type == "PKW":
            VKNZIELART = 2
            TREETYPNR = 1
        else:
            VKNZIELART = 16
            TREETYPNR = 2

        if manufacturer_id:
            filter_manufacturer = f"AND T400.DLNR = { manufacturer_id }"
        else:
            filter_manufacturer = ""
            manufacturer_id = ""

        data = frappe.cache().get_value('vehicle_products_count_' + type + '_' + node_id + '_' + vehicle_id + '_' + manufacturer_id)
        if data is None:
            data = frappe.db.sql(f"""
                SELECT COUNT(DISTINCT T400.ARTNR, T400.DLNR) AS total_count
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
                    { filter_manufacturer };
            """, as_dict=True)
            frappe.cache().set_value('vehicle_products_count_' + type + '_' + node_id + '_' + vehicle_id + '_' + manufacturer_id, data)

        return data[0]['total_count']
    
    def get_vehicle_products(self, type, vehicle_id, node_id, manufacturer_id, page):
        if type == "PKW":
            VKNZIELART = 2
            TREETYPNR = 1
        else:
            VKNZIELART = 16
            TREETYPNR = 2

        items_per_page = 20
        offset = (page - 1) * items_per_page

        if manufacturer_id:
            filter_manufacturer = f"AND T001.DLNR = { manufacturer_id }"
        else:
            filter_manufacturer = ""
            
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
                { filter_manufacturer }
            ORDER BY ASSEMBLY_GROUP, NAMEPRODUCT
            LIMIT { offset }, { items_per_page };
        """, as_dict=True)

        return data
    
    def dlnr_from_artnr(self, artnr):
        data = frappe.db.sql(f"""
            SELECT
                T200.DLNR
            FROM `200` AS T200
            WHERE T200.ARTNR = '{ artnr }';
        """, as_dict=True)

        return data[0]['DLNR']
    
    def get_product_main_info(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT
                -- PRODUCT TABLE
                T200.ARTNR AS `ARTNR`, 
                T200.DLNR AS `DLNR`, 
                T001.MARKE AS MARKE,
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
                JOIN `001` AS T001 ON T001.DLNR = T200.DLNR
            WHERE T200.ARTNR = '{ artnr }'
                AND T200.DLNR = { dlnr };
        """, as_dict=True)

        return data[0]
    
    def get_product_criteria(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT DISTINCT
                IFNULL(GET_BEZNR(T050.BEZNR, { self.language }), '') AS NAME,						
                IF(T050.TYP <> 'K', 
                    T210.KRITWERT, 
                    IFNULL(GET_BEZNR_FOR_KEY_TABLE(T050.TABNR, T210.KRITWERT, { self.language }), '')
                    ) AS VALUE
            FROM `200` AS T200		
                JOIN `210` AS T210 ON T210.ARTNR = T200.ARTNR AND T210.DLNR = T200.DLNR
                JOIN `050` AS T050 ON T050.DLNR IN (T200.DLNR, 9999) AND T050.KRITNR = T210.KRITNR
            WHERE T200.ARTNR LIKE '{artnr}'
                AND T200.DLNR = {dlnr}
            ORDER BY T210.SORTNR;
        """, as_dict=True)

        return data
    
    def get_product_additional_info(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT DISTINCT
                IFNULL(GET_BEZNR_FOR_KEY_TABLE(72, T206.INFART, { self.language }), '') AS `INFART`,
                T035.TEXT AS ADDITIONAL_TEXT
            FROM `200` AS T200
                JOIN `206` AS T206 ON T206.ARTNR = T200.ARTNR AND T206.DLNR = T200.DLNR
                JOIN `035` AS T035 ON T035.DLNR = T200.DLNR AND T035.TBSNR = T206.TBSNR AND T035.SPRACHNR = { self.language }
            WHERE T200.ARTNR LIKE '{artnr}'
                AND T200.DLNR = {dlnr}
            HAVING ADDITIONAL_TEXT IS NOT NULL
            ORDER BY T206.SORTNR;
        """, as_dict=True)

        return data
    
    def get_product_oe_numbers(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT DISTINCT
                GET_LBEZNR(T100.LBEZNR, { self.language }) AS CROSS_BRAND,
                T203.REFNR AS CROSS_ARTNR,
                IF(T100.VGL = 1, 'AFTERMARKET RPODUCT', 'OE PRODUCT') AS NOTE
            FROM `200` AS T200
                JOIN `203` AS T203 ON T203.ARTNR = T200.ARTNR AND T203.DLNR = T200.DLNR
                JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR
            WHERE T200.ARTNR LIKE '{artnr}'
                AND T200.DLNR = {dlnr}
            ORDER BY CROSS_BRAND;
        """, as_dict=True)

        # Process the results
        grouped_oe_numbers = {}
        for number in data:
            # If the brand is not in the dictionary, add it
            if number['CROSS_BRAND'] not in grouped_oe_numbers:
                grouped_oe_numbers[number['CROSS_BRAND']] = []

            # Add the artnr to the brand's list
            grouped_oe_numbers[number['CROSS_BRAND']].append(number['CROSS_ARTNR'])

        return grouped_oe_numbers
    
    def get_product_oe_numbers_advanced(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT 
                T.CROSS_BRAND,
                T.CROSS_ARTNR,
                T.NOTE
            FROM (
                -- SHOW STANDARD DATA SUPPLIER
                SELECT 
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS CROSS_BRAND,
                    IFNULL(P2.ARTNR, T203.REFNR) AS CROSS_ARTNR,
                    IF(T100.VGL = 1, 'AFTERMARKET RPODUCT', 'OE PRODUCT') AS NOTE
                FROM `200` AS P
                    JOIN `203` AS T203 ON T203.ARTNR = P.ARTNR AND T203.DLNR = P.DLNR
                    JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR
                    LEFT JOIN `001` AS T001 ON T001.KHERNR = T203.KHERNR
                    LEFT JOIN `200` AS P2 ON P2.ARTNR = CLEAN_NUMBER(T203.REFNR) AND P2.DLNR = T001.DLNR
                WHERE P.ARTNR LIKE '{artnr}'
                    AND P.DLNR = {dlnr}
                
                    UNION
                    
                -- SEARCHING PRODUCTS THAT USE SERACH PRODUCT IN OWN CROSSREF DATA
                SELECT
                    T001_1.MARKE AS CROSS_BRAND,
                    CR.ARTNR AS CROSS_ARTNR,
                    'AFTERMARKET RPODUCT' AS NOTE
                FROM `203` AS CR
                    JOIN `100` AS T100 ON T100.HERNR = CR.KHERNR
                    JOIN `001` AS T001 ON T001.KHERNR = T100.HERNR
                    JOIN `001` AS T001_1 ON T001_1.DLNR = CR.DLNR
                WHERE CR.REFNR LIKE '{ artnr }'
                    AND T001.DLNR = { dlnr }			
                    
                    UNION
                    
                -- SEARCHING MAIN PRODUCTS THAT ARE ANALOGS REGARDING OWN OE-PRODUCTS
                SELECT 
                    T001_1.MARKE AS CROSS_BRAND,
                    CR.ARTNR AS CROSS_ARTNR,				
                    'AFTERMARKET RPODUCT' AS NOTE
                FROM `200` AS P
                    JOIN `203` AS T203 ON T203.ARTNR = P.ARTNR AND T203.DLNR = P.DLNR
                    JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR AND T100.VGL = 0				
                    JOIN `203` AS CR ON CR.REFNR = T203.REFNR AND CR.KHERNR = T203.KHERNR								
                    JOIN `001` AS T001_1 ON T001_1.DLNR = CR.DLNR
                WHERE P.ARTNR LIKE '{artnr}'
                    AND P.DLNR = {dlnr}					
                    
                /*	UNION
                    
                -- SEARCHING ALL CORSSREF PRODUCTS FOR PRODUCTS THAT ARE ANALOGS REGARDING OWN OE-PRODUCTS !!!! THIS POINT CAN HAVE AFFECT ON RIGHT LIST CROSSREFERENCE, YOU CAN DISABLE THIS POINT
                SELECT 
                    GET_LBEZNR(T100_1.LBEZNR, { self.language }) AS CROSS_BRAND,
                    T203_2.REFNR AS CROSS_ARTNR,				
                    IF(T100_1.VGL = 1, 'AFTERMARKET RPODUCT', 'OE PRODUCT') AS NOTE
                FROM `200` AS P
                    JOIN `203` AS T203 ON T203.ARTNR = P.ARTNR AND T203.DLNR = P.DLNR
                    JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR AND T100.VGL = 0				
                    JOIN `203` AS CR ON CR.REFNR = T203.REFNR AND CR.KHERNR = T203.KHERNR				
                    JOIN `203` AS T203_2 ON T203_2.ARTNR = CR.ARTNR AND T203_2.DLNR = CR.DLNR
                    JOIN `100` AS T100_1 ON T100_1.HERNR = T203_2.KHERNR
                WHERE P.ARTNR LIKE '{artnr}'
                    AND P.DLNR = {dlnr}	*/							
                ) AS T
            ORDER BY CROSS_BRAND, CROSS_ARTNR; 
        """, as_dict=True)
    
    def get_product_vehicles_applicability(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT
                T.KTYPE,
                T.VKNZIELART,
                T.BRAND_ID,
                T.MANUFACTURER,
                T.MODEL_ID,
                T.MODEL,
                T.VEHICLE_ID,
                T.TYPE,
                T.BJVON,
                T.BJBIS,
                T.KW,
                T.PS,
                T.CCM,
                T.BODYTYPE,
                T.ENGINETYPE,
                T.LISTENGINES
            FROM (
                -- PASSANGER
                SELECT
                    T120.KTYPNR AS `KTYPE`, 
                    T400.VKNZIELART AS VKNZIELART, -- 2-PASSANGER, 16-TRUCK
                    T100.HERNR AS BRAND_ID,  -- MANUFACTURER ID
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                    T110.KMODNR AS MODEL_ID,  -- MODEL ID
                    GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                    T120.KTYPNR AS VEHICLE_ID,  -- VEHICLE ID
                    GET_LBEZNR(T120.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE					
                    T120.BJVON AS `BJVON`, 
                    IFNULL(T120.BJBIS, 'now') AS `BJBIS`, 
                    IFNULL(T120.KW, '') AS `KW`, 
                    IFNULL(T120.PS, '') AS `PS`, 
                    IFNULL(T120.CCMTECH, '') AS `CCM`, 
                    IFNULL(GET_BEZNR_FOR_KEY_TABLE(86, T120.AUFBAUART, { self.language }), '') AS `BODYTYPE`,
                    IFNULL(GET_BEZNR_FOR_KEY_TABLE(80, T120.MOTART, { self.language }), '') AS `ENGINETYPE`, 
                    IFNULL((SELECT 
                            GROUP_CONCAT(DISTINCT T155.MCODE SEPARATOR ', ')
                        FROM `125` AS T125
                            JOIN `155` AS T155 ON T155.MOTNR = T125.MOTNR
                        WHERE T125.KTYPNR = T120.KTYPNR), '') AS LISTENGINES
                FROM `200` AS T200
                    JOIN `400` AS T400 ON T400.ARTNR = T200.ARTNR AND T400.DLNR = T200.DLNR AND T400.VKNZIELART = 2
                    JOIN `120` AS T120 ON T120.KTYPNR = T400.VKNZIELNR
                    JOIN `110` AS T110 ON T110.KMODNR = T120.KMODNR			
                    JOIN `100` AS T100 ON T100.HERNR = T110.HERNR
                WHERE T200.ARTNR LIKE '{artnr}'
                    AND T200.DLNR = {dlnr}	
                
                    UNION
                    
                -- TRUCK
                SELECT
                    T532.NTYPNR AS `KTYPE`, 
                    T400.VKNZIELART AS VKNZIELART, -- 2-PASSANGER, 16-TRUCK
                    T100.HERNR AS BRAND_ID,  -- MANUFACTURER ID
                    GET_LBEZNR(T100.LBEZNR, { self.language }) AS MANUFACTURER,  -- NAME MANUFACTURER
                    T110.KMODNR AS MODEL_ID,  -- MODEL ID
                    GET_LBEZNR(T110.LBEZNR, { self.language }) AS MODEL,  -- NAME MODEL
                    T532.NTYPNR AS VEHICLE_ID,  -- VEHICLE ID
                    GET_LBEZNR(T532.LBEZNR, { self.language }) AS TYPE,  -- NAME TYPE					
                    T532.BJVON AS `BJVON`, 
                    IFNULL(T532.BJBIS, 'now') AS `BJBIS`, 		
                    IFNULL(T532.KWVON, '') AS `KW`, 
                    IFNULL(T532.PSVON, '') AS `PS`, 
                    IFNULL(T532.CCMTECH, '') AS `CCM`, 
                    IFNULL(GET_BEZNR_FOR_KEY_TABLE(67, T532.BAUART, { self.language }), '') AS `BODYTYPE`,
                    IFNULL(GET_BEZNR_FOR_KEY_TABLE(80, T532.MOTART, { self.language }), '') AS `ENGINETYPE`, 
                    IFNULL((SELECT 
                            GROUP_CONCAT(DISTINCT T155.MCODE SEPARATOR ', ')
                        FROM `537` AS T537
                            JOIN `155` AS T155 ON T155.MOTNR = T537.MOTNR
                        WHERE T537.NTYPNR = T532.NTYPNR), '') AS LISTENGINES
                FROM `200` AS T200
                    JOIN `400` AS T400 ON T400.ARTNR = T200.ARTNR AND T400.DLNR = T200.DLNR AND T400.VKNZIELART = 16
                    JOIN `532` AS T532 ON T532.NTYPNR = T400.VKNZIELNR
                    JOIN `110` AS T110 ON T110.KMODNR = T532.KMODNR			
                    JOIN `100` AS T100 ON T100.HERNR = T110.HERNR
                WHERE T200.ARTNR LIKE '{artnr}'
                    AND T200.DLNR = {dlnr}	
                ) AS T
            ORDER BY MANUFACTURER, MODEL, TYPE; 		
        """, as_dict=True)

        for row in data:
            row['BJVON'] = self.convert_yyyymm(row['BJVON'])
            row['BJBIS'] = self.convert_yyyymm(row['BJBIS'])

        return data

    def get_product_media(self, dlnr, artnr):
        data = frappe.db.sql(f"""
            SELECT
                IFNULL(GET_BEZNR(T014.BEZNR, { self.language }), '') AS INFO,
                GET_BEZNR_FOR_KEY_TABLE(143, T231.BILDTYPE, { self.language }) AS `BILDTYPE`, 
                GET_BEZNR_FOR_KEY_TABLE(141, T231.BEZNORM, { self.language }) AS `Standardised Graphic Header`, 
                IFNULL(T231.BREIT, '') AS `Graphic width`, 
                IFNULL(T231.HOCH, '') AS `Graphic height`, 
                IFNULL(T231.FARBEN, '') AS `Colour Quantity`, 
                IFNULL(GET_BEZNR(T231.BEZNR, { self.language }), '') AS `Description`,
                CONCAT(
                    (CASE
                        WHEN IFNULL(T014.EXTENSION, '') = 'PDF' THEN '{ self.settings.pdf_url }' 
                        WHEN IFNULL(T014.EXTENSION, '') IN ('BMP','JPG','PNG','GIF') THEN '{ self.settings.images_url }'
                        ELSE ''
                    END), -- URL SERVER WHERE PLACED IMAGES OR PDF
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN CONCAT(T200.DLNR, '/')
                        ELSE ''
                    END), -- FOLDER
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN T231.BILDNAME
                        ELSE ''
                    END), -- NAME FILE
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN CONCAT('.', T014.EXTENSION)
                        ELSE T231.URL
                    END) -- EXTENSION
                    ) AS PATH
            FROM `200` AS T200
                JOIN `232` AS T232 ON T232.ARTNR = T200.ARTNR AND T232.DLNR = T200.DLNR
                JOIN `231` AS T231 ON T231.BILDNR = T232.BILDNR AND T231.SPRACHNR IN ({ self.language }, 255) AND T231.DOKUMENTENART = T232.DOKUMENTENART
                LEFT JOIN `014` AS T014 ON T014.DOKUMENTENART = T232.DOKUMENTENART
            WHERE T200.ARTNR LIKE '{artnr}'
                AND T200.DLNR = {dlnr}
            ORDER BY T232.SORTNR;
        """, as_dict=True)

        return data

    def get_manufacturer_logo(self, dlnr):
        data = frappe.db.sql(f"""
            SELECT
                IFNULL(GET_BEZNR(T014.BEZNR, { self.language }), '') AS INFO,
                GET_BEZNR_FOR_KEY_TABLE(143, T231.BILDTYPE, { self.language }) AS `BILDTYPE`, 
                GET_BEZNR_FOR_KEY_TABLE(141, T231.BEZNORM, { self.language }) AS `Standardised Graphic Header`, 
                IFNULL(T231.BREIT, '') AS `Graphic width`, 
                IFNULL(T231.HOCH, '') AS `Graphic height`, 
                IFNULL(T231.FARBEN, '') AS `Colour Quantity`, 
                IFNULL(GET_BEZNR(T231.BEZNR, { self.language }), '') AS `Description`,
                CONCAT(
                    (CASE
                        WHEN IFNULL(T014.EXTENSION, '') = 'PDF' THEN '{ self.settings.pdf_url }' 
                        WHEN IFNULL(T014.EXTENSION, '') IN ('BMP','JPG','PNG','GIF') THEN '{ self.settings.images_url }' 
                        ELSE ''
                    END), -- URL SERVER WHERE PLACED IMAGES OR PDF
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN CONCAT(T042.DLNR, '/')
                        ELSE ''
                    END), -- FOLDER
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN T231.BILDNAME
                        ELSE ''
                    END), -- NAME FILE
                    (CASE					
                        WHEN IFNULL(T014.EXTENSION, '') IN ('PDF','BMP','JPG','PNG','GIF') THEN CONCAT('.', T014.EXTENSION)
                        ELSE T231.URL
                    END) -- EXTENSION
                    ) AS PATH
            FROM `042` AS T042
                JOIN `231` AS T231 ON T231.BILDNR = T042.BILDNR AND T231.BILDNR = T042.BILDNR AND T231.SPRACHNR IN ({ self.language }, 255) AND T231.DOKUMENTENART = T042.DOKUMENTENART
                LEFT JOIN `014` AS T014 ON T014.DOKUMENTENART = T042.DOKUMENTENART
            WHERE T042.DLNR = {dlnr};
        """, as_dict=True)

        return data[0]['PATH']
    
    def get_product_analogs(self, artnr, search_brand = ''):

        data = frappe.db.sql(f"""
            SELECT 
                T.DLNR AS DLNR,
                T001.MARKE AS BRAND,
                T.ARTNR AS ARTNR,
                IFNULL(GET_BEZNR(T320.BEZNR, {self.language}), '') AS `NAMEPRODUCT`,
                IFNULL(GET_BEZNR(T324.BEZNR, {self.language}), '') AS ASSEMBLY_GROUP,
                GROUP_CONCAT(DISTINCT CONCAT('[',T.TRUST,'%] - ',T.NOTE,CHAR(10)) SEPARATOR '') AS NOTE,
                IF(MIN(T.TRUST) = MAX(T.TRUST), MIN(T.TRUST), CONCAT(MIN(CAST(T.TRUST AS UNSIGNED)), ' - ', MAX(CAST(T.TRUST AS UNSIGNED)))) AS TRUST_IN
            FROM (
                    -- SEARCH IN STANDARD TABLE PRODUCTS TECDOC SUPPLIERS - CAN USE NUMBER EVEN WITH ADIDITONAL SYMBOLS
                    SELECT
                        T200.DLNR AS DLNR,					
                        T200.ARTNR AS ARTNR,
                        'FOUND IN MAIN TABLE PRODUCTS' AS NOTE,
                        '100' AS TRUST
                    FROM `200` AS T200
                        LEFT JOIN `001` AS T001 ON T001.DLNR = T200.DLNR
                    WHERE T200.ARTNR = '{artnr}'
                        AND IF(TRIM('{search_brand}') = '' OR (TRIM('{search_brand}') <> '' AND T001.MARKE = '{search_brand}'), 1, 0) = 1
                    
                        UNION
                        
                    -- SEARCH IN EAN TABLE - CAN USE NUMBER EVEN WITH ADIDITONAL SYMBOLS
                    SELECT
                        T209.DLNR AS DLNR,					
                        T209.ARTNR AS ARTNR,
                        'FOUND IN EAN TABLE' AS NOTE,
                        '100' AS TRUST
                    FROM `209` AS T209					
                    WHERE T209.EANNR = '{artnr}'	
                    
                        UNION
                        
                    -- SEARCH IN SUPERSEDED TABLE - MUST USE RIGHT ARTNUMBER
                    SELECT
                        T204.DLNR AS DLNR,					
                        T204.ARTNR AS ARTNR,
                        'FOUND IN SUPERSEDED TABLE PRODUCTS' AS NOTE,
                        '100' AS TRUST
                    FROM `204` AS T204
                        LEFT JOIN `001` AS T001 ON T001.DLNR = T204.DLNR
                    WHERE T204.ERSATZNR = '{artnr}'
                        AND IF(TRIM('{search_brand}') = '' OR (TRIM('{search_brand}') <> '' AND T001.MARKE = '{search_brand}'), 1, 0) = 1					
                        
                        UNION
                        
                    -- SEARCH IN USER NUMBER TABLE - MUST USE RIGHT NUMBER
                    SELECT
                        T207.DLNR AS DLNR,					
                        T207.ARTNR AS ARTNR,
                        'FOUND IN USERNUMBER TABLE' AS NOTE,
                        '100' AS TRUST
                    FROM `207` AS T207					
                    WHERE T207.GEBRNR = '{artnr}'
                        
                        UNION
                        
                    -- SEARCH IN CROSSREFERENCE TABLE - SHOW TECDOC PRODUCTS WHERE IS INCLUDED SEARCH NUMBER - CAN USE NUMBER EVEN WITH ADIDITONAL SYMBOLS
                    SELECT
                        T203.DLNR AS DLNR,
                        T203.ARTNR AS ARTNR,
                        CONCAT('FOUND IN CROSSREFERENCE TABLE [WHERE PRODUCT WITH SEARCH NUMBER "','{artnr}','" AND BRAND "',ifnull(GET_LBEZNR(T100.LBEZNR, 1), ''),'" INCLUDED IN OTHER PRODUCTS]') AS NOTE,
                        '90' AS TRUST
                    FROM `203` AS T203					
                        LEFT JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR
                    WHERE T203.REFNR = '{artnr}'
                        AND IF(TRIM('{search_brand}') = '' OR (TRIM('{search_brand}') <> '' AND GET_LBEZNR(T100.LBEZNR, 1) = '{search_brand}'), 1, 0) = 1	
                    
                        UNION
                        
                    -- SEARCH IN CROSSREFERENCE TABLE - SHOW INCLUDED CROSSREFERENCE PRODUCTS THAT FOUND FOR MAIN SEARCH NUMBER PRODUCT - CAN USE NUMBER EVEN WITH ADIDITONAL SYMBOLS
                    SELECT
                        T200_2.DLNR AS DLNR,					
                        T200_2.ARTNR AS ARTNR,
                        CONCAT('FOUND IN CROSSREFERENCE TABLE [WHERE OTHER PRODUCTS ARE INCLUDED IN PRODUCT WITH SEARCH NUMBER "',T200.ARTNR,'" AND BRAND "',T001.MARKE,'"]') AS NOTE,
                        '90' AS TRUST
                    FROM `200` AS T200
                        JOIN `001` AS T001 ON T001.DLNR = T200.DLNR
                        JOIN `203` AS T203 ON T203.ARTNR = T200.ARTNR AND T203.DLNR = T200.DLNR
                        JOIN `001` AS T001_2 ON T001_2.KHERNR = T203.KHERNR
                        JOIN `200` AS T200_2 ON T200_2.ARTNR = T203.REFNR AND T200_2.DLNR = T001_2.DLNR					
                    WHERE T200.ARTNR = '{artnr}'
                        AND IF(TRIM('{search_brand}') = '' OR (TRIM('{search_brand}') <> '' AND T001.MARKE = '{search_brand}'), 1, 0) = 1				

                        UNION
                        
                    -- SEARCH IN CROSSREFERENCE TABLE - SHOW ALL ANALOGS REGARDING OWN OE-NUMBERS FOR MAIN SEARCH NUMBER PRODUCT - CAN USE NUMBER EVEN WITH ADIDITONAL SYMBOLS
                    -- QUERY WILL WORK ONLY WHEN USE SEARCHBRAND
                    SELECT
                        T203_2.DLNR AS DLNR,
                        T203_2.ARTNR AS ARTNR,
                        CONCAT('FOUND IN CROSSREFERENCE TABLE [FOUND ANALOGS VIA OE-NUMBERS FOR PRODUCT WITH SEARCH NUMBER "',T200.ARTNR,'" AND BRAND "',T001.MARKE,'"]') AS NOTE,
                        '80' AS TRUST
                    FROM `200` AS T200
                        JOIN `001` AS T001 ON T001.DLNR = T200.DLNR
                        JOIN `203` AS T203 ON T203.ARTNR = T200.ARTNR AND T203.DLNR = T200.DLNR
                        JOIN `100` AS T100 ON T100.HERNR = T203.KHERNR AND (T100.PKW = 1 OR T100.NKW = 1)
                        JOIN `203` AS T203_2 ON T203_2.REFNR = T203.REFNR AND T203_2.KHERNR = T203.KHERNR															
                    WHERE TRIM('{search_brand}') <> ''
                        AND T200.ARTNR = '{artnr}'
                        AND T001.MARKE = '{search_brand}'
                    
                ) as T
                JOIN `211` AS T211 ON T211.ARTNR = T.ARTNR AND T211.DLNR = T.DLNR
                JOIN `320` AS T320 ON T320.GENARTNR = T211.GENARTNR
                LEFT JOIN `324` AS T324 ON T324.BGNR = T320.BGNR
                LEFT JOIN `001` AS T001 ON T001.DLNR = T.DLNR	
            GROUP BY T.DLNR, T.ARTNR;
        """, as_dict=True)

        return data
