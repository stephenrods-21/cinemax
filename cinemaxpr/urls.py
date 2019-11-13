from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('memo', views.memo, name='memo'),
    path('editmemo', views.editMemo, name='editmemo'),
    path('editmemo/<int:id>', views.editMemo, name='editMemoById'),
    path('updatememo', views.updateMemo, name='updateMemo'),
    path('budget', views.budget, name='budget'),
    path('getDocumentNumber/<int:buid>', views.getDocumentNumber, name='getdocumentnumber'),
    path('updateTransactionStatus/<int:tid>/<int:isApproved>', views.updateTransactionStatus, name='updateTransactionStatus')
]