from django.contrib import admin
from tse_downloader.models import Stock, Option


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'is_in_option_chain', 'group')  # columns in list view
    list_filter = ('is_in_option_chain', 'group')  # filter sidebar
    search_fields = ('name', 'symbol')     # search box


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('stock', 'strike_price', 'expiration_date', 'contract_type')  # columns in list view
    list_filter = ('stock', 'contract_type', 'expiration_date')  # filter sidebar
    search_fields = ('stock', 'contract_type')     # search box