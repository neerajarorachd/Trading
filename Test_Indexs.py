from LibDBBase import DBOps
from Dhan_Tradehull import Tradehull


tsl             =   DBOps()
acc_ltp = tsl.get_ltp_data(['BANKNIFTY'])
print(acc_ltp)
"""
get Today's Watchlist -> Check if DB has today's watchlist 
-> No -> Get index historical data -> Get the top index 
-> Get the watchlist of the index 
-> get historical data of watchlist

First Level:
Call Get Historical Momentum data from HW
Add parameter for Watchlist

table for indexes. Date, index, UpCount, DownCount, Last 5 trend
Get all indexes LTP
Get previous day close of all indexes
today change
time stamp of last retreival





Selected Index table
Date, WatchlistID, Index ID, Timestamp, Open, High, Low Close

Store 5 min Intraday data every 5 mins for the selected Index


Store in Index Table



"""