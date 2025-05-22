from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import datetime
import requests

DOWNLOAD_LINK = "https://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d=0&format=0"
EXCEL_FILES_SAVE_PATH = os.path.join(settings.BASE_DIR, 'excel_files')


daily_directory_path = os.path.join(EXCEL_FILES_SAVE_PATH, datetime.date.today().strftime("%Y%m%d"))
os.makedirs(daily_directory_path, exist_ok=True)


def setup_download_tse_excel_data(request):
    return render(request, "tse_downloader/setup.html")   


def download_tse_excel_data(request):
    """Download the latest excel file from TSETMC, save it on disk and return the saved file's path."""
    path = os.path.join(daily_directory_path, datetime.datetime.now().time().strftime("%H%M%S") + '.xlsx')
    print(path)
    response = requests.get(DOWNLOAD_LINK)

    output = open(path, 'wb')
    output.write(response.content)
    output.close()
    print(path, " downloaded!")

    return render(request, "tse_downloader/setup.html") 