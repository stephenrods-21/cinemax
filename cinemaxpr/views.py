from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from cinemaxpr.models import businessunit, LineOfApproval, LineOfApprovalDetail, ExtendedUser, Role, Memo, ApprovalStatus
import json
from cinemax.enums import Status
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.htm')

@login_required(login_url='login')
def dashboard(request):
    pending_count = Memo.objects.filter(approvalstatus_id=Status.PENDING.value, created_by_id=request.user.id).count()
    approved_count = Memo.objects.filter(approvalstatus_id=Status.APPROVED.value, created_by_id=request.user.id).count()
    rejected_count = Memo.objects.filter(approvalstatus_id=Status.REJECTED.value, created_by_id=request.user.id).count()
    return render(request, 'dashboard.htm', {'view': 'dashboard', 'title': 'Dashboard','pending_count': pending_count, 'approved_count' : approved_count, 'rejected_count' : rejected_count})

@login_required(login_url='login')
def memo(request):
    return render(request, 'memo/list.htm', {'view': 'memo', 'title': 'Memo', 'memos': Memo.objects.filter(created_by_id=request.user.id).select_related()})

@login_required(login_url='login')
def editMemo(request, id):
    if id > 0:
        editMemo = Memo.objects.get(id=id)
        return render(request, 'memo/editmemo.htm', {'view':'memo', 'title': 'Edit Memo', 'editMemo' : editMemo, 'businessunits' : businessunit.objects.all()})

    if request.method == "POST":
        memoData = json.loads(request.POST['data'])

        memo = Memo(documentno=memoData['documentno'],topic=memoData['topic'],businessunit=businessunit.objects.get(id=memoData['businessunit']),
        approvalstatus_id=Status.PENDING.value,created_by=request.user)
        memo.save()
        editBusinessUnit = businessunit.objects.get(id=memoData['businessunit'])
        editBusinessUnit.documentno = editBusinessUnit.documentno + 1;
        editBusinessUnit.save()

        return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")
    return render(request, 'memo/editmemo.htm', {'view':'memo', 'title': 'Edit memo', 'businessunits' : businessunit.objects.all()})

@login_required(login_url='login')
def updateMemo(request):
    if request.method == "POST":
        memoData = json.loads(request.POST['data'])

        editMemo = Memo.objects.get(id=memoData['id'])
        editMemo.topic = memoData['topic']
        editMemo.businessunit_id = memoData['businessunit']
        editMemo.documentno = memoData['documentno']
        editMemo.save()

    return redirect('memo')


@login_required(login_url='login')
def budget(request):
    return render(request, 'budget.htm', {'view': 'budget'})

def getDocumentNumber(request,buid):
    bu = businessunit.objects.get(id=buid)
    documentno = "{}-{}".format(bu.prefix, bu.documentno)
    return HttpResponse(json.dumps({'documentno': documentno}), content_type="application/json")

