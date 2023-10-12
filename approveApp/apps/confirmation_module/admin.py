from django.contrib import admin
from .models import Invoice, InvoiceItem, Supplier, POItem, PercacheOrder


class InvoiceAdmin(admin.ModelAdmin):
    pass


class InvoiceItemAdmin(admin.ModelAdmin):
    pass


class SupplierAdmin(admin.ModelAdmin):
    pass


class POItemAdmin(admin.ModelAdmin):
    pass


class PercacheOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(POItem, POItemAdmin)
admin.site.register(PercacheOrder, PercacheOrderAdmin)
