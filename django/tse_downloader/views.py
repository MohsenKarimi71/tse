from django.shortcuts import render
from django.http import HttpResponse


def download_tse_excel_data(request):
    return HttpResponse("It works!")   
