from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.confirmation_module.views import InvoiceListAPIView, InvoiceAPIView, POAPIView


urlpatterns = [
    path('invoice_list/', InvoiceListAPIView.as_view()),
    path('po/<str:po_number>/', POAPIView.as_view()),
    path('invoice/<int:id>/', csrf_exempt(InvoiceAPIView.as_view()))

]
