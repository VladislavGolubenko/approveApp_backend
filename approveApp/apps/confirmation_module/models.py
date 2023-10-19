from django.db import models


class Supplier(models.Model):
    supplier_code = models.CharField(unique=True)
    supplier_name = models.CharField()
    gl_account = models.CharField()


class PercacheOrder(models.Model):
    po_number = models.CharField(unique=True)
    po_date = models.DateField()
    po_amount = models.DecimalField(max_digits=19, decimal_places=2)

    supplier_code = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class Invoice(models.Model):
    invoice_number = models.CharField(unique=True)
    status = models.CharField()
    approvement_level = models.IntegerField()
    file_name = models.CharField()
    invoice_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=19, decimal_places=2)
    department_id = models.IntegerField()
    download_link = models.URLField()

    po_number = models.OneToOneField(PercacheOrder, on_delete=models.CASCADE)
    supplier_code = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    @property
    def new_po_number(self):
        return None

    @new_po_number.setter
    def new_po_number(self, value):
        pass

    @property
    def new_invoice_number(self):
        return None

    @new_invoice_number.setter
    def new_invoice_number(self, value):
        pass


class POItem(models.Model):
    check_box = models.BooleanField(default=False)
    line_number = models.IntegerField()
    product_id = models.CharField()
    product_description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)
    line_price = models.DecimalField(max_digits=19, decimal_places=2)
    unit_type = models.CharField()

    po_number = models.ForeignKey(
        PercacheOrder, related_name='po_items', on_delete=models.CASCADE, null=True, blank=True
    )


class InvoiceItem(models.Model):
    line_number = models.IntegerField()
    product_id = models.CharField()
    product_description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)
    line_price = models.DecimalField(max_digits=19, decimal_places=2)

    matchig_po_line = models.ForeignKey(
        POItem, on_delete=models.SET_NULL, null=True, blank=True
    )

    invoice_number = models.ForeignKey(
        Invoice, related_name='invoice_items', on_delete=models.CASCADE, null=True, blank=True
    )
