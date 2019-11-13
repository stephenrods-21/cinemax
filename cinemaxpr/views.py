from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from cinemaxpr.models import businessunit, MemoDetail, BudgetDetail, LineOfApproval, LineOfApprovalDetail, ExtendedUser, Role, ApprovalStatus, TransactionDetail
import json
from cinemax.enums import Status
from django.http import HttpResponse

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
        extendeduser_id=request.user.id, transactionstatus=Status.PENDING.value).select_related()
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
                transaction = TransactionDetail(level=loaDetail.level, must_approve=loaDetail.must_approve,
                                                businessunit_id=lineOfApproval.businessunit_id, created_by_id=request.user.id,
                                                lineOfApproval=lineOfApproval.id,
                                                extendeduser_id=loaDetail.approver_id, memo_id=memo.id, transactionstatus_id=Status.PENDING.value)

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

   if isApproved == 1:
       transaction = TransactionDetail.objects.get(id=tid)
       transaction.transactionstatus = Status.APPROVED.value
       transaction.save();
   else:
       transaction = TransactionDetail.objects.get(id=tid)
       transaction.transactionstatus = Status.REJECTED.value
       transaction.save();

   if isApproved == 0 and transaction.must_approve == True:
       print("REJECTED")
   elif isApproved == 1:
        # check if there are any more pending approvals needs to be approved where must_approve is true
        if TransactionDetail.objects.filter(transactionstatus=Status.PENDING.value, must_approve=True).count()  > 0:
            print("WAITING FOR OTHERS TO APPROVE")
            return HttpResponse(json.dumps({'status': "WAITING FOR OTHERS TO APPROVE"}), content_type="application/json")
        
        # Once all approve in the current Level, check if more level of approval is needed
        nextLevel = transaction.level + 1
        lineOfApprovalDetail = LineOfApprovalDetail.objects.filter(line_of_approval_id=transaction.lineOfApproval, level=nextLevel)

        if(lineOfApprovalDetail.count() > 0):
            print("REQUIRE FURTHER LOA LEVEL 2 {}",transaction.lineOfApproval)
            for loaDetail in lineOfApprovalDetail:
                transactionDetail = TransactionDetail(level=loaDetail.level, must_approve=loaDetail.must_approve,
                                                extendeduser_id=loaDetail.approver_id,
                                                lineOfApproval=loaDetail.line_of_approval_id,
                                                businessunit=transaction.businessunit,
                                                transactionstatus=Status.PENDING.value)
                transactionDetail.save()
        else:
            print("NO MORE LOA LEVEL, SO SET TRANSACTION STATUS TO APPROVED")
    
   return HttpResponse(json.dumps({'documentno': "123"}), content_type="application/json")
