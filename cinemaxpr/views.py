from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.htm')

def dashboard(request):
    return render(request, 'dashboard.htm', {'view': 'dashboard'})

def memo(request):
    return render(request, 'memo.htm', {'view': 'memo'})

def budget(request):
    return render(request, 'budget.htm', {'view': 'budget'})
