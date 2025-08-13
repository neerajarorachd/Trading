from LibDBBase import DBBase
import sys
import json
import pandas as pd
from ClassStrategies import Strategy921
from LibDhan import Dhan

DH              = Dhan()
tsl             =   DH.DhanConnection
ST921           =   Strategy921()

def main():
    # Get the dictionary from the first argument
    input_json = sys.argv[1]
    Watchlist = pd.read_json(input_json)  #pd.DataFrame(input_json) #json.loads(input_json)
    
    #ST921.exit_921_927(Watchlist)
    ST921.Exit(Watchlist, tsl)
    

if __name__ == "__main__":
    print("Entered into 921 monitor")
    main()
    print("exit from 921 monitor")




    """ if curr_time >= Const.End_Time_921:
        for index, WatchlistRow in Watchlist.iterrows():
            str_SL_Order_ID = WatchlistRow['SLOrderID']
            str_Target_Order_ID = WatchlistRow['TargetOrderID']
            #SLorder_status = None
            #Target_Order_Status = None#
            #columns = ['Active', 'ClosingSource', 'ExecutedPrice']
            #DL = {col: None for col in columns}

            # Modify or use the dictionary
            #data['status'] = 'received'
            #data['length'] = len(data)

        
            #Close the position
            #str_Timeout_Order_ID = CreateSingleOrder(str_Symbol, str_NSE,int_Qty, 0, 0, str_MARKET, str_Closing_Type, str_INTRADAY)
            DLOrder = TrLib.Order(tsl, TE.Strategy.Morning921, TE.Watchlist_Type.NONE, WatchlistRow['SYMBOL'], False, 0, TE.Exchange.NSE, TE.OrderGroupType.MARKET,WatchlistRow['BalanceQty'],TE.TradeType.MIS, TE.CallType.NA, TE.OrderDirection(WatchlistRow['OrderClosingType']),0,0,0, 0,0, 0, 0, WatchlistRow['OrderID'])
            
            TrLib.CancelOrder(tsl, str_SL_Order_ID)
            TrLib.CancelOrder(tsl, str_Target_Order_ID)

            Watchlist.at[index, "TradeClosingSource"] = TE.TradeClosingSource.TimeOut
            Watchlist.at[index, "FinalExecutedPrice"] = DLOrder["OrderPrice"]

            TrLib.UpdateDBRecord(Watchlist.iloc[index])
    
    print("exit from 921 monitor") """
            # DL["ClosingSource"] = TE.TradeClosingSource.TimeOut
            # DL["ExecutedPrice"] = DLOrder["OrderPrice"]
        #     DL["Active"] =   False
        # else:
        #     DL["Active"] =   True
        
        #return DL
        # Return the result as JSON
        #print(json.dumps(DL))



