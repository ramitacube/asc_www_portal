import frappe
from frappe import get_doc

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] == "System User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    username = get_doc("User", frappe.session.user)
    commission_report = get_doc("Commission Report", username.full_name).as_dict()
    context.commission_report = commission_report.commission_report