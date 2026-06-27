from django.contrib import admin
from file_tracker.models import ExcelFileInfo



@admin.register(ExcelFileInfo)
class ExcelFileInfoAdmin(admin.ModelAdmin):
    list_display = ('directory', 'name', 'is_contracts_saved', 'is_prices_saved')  # columns in list view
    list_filter = ('directory', 'is_contracts_saved', 'is_prices_saved')  # filter sidebar
