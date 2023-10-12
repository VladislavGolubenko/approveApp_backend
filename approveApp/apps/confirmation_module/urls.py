from django.urls import path
from apps.confirmation_module.views import InvoiceListAPIView, InvoiceAPIView


urlpatterns = [
    path('invoice_list/', InvoiceListAPIView.as_view()),
    path('invoice/<invoice_number:str>/', InvoiceAPIView.as_view()),
]
