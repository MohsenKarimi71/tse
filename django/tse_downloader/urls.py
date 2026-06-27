
from django.urls import path, re_path
from . import views

app_name = "tse"

urlpatterns = [
    path('setup/', views.setup_download_tse_excel_data),
    path('download/', views.download_tse_excel_data),
    re_path(r"^save/stock/(?P<directory>[0-9]{8})/(?P<name>[\w.]{11})/$", views.save_stocks_with_options_2db_from_file),
    re_path(r"^save/contract/(?P<directory>[0-9]{8})/(?P<name>[\w.]{11})/$", views.save_new_option_contracts_2db_from_file),
    re_path(r"^save/price/(?P<directory>[0-9]{8})/(?P<name>[\w.]{11})/$", views.save_option_contracts_deal_info_2db_from_file),
    path('delete/stocks/with/contracts/all/', views.delete_all_stocks_with_options),
    re_path(r"^delete/price/(?P<stock_id>[0-9]+)/$", views.delete_stock_contracts_deal_info),
    path("delete/price/all/", views.delete_all_stocks_contracts_deal_info),
    re_path(r"^delete/contracts/expired/(?P<stock_id>[0-9]+)/$", views.delete_stock_expired_contracts),
    re_path(r"^delete/contracts/(?P<stock_id>[0-9]+)/$", views.delete_stock_contracts),
    path("delete/contracts/expired/", views.delete_all_expired_contracts),
    path("delete/contracts/", views.delete_all_contracts),
]
