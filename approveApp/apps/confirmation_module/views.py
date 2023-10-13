from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from apps.confirmation_module.models import Invoice, PercacheOrder, InvoiceItem
from apps.confirmation_module.serializers import InvoiceListSerializer, InvoiceSerializer, PercacheOrderSerializer, \
    ChangeInvoiceSerializer, ChangeInvoiceItemSerializer


class InvoiceListAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer
    pagination_class = LimitOffsetPagination


class InvoiceAPIView(RetrieveUpdateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceSerializer
        if self.request.method == 'PATCH':
            return ChangeInvoiceSerializer

    def get_object(self):
        return get_object_or_404(Invoice, invoice_number=self.kwargs['invoice_number'])


class POAPIView(RetrieveAPIView):
    serializer_class = PercacheOrderSerializer

    def get_object(self):
        return get_object_or_404(PercacheOrder, po_number=self.kwargs['po_number'])


class ChangeInvoiceItemAPIView(UpdateAPIView):
    serializer_class = ChangeInvoiceItemSerializer

    def get_object(self):
        return get_object_or_404(InvoiceItem, id=self.kwargs['id'])
