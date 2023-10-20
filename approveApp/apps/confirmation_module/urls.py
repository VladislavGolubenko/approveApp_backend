from django.urls import path
from apps.confirmation_module.views import InvoiceListAPIView, InvoiceAPIView, POAPIView, SupplierListAPIView


urlpatterns = [
    path('invoice_list/', InvoiceListAPIView.as_view()),
    path('po/<str:po_number>/', POAPIView.as_view()),
    path('invoice/<int:id>/', InvoiceAPIView.as_view()),
    path('supplier_list/', SupplierListAPIView.as_view()),
]
