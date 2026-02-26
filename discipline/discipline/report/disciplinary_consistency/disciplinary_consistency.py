# Copyright (c) 2026, Hak3em and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)

    return columns, data, None, chart

def get_columns():
    return [
        {
            "fieldname": "offence",
            "label": "Offence",
            "fieldtype": "Link",
            "options": "Offence",
            "width": 150
        },
        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },
        {
            "fieldname": "employee_name",
            "label": "Employee Name",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "fieldname": "incident_date",
            "label": "Incident Date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "fieldname": "occurrence_no",
            "label": "Occurrence No",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "recommended_days_deducted",
            "label": "Recommended Days Deducted",
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "final_days_deducted",
            "label": "Final Days Deducted",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "fieldname": "difference",
            "label": "Difference (Final - Rec)",
            "fieldtype": "Float",
            "width": 180
        },
        {
            "fieldname": "name",
            "label": "Disciplinary Incident",
            "fieldtype": "Link",
            "options": "Disciplinary Incident",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql(f"""
        SELECT
            di.name,
            di.employee,
            e.employee_name,
            di.offence,
            di.incident_date,
            di.occurrence_no,
            di.recommended_days_deducted,
            di.final_days_deducted,
            (di.final_days_deducted - di.recommended_days_deducted) as difference
        FROM
            `tabDisciplinary Incident` di
        LEFT JOIN `tabEmployee` e ON di.employee = e.name
        WHERE
            di.docstatus = 1
            {conditions}
        ORDER BY
            di.incident_date desc, di.offence
    """, filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = []
    
    if filters.get("company"):
        conditions.append("AND di.company = %(company)s")
    if filters.get("employee"):
        conditions.append("AND di.employee = %(employee)s")
    if filters.get("offence"):
        conditions.append("AND di.offence = %(offence)s")
    if filters.get("from_date"):
        conditions.append("AND di.incident_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("AND di.incident_date <= %(to_date)s")
        
    return " ".join(conditions)

def get_chart(data):
    if not data:
        return None
        
    labels = []
    differences = []
    
    for row in data:
        name = row.get("name")
        diff = row.get("difference", 0)
        
        labels.append(name)
        differences.append(diff)
        
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Variation from Recommendation (Days)",
                    "values": differences
                }
            ]
        },
        "type": "bar",
        "colors": ["#fc4f4f"]
    }
    
    return chart
