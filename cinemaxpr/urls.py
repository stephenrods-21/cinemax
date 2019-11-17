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
    path('purchaserequisition', views.purchaseRequisition, name='purchaserequisition'),
    path('purchaserequisition/memo', views.purchaseRequisitionMemo, name='purchaserequisitionmemo'),
    path('editpurchaserequisition', views.editPurchaseRequisition, name='editpurchaserequisition'),
    path('editpurchaserequisition/<int:id>/<int:budgetid>', views.editPurchaseRequisition, name='editpurchaserequisitionById'),
    path('updatepurchaserequisition', views.updateMemo, name='updatepurchaserequisition'),
    path('getDocumentNumber/<int:buid>', views.getDocumentNumber, name='getdocumentnumber'),
    path('updateTransactionStatus/<int:tid>/<int:isApproved>', views.updateTransactionStatus, name='updateTransactionStatus'),
    path('updatePRTransactionStatus/<int:tid>/<int:isApproved>', views.updatePRTransactionStatus, name='updatePRTransactionStatus')
]