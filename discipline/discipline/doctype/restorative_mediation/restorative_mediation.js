// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Restorative Mediation", {
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
        frm.set_query("mediator", function () {
            return {
                filters: { status: "Active" }
            };
        });
        frm.set_query("party_1", function () {
            return {
                filters: { status: "Active" }
            };
        });
        frm.set_query("party_2", function () {
            let filters = { status: "Active" };
            if (frm.doc.party_1) {
                filters.name = ["!=", frm.doc.party_1];
            }
            return { filters: filters };
        });
    },
    incident_ref: function (frm) {
        if (frm.doc.incident_ref) {
            frappe.db.get_value("Disciplinary Incident", frm.doc.incident_ref, "employee", function (r) {
                if (r && r.employee && !frm.doc.party_1) {
                    frm.set_value("party_1", r.employee);
                }
            });
        }
    }
});
