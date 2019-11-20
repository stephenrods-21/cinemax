from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Max
from cinemaxpr.models import businessunit, LineOfApproval, LineOfApprovalDetail, ExtendedUser, Role, MemoDetail
import json
from cinemax.enums import Status
from django.http import HttpResponse


def check_access(user):
    return user.is_superuser


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        # check if user exists
        user = auth.authenticate(
            username=request.POST["uname"], password=request.POST["pass"])

        if user is not None:
            auth.login(request, user)
            extended_user = ExtendedUser.objects.get(user_id=request.user.id)

            request.session['role'] = extended_user.role.name
            # request.session['entity_type_id'] = 2
            request.session['entity_type_id'] = extended_user.entity_type_id
            request.session['bu_id'] = extended_user.businessunit_id

            if user.is_superuser:
                return redirect('admindashboard')
            elif extended_user.entity_type_id == 2:
                return redirect('purchaseorder/dashboard')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'account/login.htm', {'error': 'Invalid Login credentials!'})
    else:
        return render(request, 'account/login.htm', {'view': 'login'})


@user_passes_test(check_access)
def editUser(request, id):
    if id > 0:
        editUser = ExtendedUser.objects.get(id=id)
        return render(request, 'admin/edituser.htm', {'view': 'manageusers', 'title': 'Manage User', 'editUser': editUser, 'businessunits': businessunit.objects.filter(is_visible=True, entity_type_id=request.session['entity_type_id']), 'users': ExtendedUser.objects.filter(entity_type_id=request.session['entity_type_id']).select_related(), 'roles': Role.objects.filter(entity_type_id=request.session['entity_type_id'])})

    if request.method == "POST":
        userData = json.loads(request.POST['data'])
        user = User.objects.create_user(
            username=userData['username'], password=userData['password'])
        extendedUser = ExtendedUser(
            email=userData['email'], role_id=userData['role'], businessunit_id=userData['businessunit'], user_id=user.id, entity_type_id=request.session['entity_type_id'])
        extendedUser.save()

        return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")

    return render(request, 'admin/edituser.htm', {'view': 'manageusers', 'title': 'Manage User', 'businessunits': businessunit.objects.filter(is_visible=True, entity_type_id=request.session['entity_type_id']), 'users': ExtendedUser.objects.filter(entity_type_id=request.session['entity_type_id']).select_related(), 'roles': Role.objects.filter(entity_type_id=request.session['entity_type_id'])})


@user_passes_test(check_access)
def updateUser(request):
    if request.method == "POST":
        userData = json.loads(request.POST['data'])

        editUser = ExtendedUser.objects.get(id=userData['id'])
        editUser.email = userData['email']
        editUser.businessunit_id = userData['businessunit']
        editUser.role_id = userData['role']
        editUser.save()

    return redirect('/manageusers')


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('login'))


@user_passes_test(check_access)
def adminDashboard(request):
    pending_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.PENDING.value, entity_type_id=request.session['entity_type_id']).count()
    approved_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.APPROVED.value, entity_type_id=request.session['entity_type_id']).count()
    rejected_count = MemoDetail.objects.filter(
        approvalstatus_id=Status.REJECTED.value, entity_type_id=request.session['entity_type_id']).count()
    return render(request, 'admin/admindashboard.htm', {'view': 'dashboard', 'title': 'Dashboard', 'pending_count': pending_count, 'approved_count': approved_count, 'rejected_count': rejected_count})


@user_passes_test(check_access)
def manageUsers(request):
    users = ExtendedUser.objects.filter(
        entity_type_id=request.session['entity_type_id']).select_related()
    return render(request, 'admin/manageusers.htm', {'view': 'manageusers', 'title': 'Manage Users', 'users': users, 'businessunits': businessunit.objects.filter(entity_type_id=request.session['entity_type_id']), 'roles': Role.objects.filter(entity_type_id=request.session['entity_type_id'])})


@user_passes_test(check_access)
def businessunits(request):
    return render(request, 'admin/businessunit.htm', {'view': 'businessunits', 'title': 'Business Unit', 'businessunits': businessunit.objects.filter(is_visible=True, entity_type_id=request.session['entity_type_id'])})


@user_passes_test(check_access)
def addBusinessUnit(request):
    bu = businessunit(
        name=request.POST['name'], prefix=request.POST['prefix'], created_by_id=request.user.id, entity_type_id=request.session['entity_type_id'])
    bu.save()
    return redirect('businessunits')


