import pdb
import time
from datetime import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib


client_code = "1106451789"
token_id    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ2ODUyNjg2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.tyAOEhC8dQtoQUhCabZdPIfhOa72w-heAVXLld79myY5W97-ai-xeq2Y94tc_OIFMflv-F8k76Hu4tMH9OpZbQ"
tsl         = Tradehull(client_code,token_id)
ctr = 0

"""
while True:
    ts = time.time()
    all_ltp_data   = tsl.get_ltp_data(names = ['NIFTY 17 APR 25400 CALL', 'NIFTY 17 APR 25400 PUT', "ACC", "CIPLA"])
    acc_ltp = all_ltp_data['ACC']
    ce_ltp = all_ltp_data['NIFTY 17 APR 25400 CALL']
    pe_ltp  = all_ltp_data['NIFTY 17 APR 25400 PUT']
    print("\nRound " + str(ctr+1) + "\n" )
    print(ts)
    print("\n")
    print(acc_ltp)
    print(pe_ltp)
    print(ce_ltp)
    ctr= ctr + 1
    if ctr==5:
        break
"""
#stock_name = 'NIFTY'
#ltp   = tsl.get_ltp_data(names = [stock_name])[stock_name]
#print(ltp)

#chart = tsl.get_historical_data(tradingsymbol = 'NIFTY',  exchange = 'INDEX',timeframe="DAY")
#chart = tsl.get_historical_data(tradingsymbol = 'BANKBARODA',  exchange = 'NSE',timeframe="DAY")
#df = pd.DataFrame(chart)
#df.to_csv("Bank of Baroda")
#print(df)

# positions = tsl.get_positions()
# orderbook = tsl.get_orderbook()
# orderbook.to_csv("orderbook.csv")
# tradebook = tsl.get_trade_book()
# holdings = tsl.get_holdings()
# pnl = tsl.get_live_pnl()

# print("\n Positions \n")
# print(positions)
# print("\n P&L \n")
# print(pnl)
# print("\n Order Book \n")
# print(orderbook)
# print("\n Trade Book \n")
# print(tradebook)
# print("\n Holdings \n")
# print(holdings)

#acc_ltp = tsl.get_ltp_data['BANKBARODA']
#entry_orderid  = tsl.order_placement(tradingsymbol='BANKBARODA' ,exchange='NSE', quantity=1, price=0, trigger_price=0,    order_type='MARKET',     transaction_type='SELL',   trade_type='MIS')
#sl_orderid     = tsl.order_placement(tradingsymbol='ACC' ,exchange='NSE', quantity=1, price=0, trigger_price=235, order_type='STOPMARKET', transaction_type ='BUY', trade_type='MIS')
#sl_orderid     = tsl.order_placement(tradingsymbol='BANKBARODA' ,exchange='NSE', quantity=1, price=0, trigger_price=235, order_type='STOPMARKET', transaction_type ='BUY', trade_type='MIS')
#modified_order = tsl.modify_order(order_id=sl_orderid,order_type="STOPLIMIT",quantity=1,price=236,trigger_price=237)
#tsl.cancel_all_orders()

#margin = tsl.margin_calculator(tradingsymbol='ACC', exchange='NSE', transaction_type='BUY', quantity=2, trade_type='MIS', price=2180, trigger_price=0)

#print(margin)
curr_time = datetime.now().strftime("%H:%M:%S")
print(curr_time)

chart = tsl.get_intraday_data('BANKBARODA', 'NSE', 3)
Uptrend = chart["high"].iloc[-1] > chart["high"].iloc[-2]
Downtrend = chart["high"].iloc[-1] < chart["high"].iloc[-2]
orderid = 0
slorderid = 0

print(Downtrend)

def buy_order():
    print("buy")
    orderid = 0
    slorderid = 0
def sell_order():
    print("Sell")
    orderid = 0
    slorderid = 0
def cancel_pending_sl_order():
    print("Cancel")
    #get SL order status
    #if order is pending
    #cancel SL order
def entry_time_921():
    print("9:21 Time started")
    if Uptrend:
        buy_order()
    if Downtrend:
        sell_order()

    #get the direction from last 3 candles
    #Create order
    #create SL order


def exit_time_921():
    print("Morning time finished at 9:25")
    #get status of the order
    #if order is active, close the order, cancel SL order


while True:
    curr_time = datetime.now().strftime("%H:%M:%S")
    entry_flag = 0
    if curr_time >= "09:21:15" and entry_flag==0:
        if Uptrend:
            buy_order()
        if Downtrend:
            sell_order()
        entry_flag = 1
    if entry_flag == 1:
        break


