from django.contrib import admin
from .models import EggsModelAudit, EggsModel


@admin.register(EggsModel)
class EggsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen', 'date_created', 'time', 'quantity', 'auth_user')
    list_display_links = ('id', 'pen')
    list_filter = ('date_created', 'pen')
    search_fields = ('id', 'pen', 'date_created')
    list_per_page = 25


@admin.register(EggsModelAudit)
class EggsModelAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen', 'date_created', 'time', 'quantity', 'auth_user', 'action_flag')
    list_display_links = ('id', 'pen')
    list_filter = ('date_created', 'pen')
    search_fields = ('id', 'pen', 'date_created')
    list_per_page = 25
