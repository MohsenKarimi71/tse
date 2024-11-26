import datetime
import os
from openpyxl import Workbook, load_workbook
import requests

from variables import DOWNLOAD_LINK, START_TIME, END_TIME
from tools import download_excel_data_file


# create daily directory to store data files
daily_directory_path = os.path.join('tse_excel_data', datetime.date.today().strftime("%Y%m%d"))
os.makedirs(daily_directory_path, exist_ok=True)

counter = 0
### Download data files and Saving it into a File ###
while(END_TIME > datetime.datetime.now().time() > START_TIME):
    if(counter < 3):
        file_name = os.path.join(daily_directory_path)
        # print(file_name)

        print("downloading...")
        download_excel_data_file(daily_directory_path)
        counter=+1

print("time finished!")


