// Copyright (c) 2026, RootRise and contributors
// For license information, please see license.txt

frappe.ui.form.on("Offence", {
    setup: function (frm) {
        frm.set_query("salary_component", "penalties", function () {
            return {
                filters: {
                    type: "Deduction"
                }
            };
        });
    }
});
