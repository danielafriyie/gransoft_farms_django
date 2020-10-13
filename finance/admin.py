# from django.contrib import admin
# from .models import PurchasesModel, PurchasesModelAudit
#
#
# @admin.register(PurchasesModel)
# class PurchasesAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'supplier_name', 'phone', 'address', 'invoice_no', 'quantity',
#         'unit_price', 'amount', 'date_created'
#     )
#     list_display_links = ('id', 'supplier_name')
#     list_filter = ('date_created',)
#     search_fields = ('id', 'date_created', 'supplier_name', 'invoice_no')
#     list_per_page = 25
#
#
# @admin.register(PurchasesModelAudit)
# class PurchasesAuditAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'purchase_id', 'supplier_name', 'phone', 'address', 'invoice_no', 'quantity',
#         'unit_price', 'amount', 'date_created'
#     )
#     list_display_links = ('id', 'supplier_name')
#     list_filter = ('date_created',)
#     search_fields = ('id', 'date_created', 'supplier_name', 'invoice_no')
#     list_per_page = 25
