from rest_framework import serializers
from apps.confirmation_module.models import Invoice, PercacheOrder, POItem, InvoiceItem


class InvoiceListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    gl_account = serializers.CharField(source='supplier_code.gl_account')

    class Meta:
        model = Invoice
        fields = (
            'invoice_number', 'status', 'approvement_level', 'file_name', 'invoice_date', 'invoice_amount',
            'department_id', 'download_link', 'po_number', 'supplier_code', 'supplier_name', 'gl_account'
        )


class POItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = POItem
        fields = (
            'check_box', 'line_number', 'product_id', 'product_description', 'quantity', 'unit_price', 'line_price',
            'unit_type'
        )


class PercacheOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    gl_account = serializers.CharField(source='supplier_code.gl_account')
    po_items = serializers.SerializerMethodField()

    class Meta:
        model = PercacheOrder
        fields = (
            'po_number', 'po_date', 'po_amount', 'supplier_code', 'po_items',
            'supplier_name', 'gl_account'
        )

    def get_po_items(self, instance):
        items = POItem.objects.filter(po_number=instance.po_number)
        return POItemSerializer(items, many=True).data


class InvoiseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = (
            'line_number', 'product_id', 'product_description', 'quantity', 'unit_price', 'line_price',
            'matchig_po_line'
        )


class InvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    gl_account = serializers.CharField(source='supplier_code.gl_account')
    invoice_items = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = (
            'invoice_number', 'invoice_date', 'invoice_amount',
            'supplier_name', 'gl_account', 'invoice_items', 'po_number'
        )

    def get_invoice_items(self, instance):
        items = InvoiceItem.objects.filter(invoice_number=instance.invoice_number)
        return InvoiseItemSerializer(items, many=True).data
