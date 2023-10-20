from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from apps.confirmation_module.models import Invoice, PercacheOrder, Supplier
from apps.confirmation_module.serializers import InvoiceListSerializer, InvoiceSerializer, PercacheOrderSerializer, \
    ChangeInvoiceSerializer, SuppliersListSerializer


class InvoiceListAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer
    pagination_class = LimitOffsetPagination


class InvoiceAPIView(RetrieveUpdateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceSerializer
        if self.request.method in ('PATCH', 'PUT'):
            return ChangeInvoiceSerializer

    def get_object(self):
        return get_object_or_404(Invoice, id=self.kwargs['id'])


class POAPIView(RetrieveAPIView):
    serializer_class = PercacheOrderSerializer

    def get_object(self):
        return get_object_or_404(PercacheOrder, po_number=self.kwargs['po_number'])


class SupplierListAPIView(ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SuppliersListSerializer
