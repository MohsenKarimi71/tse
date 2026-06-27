
from django.conf import settings
from openpyxl import load_workbook
import jdatetime
import datetime
import os

from tse_downloader.models import Stock, Option, OptionPrice
from file_tracker.models import ExcelFileInfo


def parse_option_description(text):
    try:
        option, strike_price, expiry_date = text.split("-")
        option_type = option[6:7]
        symbol = option[7:].strip()
        if "/" in expiry_date:
            year, month, day = map(int, expiry_date.split('/'))
        elif len(expiry_date) < 8:
            year = int("14" + expiry_date[:2])
            month = int(expiry_date[2:4])
            day = int(expiry_date[4:])
        else:
            year = int(expiry_date[:4])
            month = int(expiry_date[4:6])
            day = int(expiry_date[6:])
        expiry_date = jdatetime.date(year, month, day).togregorian()
        
        # نگاشت نوع قرارداد
        option_type = "SELL" if option_type == "ف" else "BUY"
        
        return option_type, symbol, strike_price, expiry_date
    except Exception as e:
        print("Error in function 'parse_option_description' >>> " ,str(e), "===> ", text)
        return None

