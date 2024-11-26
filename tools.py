### This file contains functions to download and work on Iran's stock market data files.
import os
import datetime
import requests

from variables import DOWNLOAD_LINK 


def download_excel_data_file(daily_path):
    path = os.path.join(daily_path, datetime.datetime.now().time().strftime("%H%M%S") + '.xlsx')
    response = requests.get(DOWNLOAD_LINK)

    output = open(path, 'wb')
    output.write(response.content)
    output.close()
    print(path, " downloaded!")


def save_excel_data_into_database(excel_path):
    pass


