from django.contrib import admin
from tse_downloader.models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'is_in_option_chain', 'group')  # columns in list view
    list_filter = ('is_in_option_chain', 'group')  # filter sidebar
    search_fields = ('name', 'symbol')     # search box

