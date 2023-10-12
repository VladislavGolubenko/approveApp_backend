from rest_framework import serializers
from apps.confirmation_module.models import Invoice, PercacheOrder, POItem, InvoiceItem, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('supplier_name', 'gl_account')


class InvoiceListSerializer(serializers.ModelSerializer):
    supplier_data = SupplierSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ('__all__', 'supplier_data')


class InvoiseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        exclude = ('id', )


class InvoiceSerializer(serializers.ModelSerializer):
    supplier_data = SupplierSerializer(read_only=True)
    items = InvoiseItemSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ('invoice_number', 'invoice_date', 'invoice_amount', 'items', 'supplier_data')


class POItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = POItem
        exclude = ('id', )


class PercacheOrderSerializer(serializers.ModelSerializer):
    supplier_data = SupplierSerializer(read_only=True)
    items = POItemSerializer(read_only=True)

    class Meta:
        model = PercacheOrder
        fields = ('__all__', 'supplier_data', 'items')


class DetailInvoiceSerializer(serializers.Serializer):
    invoice = InvoiceSerializer(read_only=True)
    percache_order = PercacheOrderSerializer(read_only=True)


class ChangeInvoiceSerializer(serializers.ModelSerializer):
    pass
