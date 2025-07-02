from django.shortcuts import render
from django.conf import settings
import os
import jdatetime
import datetime
import requests
from openpyxl import load_workbook

from tse_downloader.models import Stock, Option
from tse_downloader.tools import parse_option_description


DOWNLOAD_LINK = "https://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d=0&format=0"
EXCEL_FILES_SAVE_PATH = os.path.join(settings.BASE_DIR, 'excel_files')


daily_directory_path = os.path.join(EXCEL_FILES_SAVE_PATH, jdatetime.date.today().strftime("%Y%m%d"))
os.makedirs(daily_directory_path, exist_ok=True)


def setup_download_tse_excel_data(request):
    return render(request, "tse_downloader/setup.html")   


def download_tse_excel_data(request):
    """Download the latest excel file from TSETMC, save it on disk and return the saved file's path."""
    path = os.path.join(daily_directory_path, jdatetime.datetime.now().time().strftime("%H%M%S") + '.xlsx')
    print(path)
    response = requests.get(DOWNLOAD_LINK)

    output = open(path, 'wb')
    output.write(response.content)
    output.close()
    print(path, " downloaded!")

    return render(request, "tse_downloader/setup.html") 


def save_option_contracts_2db_from_excel(request):
    excel_file_path = os.path.join(settings.BASE_DIR,
                                   "excel_files",
                                   "20250613",
                                   "161524.xlsx"
                                )
    wb = load_workbook(excel_file_path)
    sheet = wb.active
    
    # finding excel file last row
    last_row = 3  # starting from row 4
    for row in sheet.iter_rows(min_row=4, min_col=1, max_col=1, values_only=True):
        if row[0] is None:
            break
        last_row += 1

    for row in sheet.iter_rows(min_row=4, min_col=1, max_col=2, max_row=300):
        text = row[1].value
        if('اختيار' in text):
            option_type, symbol, strike_price, expiry_date = parse_option_description(text)
            stock = Stock.objects.get(symbol=symbol)
            # save the Option contract into database if contract is not expired!
            if expiry_date >= datetime.date.today():
                contract_data = {
                    "stock": stock,
                    "strike_price": strike_price,
                    "expiration_date": expiry_date,
                    "contract_type": option_type
                }

                # Try to get the contract or create it if not exists
                Option.objects.get_or_create(**contract_data)

    return render(request, "tse_downloader/setup.html") 

	# # Connect to DB and create a cursor
    # sqliteConnection = sqlite3.connect(db)

    # # Get cursor
    # cursor = sqliteConnection.cursor()
    # query = "INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?)"
    # cursor.executemany(query, new_rows)
    # sqliteConnection.commit()
    
    # if sqliteConnection:
    #     sqliteConnection.close()
    # print("data saved!!!")
