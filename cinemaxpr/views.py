from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from cinemaxpr.models import businessunit, MemoDetail, BudgetDetail, AttachmentDetail, PurchaseRequisitionDetail, PurchaseRequisitionLineDetail, LineOfApproval, LineOfApprovalDetail, ExtendedUser, Role, ApprovalStatus, TransactionDetail
import json
import os
from django.http import JsonResponse
from .forms import ImageFileUploadForm
from cinemax.enums import Status
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.htm')

@login_required(login_url='login')
def dashboard(request):
    current_user = ExtendedUser.objects.get(user_id=request.user.id)

    memos = MemoDetail.objects.filter(
        Q(businessunit_id=current_user.businessunit_id) | Q(created_by_id=request.user.id))
    purchaserequisitions = PurchaseRequisitionDetail.objects.filter(
        created_by_id=request.user.id)

    pending_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.PENDING.value, created_by_id=request.user.id).count()
    approved_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.APPROVED.value, created_by_id=request.user.id).count()
    rejected_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.REJECTED.value, created_by_id=request.user.id).count()
    transactions = TransactionDetail.objects.filter(
        extendeduserObj=request.user.id, transactionstatus=Status.PENDING.value).select_related()
    return render(request, 'dashboard.htm', {'view': 'dashboard', 'title': 'Dashboard', 'pending_count': pending_count, 'approved_count': approved_count, 'rejected_count': rejected_count, 'transactions': transactions, 'memos': memos, 'purchaserequisitions': purchaserequisitions})


@login_required(login_url='login')
def memo(request):
    memos = MemoDetail.objects.filter(created_by_id=request.user.id).select_related()
    return render(request, 'memo/list.htm', {'view': 'memo', 'title': 'Memo', 'memos': memos})

@login_required(login_url='login')
def editMemo(request, id):
    document_id = 0
    if id > 0:
        editMemo = MemoDetail.objects.get(id=id)
        return render(request, 'memo/editmemo.htm', {'view': 'memo', 'title': 'Edit Memo', 'editMemo': editMemo, 'businessunits': businessunit.objects.filter(Q(is_visible=False) | Q(id=request.session['bu_id']))})

    if request.method == "POST":
        businessunit_id = int(request.POST['businessunit'])
        topic = request.POST['topic']
        description = request.POST['description']
        amount = request.POST['amount']
        document_no = request.POST['documentno']

        for filename, file in request.FILES.items():
            form = ImageFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                result = form.save()
                document_id = result.pk

        memo = MemoDetail(documentno=document_no, topic=topic, businessunit=businessunit.objects.get(id=businessunit_id),
                          approvalstatus_id=Status.PENDING.value, created_by=request.user)
        budget = BudgetDetail(
            description=description, amount=amount, created_by_id=request.user.id)
        budget.save()
        memo.budget_id = budget.id
        memo.save()
        #Add memo to attachment reference if exists 
        if document_id > 0:
            attachment = AttachmentDetail.objects.get(id=document_id)
            attachment.memo_id = memo.id
            attachment.save()

        # update the new document number
        editBusinessUnit = businessunit.objects.get(
            id=businessunit_id)
        editBusinessUnit.documentno = editBusinessUnit.documentno + 1
        editBusinessUnit.save()

        # get LOA for based on Users Business Unit
        if(LineOfApproval.objects.filter(businessunit_id=memo.businessunit_id).count() > 0):
            lineOfApproval = LineOfApproval.objects.get(
                businessunit_id=request.session['bu_id'])
            lineOfApprovalDetail = LineOfApprovalDetail.objects.filter(
                line_of_approval_id=lineOfApproval.id, level=1)

            # from level 1 make entry in transactions table for LOA
            for loaDetail in lineOfApprovalDetail:
                transaction = TransactionDetail(level=loaDetail.level, required_approval=loaDetail.required_approval,
                                                businessunitObj=lineOfApproval.businessunit_id,
                                                lineOfApprovalObj=lineOfApproval.id,
                                                extendeduserObj=loaDetail.approver_id, memoObj_id=memo.id, transactionstatus=Status.PENDING.value)
                transaction.save()
        else:
            # If BU does not have LOA then set status to Approved
            memo.approvalstatus_id = Status.APPROVED.value
            memo.save()

        return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")
    return render(request, 'memo/editmemo.htm', {'view': 'memo', 'title': 'Edit memo', 'businessunits': businessunit.objects.filter(Q(is_visible=False) | Q(id=request.session['bu_id']))})


