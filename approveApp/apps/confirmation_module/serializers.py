from django.db import transaction
from rest_framework import serializers
from apps.confirmation_module.models import Invoice, PercacheOrder, POItem, InvoiceItem, Supplier


class InvoiceListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    gl_account = serializers.CharField(source='supplier_code.gl_account')

    class Meta:
        model = Invoice
        fields = (
            'id', 'invoice_number', 'status', 'approvement_level', 'file_name', 'invoice_date', 'invoice_amount',
            'department_id', 'download_link', 'po_number', 'supplier_code', 'supplier_name', 'gl_account'
        )


class POItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = POItem
        fields = (
            'id', 'check_box', 'line_number', 'product_id', 'product_description', 'quantity', 'unit_price',
            'line_price', 'unit_type'
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
            'id', 'line_number', 'product_id', 'product_description', 'quantity', 'unit_price',
            'line_price', 'matchig_po_line'
        )


class InvoiceSerializer(serializers.ModelSerializer):
    # supplier_id = serializers.CharField(source='supplier_code.id')
    # supplier_name = serializers.CharField(source='supplier_code.supplier_name')
    # gl_account = serializers.CharField(source='supplier_code.gl_account')
    po_data = serializers.CharField(source='po_number.po_number')
    invoice_items = InvoiseItemSerializer(many=True, read_only=True)
    total_invoice_items = serializers.SerializerMethodField(method_name='get_total_invoice_items')
    supplier_data = serializers.SerializerMethodField(method_name='get_supplier_data')

    class Meta:
        model = Invoice
        fields = (
            'id', 'invoice_number', 'invoice_date', 'invoice_amount', 'file_name', 'status', 'po_data',
            'invoice_items', 'total_invoice_items', 'supplier_data'
        )

    def get_total_invoice_items(self, instance):
        total = InvoiceItem.objects.filter(invoice_number=instance.invoice_number).count()
        return total

    def get_supplier_data(self, instance):
        supplier = instance.supplier_code
        return {
            'id': supplier.id,
            'gl_account': supplier.gl_account,
            'supplier_name': supplier.supplier_name
        }


class ChangeInvoiceSerializer(serializers.ModelSerializer):
    invoice_items = InvoiseItemSerializer(many=True, read_only=True)
    new_po_number = serializers.CharField()
    new_invoice_number = serializers.CharField()

    @property
    def data(self):
        _ = super().data
        serializer = InvoiceSerializer(instance=self.instance)
        return serializer.data

    @staticmethod
    def _delete_items(instance, validated_data, inv_number):
        InvoiceItem.objects.filter(invoice_number=instance.id).delete()
        instance.invoice_number = inv_number
        del validated_data['new_invoice_number']
        if validated_data.get('invoice_number'):
            del validated_data['invoice_number']

    @staticmethod
    def _update_items(items_data):
        update_items = []
        for item in items_data:
            obj = InvoiceItem.objects.get(id=item['id'])
            obj.line_number = item['line_number']
            obj.product_id = item['product_id']
            obj.product_description = item['product_description']
            obj.quantity = item['quantity']
            obj.unit_price = item['unit_price']
            obj.line_price = item['line_price']
            obj.matchig_po_line = POItem.objects.get(pk=item['matchig_po_line'])
            update_items.append(obj)

        InvoiceItem.objects.bulk_update(
            update_items,
            ['line_number', 'product_id', 'product_description', 'quantity', 'unit_price', 'line_price',
             'matchig_po_line']
        )

    @staticmethod
    def _update_po(validated_data, po_obj, po_numb):
        po_obj.po_number = po_numb
        po_obj.save()
        del validated_data['new_po_number']

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = self.initial_data.get('invoice_items')

        if inv_number := validated_data.get('new_invoice_number'):
            self._delete_items(instance, validated_data, inv_number)
        else:
            if items_data:
                self._update_items(items_data)

        if po_numb := validated_data.get('new_po_number'):
            if po_obj := instance.po_number:
                self._update_po(validated_data, po_obj, po_numb)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Invoice
        fields = (
            'invoice_date', 'invoice_amount', 'invoice_items', 'new_po_number', 'new_invoice_number', 'supplier_code'
        )


class SuppliersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'id', 'supplier_name'
        )

