### This file contains constants and variables to download and work on Iran's stock market data files.
import datetime

DOWNLOAD_LINK = "https://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d=0&format=0"
START_TIME = datetime.time(hour=8, minute=30)
END_TIME = datetime.time(hour=12, minute=40)
OPTION_CHAIN = {
    'اهرم':('ضهرم', 'طهرم'),
}
