# Disciplinary Management App - User Manual

Welcome to the Disciplinary Management App! This app integrates natively with Frappe HR (HRMS) to help manage company policy violations, track offense occurrences automatically, and apply calculated penalties (including payroll deductions). 

## 🌟 The New Vision: Restorative Justice & Due Process

Modern HR practices have evolved beyond purely reactive and punitive measures. This app has been explicitly leveled-up to implement a **Restorative Justice and Comprehensive Due Process** model. We believe in transparency, employee voice, and relationship repair.

To achieve this, the app now separates investigations from penalties and allows for alternative resolutions:
1. **Disciplinary Grievance**: Proactive reporting where employees have a formal voice.
2. **Disciplinary Investigation**: Objective fact-finding and evidence logging detached from final actions to ensure legal due process.
3. **Disciplinary Incident**: The formal record of an offense and penalty (if applicable).
4. **Restorative Mediation**: A structured approach to conflict resolution focusing on healing relationships rather than merely issuing deductions.

### System Flow
```text
  +-------------------------+
  | Incident Submitted      |
  +-----------+-------------+
              |
              v
  +-------------------------+
  | Employee Acknowledgment |
  +-----------+-------------+
              |
              v
  +-------------------------+
  | Appeal                  |
  | (if employee disagrees) |
  +-----------+-------------+
              |
              v
  +-------------------------+
  | HR Review               |
  +-----------+-------------+
              |
              v
  +-------------------------+
  | Final Decision          |
  +-------------------------+
```

This guide will walk you through setting up and using the app under this modern paradigm.

## Prerequisites

Before using the Disciplinary Management app, ensure the following:
1. **Frappe HR (HRMS)** is installed and configured on your site.
2. Employees and Company structures are correctly set up.
3. Salary Components are defined (specifically, setting up a Salary Component for deductions).

---

## 1. Initial Setup

### Step 1: Configure Discipline Settings
1. In the search bar at the top, type **Discipline Settings** and press Enter.
2. Fill out the configuration options:
   - **Enable Payroll Integration**: Check this box if you want the app to automatically create an **Additional Salary** (deduction) document when a monetary penalty is issued.
   - **Occurrence Window (Months)**: Enter the number of months to look back for repeat offenses. For example, `12` means the system will calculate occurrence levels (1st, 2nd, etc.) based on the past year.
   - **Max Occurrence Level**: Set the maximum escalation level (usually 5).
   - **Default Deduction Salary Component**: Select the default HRMS Salary Component to use when deducting pay for penalties. (This should be an "Earning/Deduction" component configured as a deduction in HRMS).
   - **Require Payroll Period Selection**: Check this to force users to manually select a payroll period instead of deriving it from the incident date.
   - **Block Duplicates Same Day**: Prevents the creation of two identical incidents for the same employee and the same offense on the same day.
3. **Save** the settings.

---

## 2. Defining Offences & Penalties

You must set up the rules and penalty structures for your organization.

### Step 1: Create an Offence
1. In the search bar, type **Offence List** and press Enter.
2. Click **Add Offence**.
3. Fill out the basic details:
   - **Title**: E.g., "Late Arrival".
   - **Category**: Select the severity level (e.g., Minor, Major, Critical).
   - **Company**: (Optional) Assign this rule to a specific company if managing multiple companies.
   - **Is Active**: Ensure this is checked.

### Step 2: Define the Penalty Matrix
In the lower section of the Offence form, fill out the **Penalties** table to define what happens at each occurrence level:
1. **Occurrence No**: Enter the level (1 for first occurrence, 2 for second time, etc.).
2. **Penalty Text**: Enter a written warning or note (e.g., "Verbal Warning", "Written Warning").
3. **Days Deducted**: Enter the number of days of pay to deduct. Leave as `0` for warnings without pay cuts.
4. **Salary Component Override**: (Optional) Provide a specific Salary Component for this precise penalty if it differs from the default set in *Discipline Settings*.
5. **Notes**: Add any internal HR notes.

Click **Save** when all levels are defined.

---

## 3. Recording a Disciplinary Incident

When an employee commits an offense, supervisors or HR personnel will record it here.

### Step 1: Create the Incident
1. Search for **Disciplinary Incident List** and click **Add Disciplinary Incident**.
2. Fill in the core details:
   - **Employee**: Select the employee from the list.
   - **Offence**: Select the offense they committed (e.g., "Late Arrival").
   - **Incident Date**: The exact date the offense occurred.
   - **Details/Attachments**: Add a description of the event or attach necessary proofs.

### Step 2: Review Recommendations
Once you select the Employee, Offence, and Date, the system automatically checks their history and fills out the **Computed Information** section:
- **Occurrence No**: Auto-calculated based on past incidents within the window.
- **Recommended Penalty**: Auto-pulled from the Offence matrix.
- **Recommended Days Deducted & Salary Component**: Displays the suggested payroll action.

### Step 3: Final Decision
Under the **Final Decision** section, HR/Management can adjust the recommendation if necessary. By default, the system will copy the recommended values into the final fields upon saving.
- If you wish to give a lesser or harsher penalty, manually adjust the `Final Penalty Text` or `Final Days Deducted` fields.

### Step 4: Submission and Payroll Integration
1. **Save** the document. It is now in a Draft state.
2. Click **Submit** to finalize the disciplinary incident. 
   - **Note:** Submitted records are locked and cannot be edited.
3. **Payroll Automation**: If you have *Payroll Integration* enabled and there are `Final Days Deducted` specified, the system will instantly and automatically generate an **Additional Salary** document for that employee based on their base salary rate.
   - An `Additional Salary Ref` link will appear at the bottom of the incident form so you can track the deduction.

### Undoing an Incident
If a submitted incident needs to be revoked:
1. Click **Cancel** on the submitted Disciplinary Incident.
2. The associated **Additional Salary** deduction document will be automatically canceled.

---

## 4. Workflows & Permissions (Optional)

You can use standard Frappe tools to shape the approval process:
- Navigate to **Role Permissions Manager** to restrict who can *Submit* vs who can *Create* incidents. For example, give Supervisors "Create" access but restrict "Submit" to HR Managers.
- Navigate to **Workflow List** if you want to enforce a multi-step approval process (e.g., `Draft` -> `Supervisor Review` -> `HR Approval` -> `Submitted`).

---

## Troubleshooting

- **Payroll Deduction is Rs. 0.00:** Ensure the employee has an active `Salary Structure Assignment`. The system divides the base salary by 30 to calculate the daily deduction rate.
- **Occurrence isn't escalating:** Check your `Discipline Settings` to ensure the `Occurrence Window (Months)` is wide enough, and verify that the previous incidents were formally **Submitted** (Drafts don't count towards the history).
- **Duplicates blocked error:** If an employee genuinely commits the same offense twice in one day, temporarily turn off `Block Duplicates Same Day` in Discipline Settings.
