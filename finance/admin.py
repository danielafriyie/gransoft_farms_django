from django.contrib import admin
from .models import FinanceModel, ItemDetail, FinanceModelAudit


class ItemDetailInline(admin.TabularInline):
    model = ItemDetail
    extra = 1


@admin.register(FinanceModel)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_name', 'phone', 'address', 'invoice_no', 'category', 'date_created')
    list_display_links = ('id', 'supplier_name')
    list_filter = ('date_created', 'category')
    search_fields = ('id', 'supplier_name', 'invoice_no')
    list_per_page = 25
    inlines = [ItemDetailInline]


@admin.register(FinanceModelAudit)
class FinanceAuditAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'item_id', 'supplier_name', 'phone', 'address',
        'invoice_no', 'category', 'date_created', 'quantity', 'unit_price', 'amount'
    )
    list_display_links = ('id', 'supplier_name')
    list_filter = ('date_created', 'category')
    search_fields = ('id', 'supplier_name', 'invoice_no')
    list_per_page = 25
