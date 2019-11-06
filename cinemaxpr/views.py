from django.shortcuts import render

# Create your views here.
def index(request):
    print('HIIIIIIIIIIIIIIIIII')
    return render(request, 'index.htm')
