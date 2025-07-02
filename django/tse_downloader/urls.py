
from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.setup_download_tse_excel_data),
    path('download/', views.download_tse_excel_data),
    path('save/', views.save_option_contracts_2db_from_excel),
]
