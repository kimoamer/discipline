// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Disciplinary Investigation", {
    setup: function (frm) {
        frm.set_query("incident_ref", function () {
            return {
                filters: { docstatus: 1 }
            };
        });
        frm.set_query("grievance_ref", function () {
            return {
                filters: { status: ["!=", "Closed"] }
            };
        });
        frm.set_query("investigator", function () {
            return {
                filters: { status: "Active" }
            };
        });
    },
    incident_ref: function (frm) {
        if (frm.doc.incident_ref) {
            frappe.db.get_value("Disciplinary Incident", frm.doc.incident_ref, "employee", function (r) {
                if (r && r.employee) {
                    frm.set_value("employee", r.employee);
                }
            });
        }
    },
    grievance_ref: function (frm) {
        if (frm.doc.grievance_ref && !frm.doc.employee) {
            frappe.db.get_value("Disciplinary Grievance", frm.doc.grievance_ref, "employee", function (r) {
                if (r && r.employee) {
                    frm.set_value("employee", r.employee);
                }
            });
        }
    }
});
