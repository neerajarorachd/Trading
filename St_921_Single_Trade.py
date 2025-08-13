import pdb
import time
from datetime import datetime
import traceback
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
from LibFinance import FinLib
from LibAnalysis import AnaLysisLib
from LibGeneric import GeneicLib

str_Client_Code =   "1106451789"
str_Token_ID    =   "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ2ODUyNjg2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.tyAOEhC8dQtoQUhCabZdPIfhOa72w-heAVXLld79myY5W97-ai-xeq2Y94tc_OIFMflv-F8k76Hu4tMH9OpZbQ"
tsl             =   Tradehull(str_Client_Code,str_Token_ID)
FLib            =   FinLib()
ALib            =   AnaLysisLib()
GLib            =   GeneicLib()

str_Start_Time  =   "09:21:15"
str_End_Time    =   "09:59:00" #format must be HH:MM:SS - Correct 09:, wrong 9:
str_Time_Format =   "%H:%M:%S"
str_Symbol      =   "HINDCOPPER" #"NLCINDIA" #"BANKBARODA" #"ETERNAL" #"NALCO" #"HINDCOPPER" "JIOFIN" "BHEL"
str_High        =   "high"
str_Close       =   "close"
str_open        =   "open"
flt_SL_Pers     =   0.0025
flt_Target_Pers =   0.008
flt_Trail_Pers  =   0.005
flt_Target_price      =   0
flt_SL_price    =   0
flt_Trade_Price =   0.0
flt_Expenses    =   0.25
int_ctr         =   0
int_Qty         =   1
str_Order_ID    = ''
str_SL_Order_ID = ''
str_Target_Order_ID = ''
str_NSE         =   'NSE'
str_MARKET      =   'MARKET'
str_LIMIT       =   'LIMIT'
str_STOPLIMIT   =   'STOPLIMIT'
str_STOPLOSS    =   'STOPMARKET'
str_BUY         =   'BUY'
str_SELL        =   'SELL'
str_INTRADAY    =   'MIS'
str_TRANSIT     =   'TRANSIT'
str_PENDING     =   'PENDING'
str_TRADED      =   'TRADED'
str_Closing_Type  =   str_BUY
int_Entry_Flag  =   0
int_Exit_Flag   =   0
flt_LST         =   0.0
Watchlist_Refined = pd.DataFrame()

#print script start time
curr_time = datetime.now().strftime(str_Time_Format)
print("\nScript started at " + str(curr_time))

#flt_LST             =   tsl.get_ltp_data(names = [str_Symbol])[str_Symbol]

#exp = FLib.Expenses(1000,220)
#print(str(exp))


def CreateSingleOrder(Symbol, Exchange, Qty, Price, TriggerPrice, OrderType, TransactionType, TradeType):
    return tsl.order_placement(tradingsymbol=Symbol ,exchange=Exchange, quantity=Qty, price=Price, trigger_price=TriggerPrice, order_type=OrderType, transaction_type=TransactionType,   trade_type=TradeType)


def buy_single_order():
    print("buy")
    global str_Order_ID, str_SL_Order_ID, str_Target_Order_ID, str_Closing_Type, flt_LST

    str_Order_ID        =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, 0,0, str_MARKET, str_BUY, str_INTRADAY) 
    flt_LST             =   tsl.get_executed_price(orderid=str_Order_ID)
    flt_SL_price        =   flt_LST - (flt_LST*flt_SL_Pers)
    str_SL_Order_ID     =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, 0, flt_SL_price, str_STOPLOSS, str_SELL, str_INTRADAY)
    flt_Expenses        =   FLib.Expenses(int_Qty, flt_LST) / int_Qty
    flt_Target_price    =   flt_LST + (flt_Expenses) + (flt_LST * flt_Target_Pers)
    str_Target_Order_ID =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, flt_Target_price, 0, str_LIMIT, str_SELL, str_INTRADAY)
    str_Closing_Type    =   str_SELL


def sell_single_order():
    print("Sell")
    global str_Order_ID, str_SL_Order_ID, str_Target_Order_ID, str_Closing_Type, flt_LST

    str_Order_ID          =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, 0,0, str_MARKET, str_SELL, str_INTRADAY) 
    flt_LST               =   tsl.get_executed_price(orderid=str_Order_ID)
    flt_SL_price          =   flt_LST + (flt_LST*flt_SL_Pers)
    str_SL_Order_ID       =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, 0, flt_SL_price, str_STOPLOSS, str_BUY, str_INTRADAY)
    flt_Expenses          =   FLib.Expenses(int_Qty, flt_LST) / int_Qty
    flt_Target_price      =   flt_LST - (flt_Expenses + (flt_LST * flt_Target_Pers))
    str_Target_Order_ID   =   CreateSingleOrder(str_Symbol, str_NSE, int_Qty, flt_Target_price, 0, str_LIMIT, str_BUY, str_INTRADAY)
    str_Closing_Type      =   str_BUY


def cancel_single_order(CancelOrderID):
    
    Order_status  = tsl.get_order_status(orderid=CancelOrderID)
    if Order_status== str_TRANSIT or Order_status== str_PENDING:
        tsl.cancel_order(OrderID=CancelOrderID)

