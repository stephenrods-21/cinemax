from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User


def check_access(user):
       return user.is_superuser
       
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        # check if user exists
        user = auth.authenticate(username=request.POST["uname"], password=request.POST["pass"])

        if user is not None:
            auth.login(request, user)

            if user.is_superuser:
                return redirect('admindashboard')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'account/login.htm', {'error' : 'Invalid Login credentials!'})
    else:
        return render(request,'account/login.htm', {'view': 'login'})
        
@user_passes_test(check_access)
def addUser(request):
    if User.objects.filter(username=request.POST['uname']).count() > 0:
        return redirect('manageusers')
        
    User.objects.create_user(username=request.POST['uname'],password=request.POST['pass'])
    return redirect('manageusers')

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect(reverse('login'))

@user_passes_test(check_access)
def adminDashboard(request):
    return render(request, 'admin/admindashboard.htm', {'view':'dashboard'})

@user_passes_test(check_access)
def manageUsers(request):
    users = User.objects.all()
    return render(request, 'admin/manageusers.htm', {'view':'manageusers', 'users': users})
