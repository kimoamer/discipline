import frappe
from frappe.model.document import Document


class DisciplinaryInvestigation(Document):
    def validate(self):
        self.validate_reference()
        self.validate_employee_matches_reference()

    def validate_reference(self):
        if not self.incident_ref and not self.grievance_ref:
            frappe.throw("At least one of Disciplinary Incident or Disciplinary Grievance must be linked.")

    def validate_employee_matches_reference(self):
        if self.incident_ref:
            inc_employee = frappe.db.get_value("Disciplinary Incident", self.incident_ref, "employee")
            if inc_employee and self.employee != inc_employee:
                frappe.throw(
                    f"Employee {self.employee} does not match the employee "
                    f"{inc_employee} on incident {self.incident_ref}."
                )
        if self.grievance_ref:
            grv_employee = frappe.db.get_value("Disciplinary Grievance", self.grievance_ref, "employee")
            if grv_employee and self.employee != grv_employee:
                frappe.throw(
                    f"Employee {self.employee} does not match the employee "
                    f"{grv_employee} on grievance {self.grievance_ref}."
                )
