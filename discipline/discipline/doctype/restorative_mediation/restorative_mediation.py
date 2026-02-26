import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class RestorativeMediation(Document):
    def validate(self):
        self.validate_parties()
        self.validate_dates()

    def validate_parties(self):
        if self.party_1 and self.party_2 and self.party_1 == self.party_2:
            frappe.throw("Party 1 and Party 2 cannot be the same employee.")
        if self.mediator:
            if self.mediator == self.party_1 or self.mediator == self.party_2:
                frappe.throw("The Mediator cannot be one of the parties in the mediation.")

    def validate_dates(self):
        if self.date and self.follow_up_date:
            if getdate(self.follow_up_date) <= getdate(self.date):
                frappe.throw("Follow Up Date must be after the Mediation Date.")
