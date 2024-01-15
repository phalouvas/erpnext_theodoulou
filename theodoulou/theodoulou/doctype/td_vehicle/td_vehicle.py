# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TDVehicle(Document):
	
	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		pass

	def db_update(self):
		pass

	@staticmethod
	def get_list(args):	
		start = int(args.get('start'))
		page_length = int(args.get('page_length'))
		order_by = args.get('order_by')
	
		frappe.db.sql("SET @NEEDYEAR = '0', @SPRACHNR = 4, @LKZ = 'CY';")  # Set the variables
		
		data = frappe.db.sql(f"""
			SELECT distinct
				T100.HERNR AS `name`,
				GET_LBEZNR(T100.LBEZNR, @SPRACHNR) AS lbeznr,
				T100.PKW as pkw,
				T100.NKW as nkw,
				T100.TRANSPORTER as transporter,
				T100.ACHSE as achse,
				T100.MOTOR as motor,
				T100.GETRIEBE as getriebe
			FROM `110` AS `tabTD Vehicle`
				JOIN `100` AS T100 ON T100.HERNR = `tabTD Vehicle`.HERNR
			WHERE 1
				AND (CASE
						WHEN @NEEDYEAR = 0 OR LENGTH(@NEEDYEAR) <> 4 THEN 1
						WHEN `tabTD Vehicle`.BJVON <= CAST(CONCAT(@NEEDYEAR,'01') AS UNSIGNED) AND IFNULL(`tabTD Vehicle`.BJBIS, CAST(CONCAT(YEAR(NOW()),'12') AS UNSIGNED)) >= CAST(CONCAT(@NEEDYEAR,'01') AS UNSIGNED) THEN 1
						ELSE 0
					END) = 1
			ORDER BY {order_by}
        	LIMIT %s, %s;
		""", (start, page_length), as_dict=1)

		return data

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass

