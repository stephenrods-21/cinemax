from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.htm')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.htm', {'view': 'dashboard'})

@login_required(login_url='login')
def memo(request):
    return render(request, 'memo.htm', {'view': 'memo'})

@login_required(login_url='login')
def budget(request):
    return render(request, 'budget.htm', {'view': 'budget'})
