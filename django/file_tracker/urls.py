from django.urls import path, re_path
from . import views

app_name = "file_tracker"

urlpatterns = [
    path('list/', views.get_excel_files_list, name='file_list'),
    re_path(r"^delete/(?P<directory>[0-9]{8})/(?P<name>[\w.]{11})/$", views.delete_excel_file),
]
