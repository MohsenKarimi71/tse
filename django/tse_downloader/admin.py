from django.contrib import admin
from tse_downloader.models import Stock, Option, OptionPrice, StockPrice


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'is_in_option_chain', 'group')  # columns in list view
    list_filter = ('is_in_option_chain', 'group')  # filter sidebar
    search_fields = ('name', 'symbol')     # search box


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'timestamp')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('stock', 'strike_price', 'expiration_date', 'contract_type')  # columns in list view
    list_filter = ('stock', 'contract_type', 'expiration_date')  # filter sidebar
    search_fields = ('stock', 'contract_type')     # search box


@admin.register(OptionPrice)
class OptionPriceAdmin(admin.ModelAdmin):
    list_display = ('option', 'timestamp', 'last_deal_price', 'buy_bid_price', 'sell_bid_price')
