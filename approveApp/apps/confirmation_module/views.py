from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from apps.confirmation_module.models import Invoice
from apps.confirmation_module.serializers import InvoiceListSerializer, ChangeInvoiceSerializer, DetailInvoiceSerializer


class InvoiceListAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer
    pagination_class = LimitOffsetPagination


class InvoiceAPIView(RetrieveUpdateAPIView):
    serializer_class = None
    queryset = Invoice.objects.all()

    def get_object(self):
        serializer_class = DetailInvoiceSerializer
        return get_object_or_404(Invoice, invoice_number=self.request.invoice_number)

    def patch(self, request, *args, **kwargs):
        serializer_class = ChangeInvoiceSerializer
