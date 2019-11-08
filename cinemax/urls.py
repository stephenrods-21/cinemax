"""cinemax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('cinemaxpr.urls')),
    path('login', views.login, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('admindashboard', views.adminDashboard, name='admindashboard'),
    path('adduser', views.addUser, name='adduser'),
    path('manageusers', views.manageUsers, name='manageusers'),
    path('addbusinessunit', views.addBusinessUnit, name='addbusinessunit'),
    path('businessunits', views.businessunits, name='businessunits'),
    path('lineofapproval', views.lineOfApproval, name='lineofapproval'),
    path('admin/', admin.site.urls),
]
