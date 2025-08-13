from LibTrading import TradingLib
from datetime import datetime
from LibConstants import Const
from LibEnum import TradingEnums as TE
from LibFinance import FinLib
from LibDBOps import DBOps
from LibGeneric import GeneicLib as GL
import subprocess
import json
#import debugpy
import time
from LibDhan import Dhan
from ClassStrategyBase import Strategy

# Allow time to attach debugger (optional)
""" print("Waiting for debugger to attach...")
debugpy.listen(("127.0.0.1", 5678))  # You can use a different port if needed
debugpy.wait_for_client()  # Pauses until debugger is attached
print("Debugger attached.") """


#create objects
TrLib           =   TradingLib()
FLib            =   FinLib()
DH              = Dhan()
tsl             =   DH.DhanConnection
int_Exit_Flag   =   0


#monitor Morning 921
def IsActive(WatchlistRow):
    str_SL_Order_ID = WatchlistRow['SLOrderID']
    str_Target_Order_ID = WatchlistRow['TargetOrderID']
    SLorder_status = None
    Target_Order_Status = None
    ClosingSource = TE.TradeClosingSource.NotPlaced
    columns = ['Active', 'ClosingSource', 'ExecutedPrice']
    DL = {col: None for col in columns}

    curr_time = datetime.now().strftime(Const.Time_Format) 
    if str_SL_Order_ID != 0:
        SLorder_status  = tsl.get_order_status(orderid=str_SL_Order_ID)
    if str_Target_Order_ID != 0:
        Target_Order_Status = tsl.get_order_status(orderid=str_Target_Order_ID)
    
    #order_price   = tsl.get_executed_price(orderid=82241218256027)
    if (SLorder_status == TE.OrderStatus.CANCELLED.name or SLorder_status == TE.OrderStatus.REJECTED.name) and \
        (Target_Order_Status == TE.OrderStatus.CANCELLED.name or Target_Order_Status == TE.OrderStatus.REJECTED.name) \
            and WatchlistRow["TradeStatus"] != TE.TradeStatus.Completed \
                : 
        #Manually closed
        DL["ClosingSource"] = TE.TradeClosingSource.ManuallyClosed
        DL["Active"] =   False
    elif SLorder_status == TE.OrderStatus.TRADED.name and WatchlistRow["TradeStatus"] != TE.TradeStatus.Completed:
        TrLib.CancelOrder(tsl, str_Target_Order_ID)
        DL["ExecutedPrice"] = tsl.get_executed_price(orderid=str_SL_Order_ID)
        DL["Active"] =   False
        #PnL = FLib.PnLWithExpenses(WatchlistRow['OrderQty'], WatchlistRow['OrderPrice'], Executed_Price)
        
        DL["ClosingSource"] = TE.TradeClosingSource.SLHit
        #print("\nSL Hit at "  + str(curr_time) + " @" + str(Executed_Price))
    elif Target_Order_Status == TE.OrderStatus.TRADED.name and WatchlistRow["TradeStatus"] != TE.TradeStatus.Completed:
        TrLib.CancelOrder(tsl, str_SL_Order_ID)
        DL["ExecutedPrice"] = tsl.get_executed_price(orderid=str_Target_Order_ID)
        #PnL = FLib.PnLWithExpenses(WatchlistRow['OrderQty'], WatchlistRow['OrderPrice'], Executed_Price)
        DL["Active"] =   False
        DL["ClosingSource"] = TE.TradeClosingSource.TargetHit
        #print("\nTarget Hit at " + str(curr_time) + " @" + str(Executed_Price))
    # elif curr_time >= Const.End_Time_921 and int_Exit_Flag==0 and WatchlistRow["TradeStatus"] != TE.TradeStatus.Completed:
    #     #Close the position
    #     #str_Timeout_Order_ID = CreateSingleOrder(str_Symbol, str_NSE,int_Qty, 0, 0, str_MARKET, str_Closing_Type, str_INTRADAY)
    #     DLOrder = TrLib.Order(tsl, TE.Strategy.Morning921, TE.Watchlist_Type.NONE, WatchlistRow['SYMBOL'], False, 0, TE.Exchange.NSE, TE.OrderGroupType.MARKET,WatchlistRow['BalanceQty'],TE.TradeType.MIS, TE.CallType.NA, TE.OrderDirection(WatchlistRow['OrderClosingType']),0, 0,0, 0, 0, WatchlistRow['OrderID'])
        
    #     TrLib.CancelOrder(tsl, str_SL_Order_ID)
    #     TrLib.CancelOrder(tsl, str_Target_Order_ID)
    #     DL["ClosingSource"] = TE.TradeClosingSource.TimeOut
    #     DL["ExecutedPrice"] = DLOrder["OrderPrice"]
    #     DL["Active"] =   False
    else:
        DL["Active"] =   True
    
    return DL
#===============================================================================================================