@user_passes_test(check_access)
def roles(request):
    return render(request, 'admin/roles.htm', {'view': 'roles', 'title': 'Role', 'roles': Role.objects.filter(entity_type_id=request.session['entity_type_id'])})


@user_passes_test(check_access)
def addRole(request):
    role = Role(name=request.POST['name'], created_by_id=request.user.id,
                entity_type_id=request.session['entity_type_id'])
    role.save()
    return redirect('roles')


@user_passes_test(check_access)
def lineOfApproval(request):
    return render(request, 'admin/lineofapproval.htm', {'view': 'lineofapprovals', 'title': 'Line Of Approval', 'lineofapprovals': LineOfApproval.objects.filter(entity_type_id=request.session['entity_type_id'])})


@user_passes_test(check_access)
def editlineOfApproval(request, id):
    if id > 0:
        editLineOfApproval = LineOfApproval.objects.get(id=id)
        editLineOfApprovalDetail = LineOfApprovalDetail.objects.filter(
            line_of_approval_id=editLineOfApproval.id)
        maxLevel = LineOfApprovalDetail.objects.filter(
            line_of_approval_id=editLineOfApproval.id).aggregate(Max('level'))

        return render(request, 'admin/editlineofapproval.htm', {'view': 'lineofapprovals', 'title': 'Line Of Approval', 'max_level': maxLevel['level__max'], 'editLineOfApproval': editLineOfApproval, 'editLineOfApprovalDetail': editLineOfApprovalDetail, 'businessunits': businessunit.objects.filter(is_visible=True, entity_type_id=request.session['entity_type_id']), 'users': ExtendedUser.objects.filter(entity_type_id=request.session['entity_type_id']).select_related()})

    if request.method == "POST":
        loaData = json.loads(request.POST['data'])
        loaApproverList = json.loads(request.POST['approverList'])
        loaApprovalRuleList = json.loads(request.POST['approvalRuleList'])

        lineOfApproval = LineOfApproval(name=loaData['name'], businessunit=businessunit.objects.get(id=loaData['businessunit']),
                                        no_of_approver=0, created_by=request.user, entity_type_id=request.session['entity_type_id'])
        lineOfApproval.save()

        for approver in loaApproverList:
            lineOfApprovalDetail = LineOfApprovalDetail(line_of_approval=lineOfApproval,
                                                        approver=User.objects.get(
                                                            id=approver['approver_id']),
                                                        required_approval=loaApprovalRuleList[int(
                                                            approver["level"])-1]['required_approval'],
                                                        level=approver['level'],
                                                        entity_type_id=request.session['entity_type_id'])

            lineOfApprovalDetail.save()

        return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")

    return render(request, 'admin/editlineofapproval.htm', {'view': 'lineofapprovals', 'title': 'Line Of Approval', 'max_level': 0, 'businessunits': businessunit.objects.filter(is_visible=True, entity_type_id=request.session['entity_type_id']), 'users': ExtendedUser.objects.filter(entity_type_id=request.session['entity_type_id']).select_related()})


@user_passes_test(check_access)
def updateLineOfApproval(request):
    if request.method == "POST":
        loaData = json.loads(request.POST['data'])
        loaApproverList = json.loads(request.POST['approverList'])
        loaApprovalRuleList = json.loads(request.POST['approvalRuleList'])

        lineOfApproval = LineOfApproval.objects.get(id=loaData['id'])
        lineOfApproval.name = loaData['name']
        lineOfApproval.businessuint = loaData['businessunit']
        lineOfApproval.save()

        LineOfApprovalDetail.objects.filter(
            line_of_approval_id=lineOfApproval.id).delete()

        for approver in loaApproverList:
            lineOfApprovalDetail = LineOfApprovalDetail(line_of_approval=lineOfApproval,
                                                        approver=User.objects.get(
                                                            id=approver['approver_id']),
                                                        required_approval=loaApprovalRuleList[int(
                                                            approver["level"])-1]['required_approval'],
                                                        level=approver['level'])

            lineOfApprovalDetail.save()

    return redirect('lineofapprovals')


@user_passes_test(check_access)
def deleteLineOfApproval(request, id):
    LineOfApproval.objects.get(id=id).delete()
    # LineOfApprovalDetail.objects.filter(id=id).delete()
    print(id)
    return HttpResponse(id)
