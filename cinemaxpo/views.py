from django.shortcuts import render
import json
from cinemaxpr.models import PurchaseRequisitionDetail, PurchaseRequisitionLineDetail, PurchaseOrderDetail, PurchaseOrderLineDetail, LineOfApproval, LineOfApprovalDetail, ExtendedUser, ApprovalStatus, TransactionDetail
from cinemax.enums import Status
from .viewmodels import purchase_order_vm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .render import Render
from xhtml2pdf import pisa
from io import StringIO
import os
from django.template.loader import get_template
from django.template import Context
import pdfkit
import pydf

# Create your views here.


def dashboard(request):
    # Fetch All PR with approved status
    approved_pr = PurchaseRequisitionDetail.objects.filter(
        status_id=Status.APPROVED.value)
    transactions = TransactionDetail.objects.filter(
        transactionstatus=Status.PENDING.value, entity_type_id=2, extendeduserObj=request.user.id).select_related()
    purchaseorders = PurchaseOrderDetail.objects.all()
    purchase_order_vm_list = []
    for item in purchaseorders:
        foruser = ""
        pending_transaction = TransactionDetail.objects.filter(
            entity_type_id=2, purchaseOrderDetail_id=item.id, transactionstatus=1)

        if pending_transaction.count() > 0:
            user = ExtendedUser.objects.get(user_id=pending_transaction[0].extendeduserObj)
            print(user.role_id)
            foruser = user.role.name

        purchase_order_vm_list.append(purchase_order_vm(
            item.id, item.title, item.status, item.created_by, item.purchaseRequisitionDetail, foruser))

    return render(request, 'purchaseorder/dashboard.htm', {'view': 'purchaseorderdash', 'title': 'Dashboard', 'approved_pr': approved_pr, 'transactions': transactions, 'purchaseorders': purchase_order_vm_list})


def purchaseorder(request):
    purchaseorders = PurchaseOrderDetail.objects.all()
    purchase_order_vm_list = []
    for item in purchaseorders:
        foruser = ""
        pending_transaction = TransactionDetail.objects.filter(
            entity_type_id=2, purchaseOrderDetail_id=item.id, transactionstatus=1)

        if pending_transaction.count() > 0:
            user = ExtendedUser.objects.get(user_id=pending_transaction[0].extendeduserObj)
            print(user.role_id)
            foruser = user.role.name

        purchase_order_vm_list.append(purchase_order_vm(
            item.id, item.title, item.status, item.created_by, item.purchaseRequisitionDetail, foruser))
    return render(request, 'purchaseorder/list.htm', {'view': 'purchaseorder', 'title': 'Purchase Order', 'purchaseorders': purchase_order_vm_list})