#Update Record
def UpdateDBRecord(DLWatchlist):
    #Current time
    curr_time = datetime.now().strftime(Const.Time_Format) 

    #PnL
    if DLWatchlist["TradeClosingSource"] == TE.TradeClosingSource.ManuallyClosed:
        PnL = FLib.PnLWithExpenses(DLWatchlist['OrderInQty'], DLWatchlist["BalanceQty"], DLWatchlist['OrderPrice'], DLWatchlist['OrderPrice']) #Source order was a buy order
    else:
        if(TE.OrderDirection(DLWatchlist['OrderClosingType']) == TE.OrderDirection.SELL):
            PnL = FLib.PnLWithExpenses(DLWatchlist['OrderInQty'], DLWatchlist["BalanceQty"], DLWatchlist['OrderPrice'], DLWatchlist["FinalExecutedPrice"])
        else: #bought at closing
            PnL = FLib.PnLWithExpenses(DLWatchlist["BalanceQty"], DLWatchlist['OrderInQty'],  DLWatchlist["FinalExecutedPrice"], DLWatchlist['OrderPrice'])

    DLWatchlist['PLStatus'] = PnL
    if PnL >= 0:
        DLWatchlist["TradeStatusOnPnL"] = TE.TradeStatusOnPnL.Success.name
    else:
        DLWatchlist["TradeStatusOnPnL"] = TE.TradeStatusOnPnL.Failure.name


    #Update closing columns
    DLWatchlist["TradeStatus"] = TE.TradeStatus.Completed.value
    DLWatchlist["OrderOutQty"] = DLWatchlist["BalanceQty"]
    DLWatchlist["BalanceQty"] = 0
    DLWatchlist["CallType"] = TE.CallType.NA.value
    DLWatchlist["OrderEndTime"] = curr_time

    DLWatchlist["TimeTaken"] = GL.GetTimeDiff(DLWatchlist["OrderStartTime"],curr_time)

    #Update DB Record    
    TrLib.UpdateOrder(DLWatchlist)
#============================================================================================
def Cleanup():
    DBO = DBOps()

    #Watchlist = TrLib.GetActiveOrders()
    Watchlist = DBO.GetActiveOrders()
    #Watchlist = Watchlist.reset_index()
    ActiveTrades = False

    if not Watchlist.empty:
        for index, WatchlistRow in Watchlist.iterrows():
            DLWatchlist = Watchlist.loc[index].to_dict()        
            DLA = IsActive(WatchlistRow)
            if not DLA["Active"]:
                #Update DB for closed trade and create print/log entries
                
                DLWatchlist["TradeClosingSource"] = DLA["ClosingSource"]
                DLWatchlist["FinalExecutedPrice"] = DLA["ExecutedPrice"]
                #update database record
                TrLib.UpdateDBRecord(DLWatchlist)
            else:
                ActiveTrades = True
    
    return ActiveTrades

def CallStrategyMonitorScript(Strategy_Script, Watchlist):
    #Strategy_Script = "Monitor_Trades_Strategy_921.py"

    result = subprocess.run(
    ["python", Strategy_Script, json.dumps(Watchlist)],
    capture_output=True,
    text=True
    )
    #DLA = json.loads(result.stdout)

    #return DLA

def CallStrategyMonitors():
    DBO = DBOps()

    #Watchlist, StrategyList = TrLib.GetActiveOrders(True)
    Watchlist, StrategyList = DBO.GetActiveOrders(True)

    if not StrategyList.empty:
        for index, WatchlistRow in StrategyList.iterrows():
            DLWatchlist = Watchlist[Watchlist["Strategy"] == WatchlistRow["StrategyID"]].to_dict(orient='records')
            
            CallStrategyMonitorScript(WatchlistRow["TradeMonitorScript"], DLWatchlist)
            #DLA = CallStrategyMonitorScript(WatchlistRow["TradeMonitorScript"], DLWatchlist)
            # Parse the output JSON string back to a Python dictionary
            


#monitor
def Monitor():
    
    #Update DB records for the closed trades
    ActiveTrades = Cleanup()
        
    #call strategy monitors if there is any active order
    if ActiveTrades:
        #Call Monitor scripts
        CallStrategyMonitors()
    

    


""" def Monitor():
    Watchlist = TrLib.GetActiveOrders()
    #Watchlist = Watchlist.reset_index()

    if not Watchlist.empty:
        for index, WatchlistRow in Watchlist.iterrows():
            DLWatchlist = Watchlist.loc[index].to_dict()        
            DLA = IsActive(WatchlistRow)
            if DLA["Active"]:
                #Call strategy monitor script
                Strategy_Script = "Monitor_Trades_Strategy_921.py"

                result = subprocess.run(
                ["python", Strategy_Script, json.dumps(DLWatchlist)],
                capture_output=True,
                text=True
                )

                # Parse the output JSON string back to a Python dictionary
                DLA = json.loads(result.stdout)
            if DLA["Active"]:
                continue
            else:
                #Update DB for closed trade and create print/log entries
                
                DLWatchlist["TradeClosingSource"] = DLA["ClosingSource"]
                DLWatchlist["FinalExecutedPrice"] = DLA["ExecutedPrice"]
                #update database record
                UpdateDBRecord(DLWatchlist) """

# print("\n" + Watchlist.at[index, "TradeClosingSource"]  + " at " + str(curr_time))
# print("\n" + TE.OrderDirection(WatchlistRow['OrderClosingType']).name + " @" + str(Executed_Price))
# print("\nPnL: " + " {:.2f}".format(PnL))

#Check if today is a holiday
DBO = DBOps()

DBO.CheckHolidays()
 
while True:
    #If Trade end time reached or Max Loss reached or max profit reached
    curr_time   =   datetime.now().strftime(Const.Time_Format)
    #PnL         =   1 #Get current state of today's PnL
    #TradeCount  =   1
    # if (
    #     curr_time >= Const.Stock_Trading_End_Time 
    #     or (PnL < 0 and PnL <= Const.Max_Loss_Per_Day) 
    #     or (PnL > 0 and PnL >= Const.Max_Profit_Per_Day) 
    #     or TradeCount >= Const.Max_Trades_Per_Day
    # ):
    #     break; 
    # else:

    if curr_time >= Const.Stock_Trading_Start_Time and curr_time <=Const.Stock_Trading_End_Time:
        Monitor()
        time.sleep(2)
    else:
        break
    




