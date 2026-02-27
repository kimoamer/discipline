# Disciplinary Management App

A Frappe HR add-on for managing workplace discipline with a **restorative justice** approach. It tracks offences and occurrences automatically, calculates recommended penalties, integrates with payroll for deductions, and provides structured paths for grievances, investigations, appeals, mediation, and performance improvement plans.

## System Flow

```text
Disciplinary Grievance ──┐
(employee-filed report)  │
                         ├──► Disciplinary Investigation
                         │    (fact-finding & evidence)
Disciplinary Incident ───┘
(formal offence record)
        │
        ├──► Disciplinary Appeal       (challenge the decision)
        ├──► Performance Improvement   (corrective action plan)
        │    Plan (PIP)
        └──► Restorative Mediation     (relationship repair)
```

**Key relationships:**

- **Incident** is the central record. Investigations, Appeals, PIPs, and Mediations all link back to it.
- **Grievance** is the employee-initiated entry point. Investigations and Mediations can also link to a Grievance.
- **Offence** defines the penalty matrix. Incidents reference an Offence to auto-calculate occurrence levels and recommended penalties.

---

## Prerequisites

1. **Frappe HR (HRMS)** installed and configured.
2. Employees, Company, and Department structures set up.
3. At least one **Salary Component** of type *Deduction* configured (for payroll integration).

---

## 1. Discipline Settings

Search for **Discipline Settings** in the Awesome Bar.

### General Section

| Field | Description |
|---|---|
| **Occurrence Window (Months)** | How far back to look when counting repeat offences (default: 12). |
| **Max Occurrence Level** | Maximum escalation level before the count stops increasing (default: 5). |
| **Block Duplicates Same Day** | Prevents recording the same offence for the same employee on the same day. |

### Payroll Integration Section

| Field | Description |
|---|---|
| **Enable Payroll Integration** | Auto-create an Additional Salary (deduction) when an incident is submitted. |
| **Default Deduction Salary Component** | The Salary Component used for deductions (filtered to Deduction type only). Required when payroll integration is enabled. |
| **Require Payroll Period Selection** | Force users to pick a Payroll Period on the incident instead of using the incident date. |

---

## 2. Offences & Penalties

### Creating an Offence

Search for **Offence** and click **Add Offence**.

| Field | Description |
|---|---|
| **Title** | Name of the offence (e.g. "Late Arrival"). Must be unique. |
| **Category** | Severity: Minor, Major, or Critical. |
| **Company** | (Optional) Restrict this offence to a specific company. |
| **Is Active** | Only active offences appear in incident forms. |
| **Max Occurrence Level** | Per-offence override for the global max level from settings. |
| **On Max Exceeded** | Controls what happens when the employee exceeds the max occurrence level. **Apply Last Penalty** (default): keeps applying the highest-level penalty on every subsequent incident. **Block New Incidents**: prevents recording any further incidents for this offence/employee combination. Only visible when Max Occurrence Level is set. |

### Penalty Matrix (child table)

Define what happens at each occurrence level:

| Field | Description |
|---|---|
| **Occurrence No** | The escalation level (1 = first time, 2 = second, etc.). |
| **Penalty Text** | Description (e.g. "Verbal Warning", "Written Warning", "Termination"). |
| **Days Deducted** | Number of pay-days to deduct. Leave at 0 for non-monetary penalties. |
| **Salary Component Override** | Use a different Salary Component for this specific penalty (filtered to Deduction type). |
| **Notes** | Internal HR notes. |

---

## 3. Disciplinary Incident

The core transactional document. It is **submittable** (Draft → Submitted → Cancelled).

### Creating an Incident