while True:
    curr_time = datetime.now().strftime("%H:%M:%S")
    exit_flag = 0
    order_status = 0
    if order_status == 0:
        exit_flag = 1
        break
    if curr_time >= "09:25:00" and exit_flag==0:
        exit_time_921()
        exit_flag = 1
    if exit_flag == 1:
        break



    


#chart = tsl.get_intraday_data('BANKBARODA', 'NSE', 1)
#chart['rsi'] = talib.RSI(chart['close'], timeperiod=14) #pandas
#chart[''] = talib
#print(chart)
#print(chart['rsi'])

""" all_ltp_data   = tsl.get_ltp_data(names = ['NIFTY 17 APR 25400 CALL', 'NIFTY 17 APR 25400 PUT', "ACC", "CIPLA"])
acc_ltp = all_ltp_data['ACC']
pe_ltp  = all_ltp_data['NIFTY 19 DEC 24000 PUT']



stock_name = 'NIFTY'
ltp   = tsl.get_ltp_data(names = [stock_name])[stock_name]




chart = tsl.get_historical_data(tradingsymbol = 'NIFTY',  exchange = 'INDEX',timeframe="DAY")
data  = tsl.get_historical_data(tradingsymbol = 'NIFTY 19 DEC 24000 CALL'     ,exchange = 'NFO'  ,timeframe="15")



order_status  = tsl.get_order_status(orderid=82241218256027)
order_price   = tsl.get_executed_price(orderid=82241218256027)
order_time    = tsl.get_exchange_time(orderid=82241218256027)


positions = tsl.get_positions()
orderbook = tsl.get_orderbook()
tradebook = tsl.get_trade_book()
holdings = tsl.get_holdings()


ce_name, pe_name, strike = tsl.ATM_Strike_Selection(Underlying='NIFTY', Expiry=0)


ce_name, pe_name, ce_strike, pe_strike = tsl.OTM_Strike_Selection(Underlying='NIFTY', Expiry=0, OTM_count=3)

ce_name, pe_name, ce_strike, pe_strike = tsl.ITM_Strike_Selection(Underlying='NIFTY', Expiry=0, ITM_count=5)

# Equity
entry_orderid  = tsl.order_placement(tradingsymbol='ACC' ,exchange='NSE', quantity=1, price=0, trigger_price=0,    order_type='MARKET',     transaction_type='BUY',   trade_type='MIS')
sl_orderid     = tsl.order_placement(tradingsymbol='ACC' ,exchange='NSE', quantity=1, price=0, trigger_price=2200, order_type='STOPMARKET', transaction_type ='SELL', trade_type='MIS')

# Options
entry_orderid  = tsl.order_placement(tradingsymbol='NIFTY 19 DEC 24400 CALL' ,exchange='NFO', quantity=50, price=0, trigger_price=0, order_type='MARKET', transaction_type='BUY', trade_type='MIS')
sl_orderid     = tsl.order_placement(tradingsymbol='NIFTY 19 DEC 24400 CALL' ,exchange='NFO', quantity=25, price=29, trigger_price=30, order_type='STOPLIMIT', transaction_type='SELL', trade_type='MIS')

modified_order = tsl.modify_order(order_id=sl_orderid,order_type="STOPLIMIT",quantity=50,price=29,trigger_price=30)

order_ids      = tsl.place_slice_order(tradingsymbol="NIFTY 19 DEC 24400 CALL",   exchange="NFO",quantity=5000, transaction_type="BUY",order_type="LIMIT",trade_type="MIS",price=0.05)



margin = tsl.margin_calculator(tradingsymbol='ACC', exchange='NSE', transaction_type='BUY', quantity=2, trade_type='MIS', price=2180, trigger_price=0)

margin = tsl.margin_calculator(tradingsymbol='NIFTY 19 DEC 24400 CALL', exchange='NFO', transaction_type='SELL', quantity=25, trade_type='MARGIN', price=43, trigger_price=0)

margin = tsl.margin_calculator(tradingsymbol='NIFTY 19 DEC 24400 CALL', exchange='NFO', transaction_type='BUY', quantity=25, trade_type='MARGIN', price=43, trigger_price=0)
margin = tsl.margin_calculator(tradingsymbol='NIFTY DEC FUT', exchange='NFO', transaction_type='BUY', quantity=25, trade_type='MARGIN', price=24350, trigger_price=0)


exit_all       = tsl.cancel_all_orders()
 """



