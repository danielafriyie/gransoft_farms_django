from django.contrib import admin
from .models import PurchaseModel, PurchaseDetail, PurchaseModelAudit


class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1


@admin.register(PurchaseModel)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created')
    list_display_links = ('id', 'supplier_name')
    list_filter = ('date_created',)
    search_fields = ('id', 'supplier_name', 'invoice_no')
    list_per_page = 25
    inlines = [PurchaseDetailInline]


@admin.register(PurchaseModelAudit)
class PurchasesAuditAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'purchase_id', 'supplier_name', 'phone', 'address',
        'invoice_no', 'date_created', 'quantity', 'unit_price', 'amount'
    )
    list_display_links = ('id', 'supplier_name')
    list_filter = ('date_created',)
    search_fields = ('id', 'supplier_name', 'invoice_no')
    list_per_page = 25