def Enter_921():
    global int_Entry_Flag
    chart = pd.DataFrame()

    curr_time = datetime.now().strftime(str_Time_Format)   
    
    if curr_time >= str_Start_Time and int_Entry_Flag==0:
        chart = tsl.get_intraday_data(str_Symbol, 'NSE', 3)
        
        Uptrend = Downtrend = False

        if not chart.empty:
            # Uptrend = chart[str_High].iloc[-1] > chart[str_High].iloc[-2]  and chart[str_High].iloc[-2] > chart[str_High].iloc[-3]
            # Downtrend = chart[str_High].iloc[-1] < chart[str_High].iloc[-2]  and chart[str_High].iloc[-2] < chart[str_High].iloc[-3]
            Uptrend = chart[str_Close].iloc[-1] > chart[str_open].iloc[-1]  and chart[str_Close].iloc[-2] > chart[str_open].iloc[-2]
            Downtrend = chart[str_Close].iloc[-1] < chart[str_open].iloc[-1]  and chart[str_Close].iloc[-2] < chart[str_open].iloc[-2]
            #if Uptrend and touched the bolinger upper band, reversal is expected. create order with a least stop loss
        else:    
            int_Entry_Flag = 2
        if Uptrend:
            buy_single_order()
            int_Entry_Flag = 1
            print("\n" + str(int_Qty) + " " + str_Symbol + " bought @" + str(flt_LST) + " at " + str(curr_time))
        elif Downtrend:
            sell_single_order()
            int_Entry_Flag = 1
            print("\n" + str(int_Qty) + " " + str_Symbol + " sold @" + str(flt_LST) + " at " + str(curr_time))




def exit_921():
    #print("Morning time finished at 9:25")
    global int_Exit_Flag
    Executed_Price = ""

    curr_time = datetime.now().strftime(str_Time_Format)  
    SLorder_status  = tsl.get_order_status(orderid=str_SL_Order_ID)
    Target_Order_Status = tsl.get_order_status(orderid=str_Target_Order_ID)
    #order_price   = tsl.get_executed_price(orderid=82241218256027)
    
    if SLorder_status == str_TRADED:
        cancel_single_order(str_Target_Order_ID)
        Executed_Price = tsl.get_executed_price(orderid=str_SL_Order_ID)
        print("\nSL Hit at "  + str(curr_time) + " @" + str(Executed_Price))
        int_Exit_Flag = 1
    elif Target_Order_Status == str_TRADED:
        cancel_single_order(str_SL_Order_ID)
        Executed_Price = tsl.get_executed_price(orderid=str_Target_Order_ID)
        print("\nTarget Hit at " + str(curr_time) + " @" + str(Executed_Price))
        int_Exit_Flag = 1
    elif curr_time >= str_End_Time and int_Exit_Flag==0:
        #Close the position
        str_Timeout_Order_ID = CreateSingleOrder(str_Symbol, str_NSE,int_Qty, 0, 0, str_MARKET, str_Closing_Type, str_INTRADAY)
        Executed_Price = tsl.get_executed_price(orderid=str_Timeout_Order_ID)
        print("\nExit Time Hit at " + str(curr_time))
        print("\n" + str_Closing_Type + " @" + str(Executed_Price))
        cancel_single_order(str_SL_Order_ID)
        cancel_single_order(str_Target_Order_ID)
        print("\n Both order legs cancelled")
        int_Exit_Flag = 1

while True:
    int_Entry_Flag = 0

    Enter_921()
    
    if int_Entry_Flag == 1:
        break
    if int_Entry_Flag == 2:
        int_Entry_Flag = 0
        break


#Exit Loop
while True:
    int_Exit_Flag = 0
    if int_Entry_Flag==1:
        exit_921()

    if int_Exit_Flag == 1 or int_Entry_Flag==0:
        break


# From While loop call Entry function
# Call function to get the watchlist
# Call Get Momentum Data to refine the watchlist. Store the momentum list in a file for future analysis after profit/Loss
# Call Two Sisters Candle function to get the final list
# If list is not empty create orders
# Before each order, check the following:
# day's loss is less than Max Loss
# Trade count is less than Max Trade count
# available money, 
# margin money, 
# calculate per share price
# Available money / per share price = available qty
# if available qty / 2 (target qty = order qty) > Max allowed qty then order Max qty otherwise order the available qty
# Symbol, Buy/Sell, TotalValue, OrderID, OrderPrice, OrderQty, StopLossPrice, StopLossOrderID, TargetPrice, TargetOrderID, OrderExpenses, FinalExecutedPrice, Profit/Loss, Status
#       (Active/Completed/Cancelled), ClosingTrade Source (TargetHit/SLHit/TimeOver/ManuallyClosed)
# On buy, set buy expenses, on sell add selling expenses
# Exit Loop
# Loop the list from two sisters candle function
# If Status is completed, continue
# If status is active, check current status of both legs
# If closed, the cancel another leg and update the status as completed
# Count active orders. if active count is 0, set exit = true
# Store the list in a file with date stamp. best part should be, combine the result with the momentum list for further analysis

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