@login_required(login_url='login')
def updateMemo(request):
    if request.method == "POST":
        print(request.POST)
        memo_id = int(request.POST['id'])
        topic = request.POST['topic']
        description = request.POST['description']
        amount = request.POST['amount']

        editMemo = MemoDetail.objects.get(id=memo_id)
        editBudget = BudgetDetail.objects.get(id=editMemo.budget_id)
        editBudget.description = description
        editBudget.save()
        editMemo.topic = topic
        editMemo.save()

    return redirect('memo')


@login_required(login_url='login')
def budget(request):
    return render(request, 'budget.htm', {'view': 'budget'})


@login_required(login_url='login')
def purchaseRequisition(request):
    return render(request, 'purchaserequisition/list.htm', {'view': 'purchaserequisition', 'title': 'Purchase Requisition', 'purchaserequisitions': PurchaseRequisitionDetail.objects.all()})


@login_required(login_url='login')
def purchaseRequisitionMemo(request):
    approved_memos = MemoDetail.objects.filter(
        approvalstatus_id=Status.APPROVED.value).select_related()
    return render(request, 'purchaserequisition/memolist.htm', {'view': 'approvedmemo', 'title': 'Approved Memo\'s', 'memos': approved_memos})


@login_required(login_url='login')
def editPurchaseRequisition(request, id, budgetid):
    edit_purchase_requisition = PurchaseRequisitionDetail()
    edit_purchase_requisition.id = 0
    edit_purchase_requisition.budget_id = 0
    edit_purchase_requisition.vendor_name = ""
    edit_purchase_requisition.vendor_account = ""
    if budgetid > 0:
        edit_purchase_requisition.budgetDetail = BudgetDetail.objects.get(
            id=budgetid)

    if id > 0:
        edit_purchase_requisition = PurchaseRequisitionDetail.objects.get(
            id=id)
        line_items = PurchaseRequisitionLineDetail.objects.filter(purchaseRequisitionDetail_id=edit_purchase_requisition.id)
        return render(request, 'purchaserequisition/editpurchaserequisition.htm', {'view': 'purchaserequisition', 'title': 'Edit Purchase Requisition', 'editPurchaseRequisition': edit_purchase_requisition, 'line_items': line_items})

    if request.method == "POST":
        purchaseRequisitionData = json.loads(request.POST['data'])
        purchaseRequisitionLineData = json.loads(request.POST['lineitems'])

        if budgetid > 0:
            purchaseRequisition = PurchaseRequisitionDetail(
                vendor_name=purchaseRequisitionData['vendorname'],
                vendor_account=purchaseRequisitionData['vendoraccount'],
                actual_amount=purchaseRequisitionData['amount'],
                title=purchaseRequisitionData['title'], budgetDetail_id=budgetid, created_by_id=request.user.id, status=ApprovalStatus.objects.get(id=Status.PENDING.value))
        else:
            purchaseRequisition = PurchaseRequisitionDetail(
                vendor_name=purchaseRequisitionData['vendorname'],
                vendor_account=purchaseRequisitionData['vendoraccount'],
                actual_amount=purchaseRequisitionData['amount'],
                title=purchaseRequisitionData['title'], created_by_id=request.user.id, status=ApprovalStatus.objects.get(id=Status.PENDING.value))

        purchaseRequisition.save()

        # entry for line items
        for lineitem in purchaseRequisitionLineData:
            if lineitem['lineid'] == "":
                lineitem = PurchaseRequisitionLineDetail(description=lineitem['linedescription'], line_amount=lineitem['lineamount'], remark=lineitem['lineremark'],
                                                         created_by_id=request.user.id,
                                                         status_id=Status.PENDING.value,
                                                         purchaseRequisitionDetail_id=purchaseRequisition.id
                                                         )
                lineitem.save()

        #get LOA for based on Business Unit
        memo = MemoDetail.objects.get(budget_id=budgetid)

        if(LineOfApproval.objects.filter(businessunit_id=memo.businessunit_id).count() > 0):
            lineOfApproval = LineOfApproval.objects.get(
                businessunit_id=memo.businessunit_id)
            lineOfApprovalDetail = LineOfApprovalDetail.objects.filter(
                line_of_approval_id=lineOfApproval.id, level=1)

            # from level 1 make entry in transactions table for LOA
            for loaDetail in lineOfApprovalDetail:
                transaction = TransactionDetail(level=loaDetail.level, required_approval=loaDetail.required_approval,
                                                businessunitObj=lineOfApproval.businessunit_id,
                                                lineOfApprovalObj=lineOfApproval.id,
                                                extendeduserObj=loaDetail.approver_id, purchaseRequisitionDetail_id=purchaseRequisition.id, transactionstatus=Status.PENDING.value)
                transaction.save()
        else:
            # If PR does not have LOA then set status to Approved
            purchaseRequisition.status_id = Status.APPROVED.value
            purchaseRequisition.save()

    return render(request, 'purchaserequisition/editpurchaserequisition.htm', {'view': 'purchaserequisition', 'title': 'Edit Purchase Requisition', 'editPurchaseRequisition': edit_purchase_requisition})