| Section | Field | Description |
|---|---|---|
| **Employee Details** | Employee | The offending employee (required). |
| | Employee Name, Company, Department, Designation | Auto-fetched from the Employee record (read-only). |
| **Incident Details** | Offence | Select from active offences (filtered by `is_active = 1`). |
| | Offence Category | Auto-fetched from the Offence (read-only). |
| | Incident Date | When the offence occurred (required). |
| | Reported By | The employee who reported it (filtered to active employees). |
| **Description & Evidence** | Details | Free-text description. |
| | Attachments | Upload supporting evidence. |

### Computed Recommendation (auto-filled)

When Employee + Offence + Incident Date are set, the system calls the backend to:

1. Count prior **submitted** incidents for the same employee + offence within the occurrence window.
2. Look up the matching row in the offence's penalty matrix.
3. Populate: **Occurrence No**, **Recommended Penalty**, **Recommended Days Deducted**, **Recommended Salary Component**.

### Final Decision

HR/Management can accept the recommendation (auto-copied) or override it:

- **Final Penalty** — adjust the penalty text.
- **Final Days Deducted** — increase or decrease the deduction.
- **Final Salary Component** — use a different component.

### Submission & Payroll

1. **Save** → Draft.
2. **Submit** → locks the record.
   - If payroll integration is enabled and Final Days Deducted > 0 with a Final Salary Component, an **Additional Salary** document is auto-created.
   - The link appears in the **Payroll Integration** section.
   - **Payroll Period** can be selected to control which pay cycle the deduction falls in (filtered by company).
3. **Cancel** → auto-cancels the linked Additional Salary.
4. **Amend** → creates a corrected copy.

### Duplicate Check

If **Block Duplicates Same Day** is enabled in settings, the system prevents saving a second incident for the same employee + offence + date.

### Dashboard

From an Incident, the sidebar shows linked:
- Disciplinary Investigations
- Restorative Mediations
- Disciplinary Appeals
- Performance Improvement Plans

---

## 4. Disciplinary Grievance

An employee-initiated report. Not submittable — uses a status workflow instead.

| Section | Field | Description |
|---|---|---|
| **Filed By** | Employee / Employee Name | The employee filing the grievance. Company and Department auto-fetched. |
| **Grievance Details** | Grievance Date | When the grievance is filed (required). |
| | Status | Open → Investigating → Closed / Escalated. |
| | Against Employee | The employee the grievance is against (filtered to exclude the filer). |
| **Description** | Description | Rich-text description of the grievance (required). |

### Validations
- The filing employee and the accused employee cannot be the same person.

### Dashboard
From a Grievance, the sidebar shows linked Investigations and Mediations.

---

## 5. Disciplinary Investigation

Objective fact-finding linked to an Incident and/or Grievance.

| Section | Field | Description |
|---|---|---|
| **Reference** | Disciplinary Incident | Link to a submitted incident (filtered by `docstatus = 1`). |
| | Disciplinary Grievance | Link to an open/investigating grievance (filtered by `status != Closed`). |
| **Employee Details** | Employee / Employee Name | The employee being investigated. Auto-fetched when selecting an incident or grievance. Company and Department auto-fetched. |
| **Investigation Details** | Investigation Date | Required. |
| | Status | Ongoing → Completed. |
| | Investigator / Investigator Name | The employee conducting the investigation (filtered to active employees). |
| **Findings** | Findings | Rich-text editor for evidence and observations. |
| **Conclusion** | Conclusion | Rich-text editor for the investigator's conclusion. |

### Validations
- At least one reference (Incident or Grievance) must be provided.
- The employee must match the employee on the referenced Incident or Grievance.

---

## 6. Disciplinary Appeal

Allows an employee to formally challenge an incident decision. **Submittable.**

| Section | Field | Description |
|---|---|---|
| **Reference** | Disciplinary Incident | Link to a submitted incident (required, filtered by `docstatus = 1`). |
| | Employee / Employee Name | Auto-fetched from the incident (read-only). |
| **Employee Details** | Company, Department | Auto-fetched (collapsible). |
| **Appeal Information** | Date of Appeal | Defaults to today (required). |
| | Status | Pending → Upheld / Overturned / Modified. |
| | Reviewer / Reviewer Name | The employee reviewing the appeal (filtered to active employees). |
| **Appeal Details** | Appeal Reason | Free-text justification (required). |
| **Decision** | Final Decision Notes | Required when status is Upheld, Overturned, or Modified. |

