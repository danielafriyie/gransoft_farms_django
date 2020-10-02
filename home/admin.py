from django.contrib import admin
from .models import CompanyConfig


@admin.register(CompanyConfig)
class CompanyConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'location', 'contact', 'date_created')
    list_display_links = ('id', 'name')
    list_filter = ('date_created',)
    search_fields = ('id', 'name', 'email', 'address')
    list_per_page = 25
