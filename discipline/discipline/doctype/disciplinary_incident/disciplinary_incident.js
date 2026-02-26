// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Disciplinary Incident", {
    employee: function (frm) {
        get_recommendation(frm);
    },
    offence: function (frm) {
        get_recommendation(frm);
    },
    incident_date: function (frm) {
        get_recommendation(frm);
    },
    setup: function (frm) {
        frm.set_query("recommended_salary_component", function () {
            return {
                filters: {
                    type: "Deduction"
                }
            };
        });
        frm.set_query("final_salary_component", function () {
            return {
                filters: {
                    type: "Deduction"
                }
            };
        });
    }
});

function get_recommendation(frm) {
    if (frm.doc.employee && frm.doc.offence && frm.doc.incident_date) {
        frappe.call({
            method: "discipline.discipline.doctype.disciplinary_incident.disciplinary_incident.get_recommendation",
            args: {
                employee: frm.doc.employee,
                offence: frm.doc.offence,
                incident_date: frm.doc.incident_date,
                docname: frm.doc.name !== undefined && frm.doc.__islocal ? null : frm.doc.name
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(frm.doctype, frm.docname, "occurrence_no", r.message.occurrence_no);
                    frappe.model.set_value(frm.doctype, frm.docname, "recommended_penalty_text", r.message.recommended_penalty_text);
                    frappe.model.set_value(frm.doctype, frm.docname, "recommended_days_deducted", r.message.recommended_days_deducted);
                    frappe.model.set_value(frm.doctype, frm.docname, "recommended_salary_component", r.message.recommended_salary_component);

                    // Also set final if they are empty
                    if (!frm.doc.final_penalty_text) {
                        frappe.model.set_value(frm.doctype, frm.docname, "final_penalty_text", r.message.recommended_penalty_text);
                    }
                    if (!frm.doc.final_days_deducted) {
                        frappe.model.set_value(frm.doctype, frm.docname, "final_days_deducted", r.message.recommended_days_deducted);
                    }
                    if (!frm.doc.final_salary_component) {
                        frappe.model.set_value(frm.doctype, frm.docname, "final_salary_component", r.message.recommended_salary_component);
                    }
                }
            }
        });
    }
}
