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
    policy_issued = frappe.db.sql(""" SELECT * FROM `tabIssue Policy`; """, as_dict=True)
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
    context.policy_issue = policy_issued

    number_of_policy = 0
    for pol in policy_issued:
        if pol.operator==username.full_name:
            number_of_policy += 1
    context.no_issue = number_of_policy
    
    total_issuance_amount = 0
    for issued in policy_issued:
        if issued.operator==username.full_name:
            total_issuance_amount += issued.grand_total
    context.total_issuance_amount = total_issuance_amount

    operator_commission_amount = 0
    for commission in policy_issued:
        if commission.operator==username.full_name:
            operator_commission_amount += commission.operator_commission_received
    context.operator_commission_amount = operator_commission_amount