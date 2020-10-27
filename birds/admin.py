from django.contrib import admin

from .models import (
    PenHouse, BirdsStock, MedicineFeed, MortalityCull
)


@admin.register(PenHouse)
class PenHouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen_number', 'date_created', 'pen_name')
    list_display_links = ('id', 'pen_number')
    list_filter = ('date_created',)
    search_fields = ('id', 'pen_number', 'pen_name')
    list_per_page = 25


@admin.register(BirdsStock)
class BirdsStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen_house', 'date_created', 'invoice_no', 'quantity')
    list_display_links = ('id', 'pen_house')
    list_filter = ('date_created',)
    search_fields = ('id', 'pen_house', 'invoice_no')
    list_per_page = 25


@admin.register(MedicineFeed)
class MedicineFeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen_house', 'date_created', 'category')
    list_display_links = ('id', 'pen_house')
    list_filter = ('date_created', 'category')
    search_fields = ('id', 'pen_house')
    list_per_page = 25


@admin.register(MortalityCull)
class MortalityCullAdmin(admin.ModelAdmin):
    list_display = ('id', 'pen_house', 'date_created', 'category')
    list_display_links = ('id', 'pen_house')
    list_filter = ('date_created', 'category')
    search_fields = ('id', 'pen_house')
    list_per_page = 25
