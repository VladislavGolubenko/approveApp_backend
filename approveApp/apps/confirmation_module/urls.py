from django.urls import path
from apps.confirmation_module.views import InvoiceListAPIView, InvoiceAPIView, POAPIView


urlpatterns = [
    path('invoice_list/', InvoiceListAPIView.as_view()),
    path('invoice/<str:invoice_number>/', InvoiceAPIView.as_view()),
    path('po/<str:po_number>/', POAPIView.as_view())
]
