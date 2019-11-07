from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('memo', views.memo, name='memo'),
    path('budget', views.budget, name='budget')
]