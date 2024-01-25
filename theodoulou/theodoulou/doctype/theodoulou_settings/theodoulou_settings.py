# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TheodoulouSettings(Document):

	def get_language(self):
		language = frappe.db.sql("""
			SELECT 
				SPRACHNR, -- ID LANGUAGE
				ISO_CODE -- ISO CODE
			FROM `020` AS T020
			WHERE `ISO_CODE` LIKE %s;
		""", (self.language), as_dict=True)

		if language:
			return language[0].SPRACHNR
		else:
			frappe.throw("Language not supported")

	def get_country(self):
		# Get country code from doctype Country
		country = frappe.get_doc("Country", self.country)
		return country.code.upper()
