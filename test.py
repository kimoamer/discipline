import frappe
frappe.init(site='site.local')
frappe.connect()
print(frappe.db.exists('DocType', 'Employee'))
