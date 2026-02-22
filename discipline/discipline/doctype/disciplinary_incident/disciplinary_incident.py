import frappe
from frappe.model.document import Document
from frappe.utils import add_months, getdate, flt

class DisciplinaryIncident(Document):
    def validate(self):
        self.check_duplicate()
        self.compute_occurrence_and_recommendation()
    
    def before_submit(self):
        self.compute_occurrence_and_recommendation()
        
        # If final fields are empty, copy from recommended
        if not self.final_penalty_text:
            self.final_penalty_text = self.recommended_penalty_text
        if not self.final_days_deducted and getattr(self, "recommended_days_deducted", 0):
            self.final_days_deducted = self.recommended_days_deducted
        if not self.final_salary_component:
            self.final_salary_component = self.recommended_salary_component

    def on_submit(self):
        settings = frappe.get_doc("Discipline Settings")
        if settings.enable_payroll_integration:
            if self.final_days_deducted and self.final_salary_component:
                self.create_additional_salary()

    def on_cancel(self):
        self.cancel_additional_salary()

    def check_duplicate(self):
        settings = frappe.get_single("Discipline Settings")
        if settings.block_duplicates_same_day:
            existing = frappe.db.get_value("Disciplinary Incident", {
                "employee": self.employee,
                "offence": self.offence,
                "incident_date": self.incident_date,
                "name": ("!=", self.name),
                "docstatus": ("!=", 2)
            })
            if existing:
                frappe.throw(f"A Disciplinary Incident already exists for the same employee and offence on this date ({existing}).")

    def compute_occurrence_and_recommendation(self):
        settings = frappe.get_single("Discipline Settings")
        window_months = settings.occurrence_window_months or 12
        max_level = settings.max_occurrence_level or 5
        
        start_date = add_months(self.incident_date, -window_months)
        
        # Count previous incidents
        count = frappe.db.count("Disciplinary Incident", {
            "employee": self.employee,
            "offence": self.offence,
            "incident_date": ["between", [start_date, self.incident_date]],
            "docstatus": 1,
            "name": ("!=", self.name)
        })
        
        computed_occurrence = min(count + 1, max_level)
        self.occurrence_no = computed_occurrence
        
        if self.offence:
            offence_doc = frappe.get_doc("Offence", self.offence)
            penalty = next((p for p in offence_doc.penalties if p.occurrence_no == computed_occurrence), None)
            
            if penalty:
                self.recommended_penalty_text = penalty.penalty_text
                self.recommended_days_deducted = penalty.days_deducted
                self.recommended_salary_component = penalty.salary_component or settings.default_deduction_salary_component
            else:
                self.recommended_penalty_text = None
                self.recommended_days_deducted = 0
                self.recommended_salary_component = settings.default_deduction_salary_component

    def create_additional_salary(self):
        if self.additional_salary_ref:
            return
            
        amount = 0
        try:
            # Try to get active salary structure assignment to compute daily rate
            assignment = frappe.db.get_value("Salary Structure Assignment", 
                {"employee": self.employee, "docstatus": 1, "is_active": 1}, 
                "base",
                order_by="from_date desc")
            if assignment:
                # rough daily rate
                daily_rate = flt(assignment) / 30.0
                amount = daily_rate * flt(self.final_days_deducted)
        except Exception:
            pass

        try:
            add_sal = frappe.get_doc({
                "doctype": "Additional Salary",
                "employee": self.employee,
                "salary_component": self.final_salary_component,
                "amount": amount,
                "payroll_date": self.incident_date,
                "company": self.company,
                "ref_doctype": "Disciplinary Incident",
                "ref_docname": self.name
            })
            if self.payroll_period:
                add_sal.payroll_period = self.payroll_period
            
            add_sal.insert(ignore_permissions=True)
            add_sal.submit()
            
            self.db_set("additional_salary_ref", add_sal.name)
        except Exception as e:
            frappe.msgprint(f"Could not create payroll deduction. Ensure HRMS is installed natively: {e}")

    def cancel_additional_salary(self):
        if self.additional_salary_ref:
            try:
                add_sal = frappe.get_doc("Additional Salary", self.additional_salary_ref)
                if add_sal.docstatus == 1:
                    add_sal.cancel()
                self.db_set("additional_salary_ref", None)
            except Exception:
                pass

@frappe.whitelist()
def get_recommendation(employee, offence, incident_date, docname=None):
    from frappe.utils import add_months
    if not employee or not offence or not incident_date:
        return {}
    settings = frappe.get_single("Discipline Settings")
    window_months = settings.occurrence_window_months or 12
    max_level = settings.max_occurrence_level or 5
    
    start_date = add_months(incident_date, -window_months)
    
    filters = {
        "employee": employee,
        "offence": offence,
        "incident_date": ["between", [start_date, incident_date]],
        "docstatus": 1
    }
    if docname:
        filters["name"] = ("!=", docname)

    count = frappe.db.count("Disciplinary Incident", filters)
    
    computed_occurrence = min(count + 1, max_level)
    
    offence_doc = frappe.get_doc("Offence", offence)
    penalty = next((p for p in offence_doc.penalties if p.occurrence_no == computed_occurrence), None)
    
    res = {"occurrence_no": computed_occurrence}
    if penalty:
        res["recommended_penalty_text"] = penalty.penalty_text
        res["recommended_days_deducted"] = penalty.days_deducted
        res["recommended_salary_component"] = penalty.salary_component or settings.default_deduction_salary_component
    else:
        res["recommended_penalty_text"] = None
        res["recommended_days_deducted"] = 0
        res["recommended_salary_component"] = settings.default_deduction_salary_component
        
    return res
