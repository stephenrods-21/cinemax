from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from cinemaxpr.models import businessunit, MemoDetail, BudgetDetail, LineOfApproval, LineOfApprovalDetail, ExtendedUser, Role, ApprovalStatus, TransactionDetail
import json
from cinemax.enums import Status
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.htm')


@login_required(login_url='login')
def dashboard(request):
    pending_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.PENDING.value, created_by_id=request.user.id).count()
    approved_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.APPROVED.value, created_by_id=request.user.id).count()
    rejected_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.REJECTED.value, created_by_id=request.user.id).count()
    transactions = TransactionDetail.objects.filter(
        extendeduserObj=request.user.id, transactionstatus=Status.PENDING.value).select_related()
    return render(request, 'dashboard.htm', {'view': 'dashboard', 'title': 'Dashboard', 'pending_count': pending_count, 'approved_count': approved_count, 'rejected_count': rejected_count, 'transactions': transactions})


@login_required(login_url='login')
def memo(request):
    return render(request, 'memo/list.htm', {'view': 'memo', 'title': 'Memo', 'memos': MemoDetail.objects.filter(created_by_id=request.user.id).select_related()})


@login_required(login_url='login')
def editMemo(request, id):
    if id > 0:
        editMemo = MemoDetail.objects.get(id=id)
        return render(request, 'memo/editmemo.htm', {'view': 'memo', 'title': 'Edit Memo', 'editMemo': editMemo, 'businessunits': businessunit.objects.all()})

    if request.method == "POST":
        memoData = json.loads(request.POST['data'])

        memo = MemoDetail(documentno=memoData['documentno'], topic=memoData['topic'], businessunit=businessunit.objects.get(id=memoData['businessunit']),
                          approvalstatus_id=Status.PENDING.value, created_by=request.user)
        budget = BudgetDetail(
            description=memoData['description'], amount=memoData['amount'], created_by_id=request.user.id)
        budget.save()
        memo.budget_id = budget.id
        memo.save()

        # update the new document number
        editBusinessUnit = businessunit.objects.get(
            id=memoData['businessunit'])
        editBusinessUnit.documentno = editBusinessUnit.documentno + 1
        editBusinessUnit.save()

        # get LOA for based on Business Unit
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
                                                extendeduserObj=loaDetail.approver_id, memoObj_id=memo.id, transactionstatus=Status.PENDING.value)
                transaction.save()

        return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")
    return render(request, 'memo/editmemo.htm', {'view': 'memo', 'title': 'Edit memo', 'businessunits': businessunit.objects.all()})


@login_required(login_url='login')
def updateMemo(request):
    if request.method == "POST":
        memoData = json.loads(request.POST['data'])

        editMemo = MemoDetail.objects.get(id=memoData['id'])
        editBudget = BudgetDetail.objects.get(id=editMemo.budget_id)
        editBudget.description = memoData['description']
        editBudget.save()
        editMemo.topic = memoData['topic']
        editMemo.businessunit_id = memoData['businessunit']
        editMemo.documentno = memoData['documentno']
        editMemo.save()

    return redirect('memo')


@login_required(login_url='login')
def budget(request):
    return render(request, 'budget.htm', {'view': 'budget'})


def getDocumentNumber(request, buid):
    bu = businessunit.objects.get(id=buid)
    documentno = "{}-{}".format(bu.prefix, bu.documentno)
    return HttpResponse(json.dumps({'documentno': documentno}), content_type="application/json")


def updateTransactionStatus(request, tid, isApproved):
   transaction = TransactionDetail.objects.get(id=tid)
   if isApproved == 1:
       transaction.transactionstatus = Status.APPROVED.value
       transaction.save();
   else:
       transaction.transactionstatus = Status.REJECTED.value
       transaction.save();

   if isApproved == 0:
       memo_detail = MemoDetail.objects.get(id=transaction.memoObj_id)
       rejected_transactions = TransactionDetail.objects.filter(memoObj_id=memo_detail.id, level=transaction.level, transactionstatus=Status.REJECTED.value)
       if rejected_transactions.count() <= transaction.required_approval:
           memo = MemoDetail.objects.get(id=transaction.memoObj_id)
           memo.approvalstatus_id = Status.REJECTED.value
           memo.save()

           extendeduser = ExtendedUser.objects.get(user_id=memo.created_by_id)
           subject = 'Memo Rejected'
           message = settings.REJECTED_EMAIL_TEMPLATE.format(extendeduser.user.username, memo.topic)
           email_from = settings.EMAIL_HOST_USER
           recipient_list = [extendeduser.email]
           send_mail( subject, message, email_from, recipient_list )
           print("REJECTED")
           return HttpResponse(json.dumps({'status': "Rejected"}), content_type="application/json")

       return HttpResponse(json.dumps({'status': "Waitng for others"}), content_type="application/json")

   elif isApproved == 1:
        # check if there are any more pending approvals needs to be approved where must_approve is true
        # Get Transaction in approved status
        memo_detail = MemoDetail.objects.get(id=transaction.memoObj_id)
        approved_transactions = TransactionDetail.objects.filter(memoObj_id=memo_detail.id, level=transaction.level, transactionstatus=Status.APPROVED.value)

        if approved_transactions.count() < transaction.required_approval:
            print("WAITING FOR OTHERS TO APPROVE")
            return HttpResponse(json.dumps({'status': "WAITING FOR OTHERS TO APPROVE"}), content_type="application/json")
        
        # Once all approve in the current Level, check if more level of approval is needed
        next_level = transaction.level + 1
        line_of_approval_detail = LineOfApprovalDetail.objects.filter(line_of_approval_id=transaction.lineOfApprovalObj, level=next_level)

        if(line_of_approval_detail.count() > 0):
            print("REQUIRE FURTHER LOA LEVEL 2 {}",transaction.lineOfApprovalObj)
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
            message = settings.APPROVED_EMAIL_TEMPLATE.format(extendeduser.user.username, memo.topic)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [extendeduser.email]
            print(message, extendeduser.email)
            send_mail( subject, message, email_from, recipient_list )
    
   return HttpResponse(json.dumps({'documentno': "123"}), content_type="application/json")