### Validations
- Employee must match the incident's employee.
- Final Decision Notes are mandatory when the appeal status changes from Pending.

---

## 7. Performance Improvement Plan (PIP)

A structured corrective action plan tied to an incident. **Submittable.**

| Section | Field | Description |
|---|---|---|
| **Reference** | Disciplinary Incident | Link to a submitted incident (filtered by `docstatus = 1`). |
| | Employee / Employee Name | Auto-fetched from the incident. |
| **Employee Details** | Company, Department, Designation | Auto-fetched (collapsible). |
| **Plan Details** | Manager / Manager Name | Supervising manager (filtered to active employees). |
| | Status | Draft → Active → Successful / Failed. |
| | Start Date / End Date | Plan duration (both required). |
| **Goals** | Goals table (child: PIP Goal) | Each goal has: Objective (required), Metric, Target Date, Status (Pending / In Progress / Met / Not Met). |

### Validations
- End Date must be after Start Date.
- Employee must match the incident's employee (when an incident is linked).

---

## 8. Restorative Mediation

A structured path for conflict resolution focusing on relationship repair rather than punishment.

| Section | Field | Description |
|---|---|---|
| **Reference** | Disciplinary Incident | Link to a submitted incident. |
| | Disciplinary Grievance | Link to a grievance (filtered by `status != Closed`). |
| | Company | Auto-fetched from the incident. |
| **Parties** | Party 1 / Party 1 Name | First employee (filtered to active). |
| | Party 2 / Party 2 Name | Second employee (filtered to active, excludes Party 1). |
| **Mediation Details** | Mediation Date | Required. |
| | Status | Scheduled → Completed / Failed. |
| | Mediator / Mediator Name | The neutral facilitator (filtered to active employees). |
| | Follow Up Date | Must be after the mediation date. |
| **Mediation Summary** | Summary | Rich-text record of the session. |
| **Agreements Reached** | Agreements | Rich-text record of what was agreed upon. |

### Validations
- Party 1 and Party 2 cannot be the same employee.
- The Mediator cannot be either party.
- Follow Up Date must be after the Mediation Date.

---

## 9. Reports

### Disciplinary Consistency Report

Compares **recommended** vs **final** penalties across submitted incidents. Useful for auditing whether managers are consistently applying the penalty matrix.

**Filters:** Company, Date Range, Offence, Employee.

**Chart:** Bar chart showing the variation (Final − Recommended days) per incident.

---

## 10. Permissions & Workflows

Use standard Frappe tools:

- **Role Permissions Manager** — control who can Create, Read, Write, Submit, Cancel each doctype. For example, give Supervisors Create access to Incidents but restrict Submit to HR Managers.
- **Workflow Builder** — enforce multi-step approval flows (e.g. Draft → Supervisor Review → HR Approval → Submitted).

All doctypes currently grant full access to the **System Manager** role. Add HR Manager, HR User, or custom roles as needed.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| **Payroll deduction amount is 0** | Ensure the employee has an active Salary Structure Assignment with a base salary. The system divides base by 30 for the daily rate. |
| **Occurrence not escalating** | Verify prior incidents are **Submitted** (drafts don't count). Check that the Occurrence Window in settings is wide enough. |
| **Duplicate blocked error** | The same employee + offence + date already exists. Disable "Block Duplicates Same Day" in settings if this is intentional. |
| **Employee mismatch error** | When creating an Appeal, PIP, or Investigation, the employee must match the one on the linked Incident. Select the Incident first and the employee will auto-fill. |
| **Offence not appearing** | Check that the Offence has `Is Active` checked. Only active offences appear in the Incident form. |
