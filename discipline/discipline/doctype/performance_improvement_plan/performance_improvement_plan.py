import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class PerformanceImprovementPlan(Document):
    def validate(self):
        self.validate_dates()
        self.validate_employee_matches_incident()

    def validate_dates(self):
        if self.start_date and self.end_date:
            if getdate(self.end_date) <= getdate(self.start_date):
                frappe.throw("End Date must be after Start Date.")

    def validate_employee_matches_incident(self):
        if self.disciplinary_incident:
            inc_employee = frappe.db.get_value(
                "Disciplinary Incident", self.disciplinary_incident, "employee"
            )
            if inc_employee and self.employee != inc_employee:
                frappe.throw(
                    f"Employee {self.employee} does not match the employee "
                    f"{inc_employee} on incident {self.disciplinary_incident}."
                )
