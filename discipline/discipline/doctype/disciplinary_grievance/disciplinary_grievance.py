import frappe
from frappe.model.document import Document


class DisciplinaryGrievance(Document):
    def validate(self):
        self.validate_parties()

    def validate_parties(self):
        if self.against_employee and self.against_employee == self.employee:
            frappe.throw("The grievance cannot be filed against the same employee who is filing it.")