def updatePurchaseRequisition(request):
    if request.method == "POST":
        purchaseRequisitionData = json.loads(request.POST['data'])
        purchaseRequisitionLineData = json.loads(request.POST['lineitems'])

        pr_detail = PurchaseRequisitionDetail.objects.get(id=purchaseRequisitionData['id'])
        pr_detail.title = purchaseRequisitionData['title']
        pr_detail.vendor_name = purchaseRequisitionData['vendorname']
        pr_detail.vendor_account = purchaseRequisitionData['vendoraccount']
        pr_detail.save()

        # entry for line items
        for lineitem in purchaseRequisitionLineData:
            if lineitem['lineid'] == "":
                lineitem = PurchaseRequisitionLineDetail(description=lineitem['linedescription'], line_amount=lineitem['lineamount'], remark=lineitem['lineremark'],
                                                         created_by_id=request.user.id,
                                                         status_id=Status.PENDING.value,
                                                         purchaseRequisitionDetail_id=pr_detail.id
                                                         )
                lineitem.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

def getDocumentNumber(request, buid):
    bu = businessunit.objects.get(id=buid)
    documentno = "{}-{}".format(bu.prefix, bu.documentno)
    return HttpResponse(json.dumps({'documentno': documentno}), content_type="application/json")


def updatePRTransactionStatus(request, tid, isApproved):
    # Get transaction by id and set status.
    transaction = TransactionDetail.objects.get(id=tid)
    if isApproved == 1:
        transaction.transactionstatus = Status.APPROVED.value
        transaction.save()
    else:
        transaction.transactionstatus = Status.REJECTED.value
        transaction.save()

    if isApproved == 0:
        # Get PR Details & pending pr transactions
        pr_detail = PurchaseRequisitionDetail.objects.get(
            id=transaction.purchaseRequisitionDetail_id)
        pending_transactions = TransactionDetail.objects.filter(
            purchaseRequisitionDetail_id=pr_detail.id, level=transaction.level, transactionstatus=Status.PENDING.value)

        if pending_transactions.count() >= transaction.required_approval:
            return HttpResponse(json.dumps({'status': "waiting for others"}), content_type="application/json")
        else:
            pr_detail.status_id = Status.REJECTED.value
            pr_detail.save()

            extendeduser = ExtendedUser.objects.get(
                user_id=pr_detail.created_by_id)
            subject = 'PR Rejected'
            message = settings.REJECTED_EMAIL_TEMPLATE.format(pr_detail.title)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            send_mail(subject, message, email_from, recipient_list)
            print("PR-REJECTED")
            return HttpResponse(json.dumps({'status': "PR Rejected"}), content_type="application/json")

        return HttpResponse(json.dumps({'status': "Waitng for others"}), content_type="application/json")

    elif isApproved == 1:
        pr_detail = PurchaseRequisitionDetail.objects.get(
            id=transaction.purchaseRequisitionDetail_id)
        approved_transactions = TransactionDetail.objects.filter(
            purchaseRequisitionDetail_id=pr_detail.id,
            level=transaction.level,
            transactionstatus=Status.APPROVED.value)

        if approved_transactions.count() < transaction.required_approval:
            print("WAITING FOR OTHERS TO APPROVE")
            return HttpResponse(json.dumps({'status': "WAITING FOR OTHERS TO APPROVE"}), content_type="application/json")

        # Once all approve in the current Level, check if more level of approval is needed
        next_level = transaction.level + 1
        line_of_approval_detail = LineOfApprovalDetail.objects.filter(
            line_of_approval_id=transaction.lineOfApprovalObj, level=next_level)

        if(line_of_approval_detail.count() > 0):
            print("REQUIRE FURTHER LOA LEVEL 2 {}",
                  transaction.lineOfApprovalObj)
            for loa_detail in line_of_approval_detail:
                transaction_detail = TransactionDetail(level=loa_detail.level, required_approval=loa_detail.required_approval,
                                                       extendeduserObj=loa_detail.approver_id,
                                                       lineOfApprovalObj=loa_detail.line_of_approval_id,
                                                       businessunitObj=transaction.businessunitObj,
                                                       purchaseRequisitionDetail=transaction.purchaseRequisitionDetail,
                                                       transactionstatus=Status.PENDING.value)
                transaction_detail.save()
        else:
            print("NO MORE LOA LEVEL, SO SET TRANSACTION STATUS TO APPROVED")
            pr_details = PurchaseRequisitionDetail.objects.get(
                id=transaction.purchaseRequisitionDetail_id)
            pr_details.status_id = Status.APPROVED.value
            pr_details.save()

            extendeduser = ExtendedUser.objects.get(
                user_id=pr_details.created_by_id)

            subject = "PR Approved By CEO"
            message = settings.APPROVED_EMAIL_TEMPLATE.format(pr_details.title)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            print(message, extendeduser.email)
            send_mail(subject, message, email_from, recipient_list)