def editpurchaseorder(request, id, poid):
    # Fetch all PR
    purchaserequisitions = PurchaseRequisitionDetail.objects.all()

    if poid > 0 and id > 0:
        purchaseorder = PurchaseOrderDetail.objects.get(id=poid)
        purchaseorderitems = PurchaseOrderLineDetail.objects.filter(purchaseOrderDetail_id=poid)
        # Get PR reference
        purchaserequisition = PurchaseRequisitionDetail.objects.get(id=id)
        # Get PR Line Items
        lineItems = PurchaseRequisitionLineDetail.objects.filter(
            purchaseRequisitionDetail_id=id)
        return render(request, 'purchaseorder/editpurchaseorder.htm', {'view': 'purchaseorder', 'title': 'Purchase Order','purchaserequisition': purchaserequisition, 'purchaserequisitions': purchaserequisitions, 'lineItems': lineItems, 'purchaseorder': purchaseorder, 'purchaseorderitems': purchaseorderitems})

    if id > 0:
        # Get PR reference
        purchaserequisition = PurchaseRequisitionDetail.objects.get(id=id)
        # Get PR Line Items
        lineItems = PurchaseRequisitionLineDetail.objects.filter(
            purchaseRequisitionDetail_id=id)
        return render(request, 'purchaseorder/editpurchaseorder.htm', {'view': 'purchaseorder', 'title': 'Purchase Order','purchaserequisition': purchaserequisition, 'purchaserequisitions': purchaserequisitions, 'lineItems': lineItems})

    if request.method == "POST":
        purchaseorder_line_data = json.loads(request.POST['lineitems'])
        print(purchaseorder_line_data)
        purchaseorder = PurchaseOrderDetail(
            title=request.POST['title'],
            purchaseRequisitionDetail_id=request.POST['prid'],
            entity_type_id=2,
            created_by_id=request.user.id,
            status_id=Status.PENDING.value)
        purchaseorder.save()

        # entry for PO line items
        for lineitem in purchaseorder_line_data:
            if lineitem['prlineid'] != "":
                polineitem = PurchaseOrderLineDetail(quantity=lineitem['linequantity'], unit_price=lineitem['lineunitprice'], amount=lineitem[
                                                     'lineamount'], purchaseRequisitionLineDetail_id=lineitem['prlineid'], purchaseOrderDetail_id=purchaseorder.id)
                polineitem.save()

        # get LOA for based on Business Unit
        if(LineOfApproval.objects.filter(businessunit_id=int(request.session['bu_id']), entity_type_id=2).count() > 0):
            lineOfApproval = LineOfApproval.objects.get(
                businessunit_id=int(request.session['bu_id']), entity_type_id=2)
            lineOfApprovalDetail = LineOfApprovalDetail.objects.filter(
                line_of_approval_id=lineOfApproval.id, level=1, entity_type_id=2)

            # from level 1 make entry in transactions table for LOA
            for loaDetail in lineOfApprovalDetail:
                transaction = TransactionDetail(level=loaDetail.level, required_approval=loaDetail.required_approval,
                                                businessunitObj=lineOfApproval.businessunit_id,
                                                lineOfApprovalObj=lineOfApproval.id,
                                                entity_type_id=2,
                                                extendeduserObj=loaDetail.approver_id,
                                                purchaseOrderDetail_id=purchaseorder.id,
                                                transactionstatus=Status.PENDING.value)
                transaction.save()
        else:
            print("NO LOA")
            # If PR does not have LOA then set status to Approved
            purchaseorder.status_id = Status.APPROVED.value
            purchaseorder.save()

    return render(request, 'purchaseorder/editpurchaseorder.htm', {'purchaserequisitions': purchaserequisitions})


