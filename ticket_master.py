import frappe
from frappe import get_doc

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] == "System User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)
    products = frappe.db.sql(""" SELECT * FROM `tabOperator Product`;""", as_dict=True)
    username = get_doc("User", frappe.session.user)
    context.username = username.full_name
    context.products = products