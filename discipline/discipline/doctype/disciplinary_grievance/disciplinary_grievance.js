// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Disciplinary Grievance", {
    setup: function (frm) {
        frm.set_query("against_employee", function () {
            let filters = { status: "Active" };
            if (frm.doc.employee) {
                filters.name = ["!=", frm.doc.employee];
            }
            return { filters: filters };
        });
    }
});
