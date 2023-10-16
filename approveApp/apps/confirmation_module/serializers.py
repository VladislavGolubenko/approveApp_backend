from rest_framework import serializers
from apps.confirmation_module.models import Invoice, PercacheOrder, POItem, InvoiceItem, Supplier


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
    po_items = POItemSerializer(many=True, read_only=True)
    total_po_items = serializers.SerializerMethodField(method_name='get_total_po_items')

    class Meta:
        model = PercacheOrder
        fields = (
            'po_number', 'po_date', 'po_amount', 'supplier_code', 'po_items',
            'supplier_name', 'gl_account', 'total_po_items'
        )

    def get_total_po_items(self, instance):
        total = PercacheOrder.objects.filter(po_number=instance.po_number).count()
        return total


class InvoiseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = (
            'id', 'line_number', 'product_id', 'product_description', 'quantity', 'unit_price', 'line_price',
            'matchig_po_line'
        )


class InvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    gl_account = serializers.CharField(source='supplier_code.gl_account')
    invoice_items = InvoiseItemSerializer(many=True, read_only=True)
    total_invoice_items = serializers.SerializerMethodField(method_name='get_total_invoice_items')

    class Meta:
        model = Invoice
        fields = (
            'invoice_number', 'invoice_date', 'invoice_amount', 'supplier_code',
            'supplier_name', 'gl_account', 'invoice_items', 'po_number', 'total_invoice_items'
        )

    def get_total_invoice_items(self, instance):
        total = InvoiceItem.objects.filter(invoice_number=instance.invoice_number).count()
        return total


class ChangeInvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField()
    gl_account = serializers.CharField()

    def update(self, instance, validated_data):
        if suplier_instance := validated_data['supplier_code']:
            suplier_instance.supplier_name = validated_data['supplier_name']
            suplier_instance.gl_account = validated_data['gl_account']
            suplier_instance.save()
            del validated_data['supplier_code']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = (
            'invoice_date', 'invoice_amount', 'supplier_code', 'supplier_name', 'gl_account'
        )


class ChangeInvoiceItemSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = InvoiceItem
        fields = (
            'line_number', 'product_id', 'product_description', 'quantity', 'unit_price', 'line_price',
            'matchig_po_line'
        )
