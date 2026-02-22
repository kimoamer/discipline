// Copyright (c) 2026, RootRise and contributors
// For license information, please see license.txt

frappe.ui.form.on("Discipline Settings", {
    setup: function (frm) {
        frm.set_query("default_deduction_salary_component", function () {
            return {
                filters: {
                    type: "Deduction"
                }
            };
        });
    }
});
