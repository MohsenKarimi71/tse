from django.urls import path, re_path
from . import views

app_name = "option_strategy"

urlpatterns = [
    path('coveredcall/all/', views.get_all_contracts_covered_call_data, name='all_covered_call'),
]
