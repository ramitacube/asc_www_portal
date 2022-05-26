from ast import operator
import frappe
import frappe.www.list
from frappe import _, get_doc
import datetime

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    if frappe.session["data"]["user_type"] == "System User":
        frappe.throw(_("You don't have access to this page"), frappe.PermissionError)

    email = frappe.session.user
    username = get_doc("User", frappe.session.user)
    customer = get_doc("Customer", username.full_name)
    profile = f"http://sports.asc:8014/{frappe.get_value('File', {'attached_to_name':email},['file_url'])}"
    operator_details = get_doc("Operator", username.full_name)
    context.userData = frappe.session
    context.username = username.full_name
    context.address = customer.primary_address
    context.ATOAI_member = operator_details.atoai_member
    context.ministry_of_tourism = operator_details.registered_with_ministry_of_tourism
    context.registered_with_state_tourism = operator_details.registered_with_state_tourism
    context.birth_date = username.birth_date.strftime("%d-%m-%Y")
    context.gender = username.gender
    context.pro_pic = profile