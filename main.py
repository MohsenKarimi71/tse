import requests
from openpyxl import Workbook, load_workbook

from variables import DOWNLOAD_LINK
print(DOWNLOAD_LINK) 
### Downloading Data file and Saving it into a File ###

# for i in range(76, 77):
#     name = 'data/14030813-' + str(i) + '.xlsx'
#     print(name)
#     response = requests.get(DOWNLOAD_LINK)

#     output = open(name, 'wb')
#     output.write(response.content)
#     output.close()


### Creating Excel File Using openpyxl Library ###
# wb = Workbook()
# ws1 = wb.create_sheet("data1", 0)
# ws2 = wb.create_sheet("data0", -1)
# ws3 = wb.create_sheet("data2")

# print(wb.sheetnames)

# for sheet in wb:
#     print(sheet.title)

# ws = wb.active
# print("active sheet: ", ws.title)
# ws['A1'] = 50
# ws['B1'] = 78
# ws['C1'] = 35
# ws.cell(row=2, column=1, value="hello!")
# ws.cell(row=2, column=2, value="hello!")
# ws.cell(row=2, column=3, value="hello!")
# wb.save("test.xlsx")

### Reading Data File Using openpyxl Library ###
# wb = load_workbook("data/14030809-001.xlsx")
# sheet = wb.active

# values = []
# for i in range(4, 14):
#     values.append((sheet.cell(row=i, column=1).value, sheet.cell(row=i, column=5).value))

# print(values)