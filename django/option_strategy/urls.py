from django.urls import path, re_path
from . import views

app_name = "option_strategy"

urlpatterns = [
    path('coveredcall/all/', views.get_all_contracts_covered_call_data, name='all_covered_call'),
    path('bull_call_spread/all/', views.get_all_contracts_bull_call_spread_data, name='all_bull_call_spread'),
]
