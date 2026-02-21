import frappe

def create_doctypes():
    frappe.flags.in_install = True
    frappe.flags.in_patch = True

    module = "Discipline"
    
    # Ensure module exists (should be created by new-app but let's be safe)
    if not frappe.db.exists("Module Def", module):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": module,
            "app_name": "discipline"
        }).insert(ignore_permissions=True)

    # 1. Discipline Settings
    if not frappe.db.exists("DocType", "Discipline Settings"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Discipline Settings",
            "module": module,
            "custom": 0,
            "issingle": 1,
            "fields": [
                {"fieldname": "enable_payroll_integration", "fieldtype": "Check", "label": "Enable Payroll Integration", "default": "1"},
                {"fieldname": "occurrence_window_months", "fieldtype": "Int", "label": "Occurrence Window (Months)", "default": "12"},
                {"fieldname": "max_occurrence_level", "fieldtype": "Int", "label": "Max Occurrence Level", "default": "5"},
                {"fieldname": "default_deduction_salary_component", "fieldtype": "Link", "options": "Salary Component", "label": "Default Deduction Salary Component"},
                {"fieldname": "require_payroll_period_selection", "fieldtype": "Check", "label": "Require Payroll Period Selection", "default": "0"},
                {"fieldname": "block_duplicates_same_day", "fieldtype": "Check", "label": "Block Duplicates Same Day", "default": "1"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)

    # 2. Offence Penalty (Child Table)
    if not frappe.db.exists("DocType", "Offence Penalty"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Offence Penalty",
            "module": module,
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "occurrence_no", "fieldtype": "Int", "label": "Occurrence No", "reqd": 1},
                {"fieldname": "penalty_text", "fieldtype": "Small Text", "label": "Penalty Text"},
                {"fieldname": "days_deducted", "fieldtype": "Float", "label": "Days Deducted"},
                {"fieldname": "salary_component", "fieldtype": "Link", "options": "Salary Component", "label": "Salary Component Override"},
                {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"}
            ]
        })
        doc.insert(ignore_permissions=True)
        
    # 3. Offence
    if not frappe.db.exists("DocType", "Offence"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Offence",
            "module": module,
            "custom": 0,
            "autoname": "field:title",
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Title", "reqd": 1, "unique": 1},
                {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "\nMinor\nMajor\nCritical"},
                {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company"},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1"},
                {"fieldname": "penalties", "fieldtype": "Table", "options": "Offence Penalty", "label": "Penalties"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)

    # 4. Disciplinary Incident
    if not frappe.db.exists("DocType", "Disciplinary Incident"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Disciplinary Incident",
            "module": module,
            "custom": 0,
            "autoname": "HR-INC-.YYYY.-.#####",
            "is_submittable": 1,
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company", "fetch_from": "employee.company"},
                {"fieldname": "offence", "fieldtype": "Link", "options": "Offence", "label": "Offence", "reqd": 1, "in_list_view": 1},
                {"fieldname": "incident_date", "fieldtype": "Date", "label": "Incident Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "details", "fieldtype": "Text", "label": "Details"},
                {"fieldname": "attachments", "fieldtype": "Attach", "label": "Attachments"},
                {"fieldname": "sb_computed", "fieldtype": "Section Break", "label": "Computed Information"},
                {"fieldname": "occurrence_no", "fieldtype": "Int", "label": "Occurrence No", "read_only": 1},
                {"fieldname": "recommended_penalty_text", "fieldtype": "Small Text", "label": "Recommended Penalty Text", "read_only": 1},
                {"fieldname": "recommended_days_deducted", "fieldtype": "Float", "label": "Recommended Days Deducted", "read_only": 1},
                {"fieldname": "recommended_salary_component", "fieldtype": "Link", "options": "Salary Component", "label": "Recommended Salary Component", "read_only": 1},
                {"fieldname": "sb_final", "fieldtype": "Section Break", "label": "Final Decision"},
                {"fieldname": "final_penalty_text", "fieldtype": "Small Text", "label": "Final Penalty Text"},
                {"fieldname": "final_days_deducted", "fieldtype": "Float", "label": "Final Days Deducted"},
                {"fieldname": "final_salary_component", "fieldtype": "Link", "options": "Salary Component", "label": "Final Salary Component"},
                {"fieldname": "sb_integration", "fieldtype": "Section Break", "label": "Integration"},
                {"fieldname": "additional_salary_ref", "fieldtype": "Link", "options": "Additional Salary", "label": "Additional Salary Ref", "read_only": 1},
                {"fieldname": "payroll_period", "fieldtype": "Link", "options": "Payroll Period", "label": "Payroll Period"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1}
            ]
        })
        doc.insert(ignore_permissions=True)

    frappe.db.commit()
    print("DocTypes created successfully.")