def updatePOTransactionStatus(request, tid, isApproved):
    transaction = TransactionDetail.objects.get(id=tid)
    if isApproved == 1:
        transaction.transactionstatus = Status.APPROVED.value
        transaction.save()
    else:
        transaction.transactionstatus = Status.REJECTED.value
        transaction.save()

    if isApproved == 0:
        purchaseorder = PurchaseOrderDetail.objects.get(
            id=transaction.purchaseOrderDetail_id)
        # rejected_transactions = TransactionDetail.objects.filter(
        #     memoObj_id=memo_detail.id, level=transaction.level, transactionstatus=Status.REJECTED.value)

        pending_transactions = TransactionDetail.objects.filter(
            purchaseOrderDetail_id=purchaseorder.id, level=transaction.level, transactionstatus=Status.PENDING.value, entity_type_id=2)

        if pending_transactions.count() >= transaction.required_approval:
            return HttpResponse(json.dumps({'status': "waiting for others"}), content_type="application/json")
        else:
            po = PurchaseOrderDetail.objects.get(
                id=transaction.purchaseOrderDetail_id)
            po.status_id = Status.REJECTED.value
            po.save()

            extendeduser = ExtendedUser.objects.get(user_id=po.created_by_id)
            subject = 'Purchase Order Rejected'
            message = settings.REJECTED_EMAIL_TEMPLATE.format(
                extendeduser.user.username, po.title)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            send_mail(subject, message, email_from, recipient_list)
            print("REJECTED")
            return HttpResponse(json.dumps({'status': "Rejected"}), content_type="application/json")

        return HttpResponse(json.dumps({'status': "Waitng for others"}), content_type="application/json")

    elif isApproved == 1:
        # check if there are any more pending approvals needs to be approved where must_approve is true
        # Get Transaction in approved status
        po = PurchaseOrderDetail.objects.get(
            id=transaction.purchaseOrderDetail_id)
        approved_transactions = TransactionDetail.objects.filter(
            purchaseOrderDetail_id=po.id,
            level=transaction.level,
            transactionstatus=Status.APPROVED.value,
            entity_type_id=2)

        if approved_transactions.count() < transaction.required_approval:
            print("WAITING FOR OTHERS TO APPROVE")
            return HttpResponse(json.dumps({'status': "WAITING FOR OTHERS TO APPROVE"}), content_type="application/json")

        # Once all approve in the current Level, check if more level of approval is needed
        next_level = transaction.level + 1
        line_of_approval_detail = LineOfApprovalDetail.objects.filter(
            line_of_approval_id=transaction.lineOfApprovalObj, level=next_level, entity_type_id=2)

        if(line_of_approval_detail.count() > 0):
            print("REQUIRE FURTHER LOA LEVEL 2 {}",
                  transaction.lineOfApprovalObj)
            for loa_detail in line_of_approval_detail:
                transaction_detail = TransactionDetail(level=loa_detail.level, required_approval=loa_detail.required_approval,
                                                       extendeduserObj=loa_detail.approver_id,
                                                       lineOfApprovalObj=loa_detail.line_of_approval_id,
                                                       businessunitObj=transaction.businessunitObj,
                                                       purchaseOrderDetail_id=transaction.purchaseOrderDetail_id,
                                                       entity_type_id=2,
                                                       transactionstatus=Status.PENDING.value)
                transaction_detail.save()
        else:
            print("NO MORE LOA LEVEL, SO SET TRANSACTION STATUS TO APPROVED")
            purchaseorder = PurchaseOrderDetail.objects.get(
                id=transaction.purchaseOrderDetail_id)
            purchaseorder.status_id = Status.APPROVED.value
            purchaseorder.save()

            extendeduser = ExtendedUser.objects.get(
                user_id=purchaseorder.created_by_id)

            subject = "Purchase Order Approved By CEO"
            message = settings.APPROVED_EMAIL_TEMPLATE.format(
                extendeduser.user.username, purchaseorder.title)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            print(message, extendeduser.email)
            send_mail(subject, message, email_from, recipient_list)

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def getprdetailbyid(request, id):
    purchaserequisition = PurchaseRequisitionDetail.objects.get(id=id)
    return HttpResponse(json.dumps({'id': purchaserequisition.id, 'title': purchaserequisition.title, 'vendorname': purchaserequisition.vendor_name, 'vendoraccount': purchaserequisition.vendor_account}), content_type="application/json")


def getprlinedetailbyid(request, id):
    lineitem = PurchaseRequisitionLineDetail.objects.get(id=id)
    return HttpResponse(json.dumps({'id': lineitem.id, 'amount': str(lineitem.line_amount)}), content_type="application/json")

def generate_pdf(request, poid):
    purchase_order = PurchaseOrderDetail.objects.get(id=poid)
    purchase_order_items = PurchaseOrderLineDetail.objects.filter(purchaseOrderDetail_id=poid)
    #calculate total
    grand_total = 0
    for item in purchase_order_items:
        grand_total = grand_total + item.amount

    template = get_template("pdf/invoice.htm")
    model = {
        'purchase_order': purchase_order,
        'purchase_order_items': purchase_order_items,
        'grand_total': grand_total
    }
    html = template.render(model)
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


    # pdf = open("out.pdf", encoding="utf8")
    # response = HttpResponse(pdf.read(), content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename=output.pdf'
    # pdf.close()
    # os.remove("out.pdf")

    # return Render.render('pdf/invoice.htm', {})

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None
