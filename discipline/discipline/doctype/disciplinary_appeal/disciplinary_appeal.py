import frappe
from frappe.model.document import Document


class DisciplinaryAppeal(Document):
    def validate(self):
        self.validate_employee_matches_incident()
        self.validate_decision()

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

    def validate_decision(self):
        if self.status in ("Upheld", "Overturned", "Modified") and not self.final_decision_notes:
            frappe.throw("Final Decision Notes are required when the appeal status is set to "
                         f"{self.status}.")
