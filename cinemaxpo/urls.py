from django.urls import path
from . import views

urlpatterns = [
    path('purchaseorder/dashboard', views.dashboard, name='purchaseorderdashboard'),
    path('purchaseorder/list', views.purchaseorder, name='purchaseorderlist'),
    # path('purchaseorder/generatepdf', views.generate_pdf, name='purchaseordergeneratepdf'),
    path('purchaseorder/editpurchaseorder', views.editpurchaseorder, name='editpurchaseorder'),
    path('purchaseorder/editpurchaseorder/<int:id>/<int:poid>', views.editpurchaseorder, name='editpurchaseorderById'),
    path('purchaseorder/getprdetail/<int:id>', views.getprdetailbyid, name='getprdetailById'),
    path('purchaseorder/getprlinedetail/<int:id>', views.getprlinedetailbyid, name='getprlinedetailById'),
    path('purchaseorder/updatePOTransactionStatus/<int:tid>/<int:isApproved>', views.updatePOTransactionStatus, name='updatePOTransactionStatus'),
]