from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from apps.confirmation_module.models import Invoice, PercacheOrder
from apps.confirmation_module.serializers import InvoiceListSerializer, InvoiceSerializer, PercacheOrderSerializer


class InvoiceListAPIView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceListSerializer
    pagination_class = LimitOffsetPagination


class InvoiceAPIView(RetrieveUpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return InvoiceSerializer
    #     if self.request.method == 'PATCH':
    #         return ChangeInvoiceSerializer

    def get_object(self):
        return get_object_or_404(Invoice, invoice_number=self.kwargs['invoice_number'])

    # def patch(self, request, *args, **kwargs):
    #     self.serializer_class = ChangeInvoiceSerializer

    # def put(self, request, pk):
    #     queryset = self.get_object(pk)
    #     serializer = OrderSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class POAPIView(RetrieveAPIView):
    queryset = PercacheOrder.objects.all()
    serializer_class = PercacheOrderSerializer

    def get_object(self):
        return get_object_or_404(PercacheOrder, po_number=self.kwargs['po_number'])