def updateTransactionStatus(request, tid, isApproved):
    transaction = TransactionDetail.objects.get(id=tid)
    if isApproved == 1:
        transaction.transactionstatus = Status.APPROVED.value
        transaction.save()
    else:
        transaction.transactionstatus = Status.REJECTED.value
        transaction.save()

    if isApproved == 0:
        memo_detail = MemoDetail.objects.get(id=transaction.memoObj_id)
        # rejected_transactions = TransactionDetail.objects.filter(
        #     memoObj_id=memo_detail.id, level=transaction.level, transactionstatus=Status.REJECTED.value)

        pending_transactions = TransactionDetail.objects.filter(
            memoObj_id=memo_detail.id, level=transaction.level, transactionstatus=Status.PENDING.value)

        if pending_transactions.count() >= transaction.required_approval:
            return HttpResponse(json.dumps({'status': "waiting for others"}), content_type="application/json")
        else:
            memo = MemoDetail.objects.get(id=transaction.memoObj_id)
            memo.approvalstatus_id = Status.REJECTED.value
            memo.save()

            extendeduser = ExtendedUser.objects.get(user_id=memo.created_by_id)
            subject = 'Memo Rejected'
            message = settings.REJECTED_EMAIL_TEMPLATE.format(memo.topic)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            send_mail(subject, message, email_from, recipient_list)
            print("REJECTED")
            return HttpResponse(json.dumps({'status': "Rejected"}), content_type="application/json")

        return HttpResponse(json.dumps({'status': "Waitng for others"}), content_type="application/json")

    elif isApproved == 1:
        # check if there are any more pending approvals needs to be approved where must_approve is true
        # Get Transaction in approved status
        memo_detail = MemoDetail.objects.get(id=transaction.memoObj_id)
        approved_transactions = TransactionDetail.objects.filter(
            memoObj_id=memo_detail.id,
            level=transaction.level,
            transactionstatus=Status.APPROVED.value)

        if approved_transactions.count() < transaction.required_approval:
            print("WAITING FOR OTHERS TO APPROVE")
            return HttpResponse(json.dumps({'status': "WAITING FOR OTHERS TO APPROVE"}), content_type="application/json")

        # Once all approve in the current Level, check if more level of approval is needed
        next_level = transaction.level + 1
        line_of_approval_detail = LineOfApprovalDetail.objects.filter(
            line_of_approval_id=transaction.lineOfApprovalObj, level=next_level)

        if(line_of_approval_detail.count() > 0):
            print("REQUIRE FURTHER LOA LEVEL 2 {}",
                  transaction.lineOfApprovalObj)
            for loa_detail in line_of_approval_detail:
                transaction_detail = TransactionDetail(level=loa_detail.level, required_approval=loa_detail.required_approval,
                                                       extendeduserObj=loa_detail.approver_id,
                                                       lineOfApprovalObj=loa_detail.line_of_approval_id,
                                                       businessunitObj=transaction.businessunitObj,
                                                       memoObj=transaction.memoObj,
                                                       transactionstatus=Status.PENDING.value)
                transaction_detail.save()
        else:
            print("NO MORE LOA LEVEL, SO SET TRANSACTION STATUS TO APPROVED")
            memo = MemoDetail.objects.get(id=transaction.memoObj_id)
            memo.approvalstatus_id = Status.APPROVED.value
            memo.save()

            extendeduser = ExtendedUser.objects.get(user_id=memo.created_by_id)

            subject = "Memo Approved By CEO"
            message = settings.APPROVED_EMAIL_TEMPLATE.format(memo.topic)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            print(message, extendeduser.email)
            send_mail(subject, message, email_from, recipient_list)

    return HttpResponse(json.dumps({'documentno': "123"}), content_type="application/json")
