from django.urls import path, re_path
from . import views

app_name = "option_visualizer"

urlpatterns = [
    path('chain_list/', views.get_option_chain_list, name='option_chain'),
    re_path(r"^contracts/(?P<pk>[0-9]{1,6})/$", views.get_option_contracts, name='option_contracts'),
    path('contracts/all/', views.get_all_options_contracts, name='all_options_contracts'),
]
