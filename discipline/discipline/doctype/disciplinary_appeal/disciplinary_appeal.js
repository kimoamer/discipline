// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Disciplinary Appeal", {
    setup: function (frm) {
        frm.set_query("disciplinary_incident", function () {
            return {
                filters: { docstatus: 1 }
            };
        });
        frm.set_query("reviewer", function () {
            return {
                filters: { status: "Active" }
            };
        });
    },
    disciplinary_incident: function (frm) {
        if (frm.doc.disciplinary_incident) {
            frappe.db.get_value("Disciplinary Incident", frm.doc.disciplinary_incident, "employee", function (r) {
                if (r && r.employee) {
                    frm.set_value("employee", r.employee);
                }
            });
        }
    }
});
