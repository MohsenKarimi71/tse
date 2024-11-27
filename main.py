import datetime
import sqlite3
import os
from openpyxl import Workbook, load_workbook
import requests

from variables import (
    DOWNLOAD_LINK,
    START_TIME,
    END_TIME
)
from tools import (
    download_excel_data_file,
    save_excel_data_into_database,
    create_table_in_sqlite
)


# create daily directory to store data files
daily_directory_path = os.path.join('tse_excel_data', datetime.date.today().strftime("%Y%m%d"))
os.makedirs(daily_directory_path, exist_ok=True)

counter = 0
### Download data files and Saving it into a File ###
while(END_TIME > datetime.datetime.now().time() > START_TIME and 0):
    file_name = os.path.join(daily_directory_path)
    # print(file_name)

    print("downloading...")
    saved_file_path = download_excel_data_file(daily_directory_path)
    save_excel_data_into_database(saved_file_path)


print("time finished!")



# create_table_in_sqlite('test.db', 'mini1', ['name','count', 'volume', 'value', 'last' ])
save_excel_data_into_database('test.db', 'mini1', os.path.join('tse_excel_data', '20241126', '112044.xlsx'))

sqliteConnection = sqlite3.connect('test.db')
cursor = sqliteConnection.cursor()
result = cursor.execute("SELECT name,count,volume,value,last FROM mini1 ORDER BY value DESC")
for row in result:
    print(row[3],"\t ===> \t", row[0])


# Close the cursor
cursor.close()
if sqliteConnection:
    sqliteConnection.close()