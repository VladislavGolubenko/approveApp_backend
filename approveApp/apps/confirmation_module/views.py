from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from apps.confirmation_module.models import Invoice, PercacheOrder
from apps.confirmation_module.serializers import InvoiceListSerializer, ChangeInvoiceSerializer, InvoiceSerializer, PercacheOrderSerializer


class InvoiceListAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer
    pagination_class = LimitOffsetPagination


class InvoiceAPIView(RetrieveUpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_object(self):
        return get_object_or_404(Invoice, invoice_number=self.kwargs['invoice_number'])

    def patch(self, request, *args, **kwargs):
        self.serializer_class = ChangeInvoiceSerializer


class POAPIView(RetrieveAPIView):
    queryset = PercacheOrder.objects.all()
    serializer_class = PercacheOrderSerializer

    def get_object(self):
        return get_object_or_404(PercacheOrder, po_number=self.kwargs['po_number'])
