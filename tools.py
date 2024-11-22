### This file contains functions to download and work on Iran's stock market data files.

from variables import DOWNLOAD_LINK 

def download_excel_data_file(save_path, save_name):
    path = save_path + save_name + '.xlsx'
    print(path)
    response = requests.get(DOWNLOAD_LINK)

    output = open(path, 'wb')
    output.write(response.content)
    output.close()
