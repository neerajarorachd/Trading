from ClassStrategyBase import Strategy
from pprint import pprint
from LibFinance import FinLib
from LibAnalysis import AnaLysisLib
from LibGeneric import GeneicLib
from LibEnum import TradingEnums as TE
from LibTrading import TradingLib
from LibDBBase import DBBase
from LibDhan import Dhan

#import ExecuteFile

#tsl             =   DBBase() #Tradehull(str_Client_Code,str_Token_ID)
DH              = Dhan()
tsl             =   DH.DhanConnection
FLib            =   FinLib()
ALib            =   AnaLysisLib()
GLib            =   GeneicLib()
TrLib            =   TradingLib()

class Strategy921(Strategy):
    

    def __init__(self):
        super().__init__(TE.Strategy.Morning921)

    def Enter(self, Watchlist_Morning_Refined):
        #global int_Entry_Flag, Watchlist_Refined, Historical_Data_Loaded, Watchlist_Morning
        return super().Enter_TimeBound(Watchlist_Morning_Refined)

    def Exit(Watchlist, Conn):
        super().Exit_TimeBound(Watchlist, Conn)

print("exit from 921 monitor")


""" Workflow
    
    Enter with Empty Refined watchlist
    Verify whether trading is allowed
    Get Watchlist ID
    Get Watchlist
    Get Mimentum data
    Get 2 Sisters data
    Start loop
    check whether trading is allowed and stock is not in active state
    get momentum indicators
    create order
    Store momentum indicators
    Loop end
    return Entry Flag state and refined watchlist
    """
    


""" def order(Symbol, Qty, Watchlist, Bullish, TotalValue, OrderDirection ):
    #print("buy")
        DL                  =   TrLib.Order(tsl, TE.Strategy.Morning921, Watchlist, Symbol,  Bullish, TotalValue,  TE.Exchange.NSE, TE.OrderGroupType.MARKET_SL_TARGET,Qty,TE.TradeType.MIS, TE.CallType.NA, OrderDirection, Const.SL_Pers_921,Const.Target_Pers_921, Const.PrimaryCandleDuration_921, Const.TotalValue_2_Sisters)
        return DL """


   


"""     def Init(self):
        #ST930 = Strategy921()
        
        DF = pd.DataFrame()
        if self.Loop:            
            while True:
                TradingStatus, DF = self.Enter(DF)

                if TradingStatus==TE.TradingStatus.NotAllowed:
                    break
        else:
            self.Enter(DF) """



""" #Check whether further orders are allowed
        #it must be a part of each strategy entry function
        #TradingStatus       =       TradingLib.TradingStatus(TE.TradeType.MIS)

        Entry_Flag          =       0
        TradingStatus       =       self.TradingStatus
        if TradingStatus == TE.TradingStatus.NotAllowed:
            #return 1, Watchlist_Morning_Refined
            Entry_Flag  =       2
        elif TradingStatus == TE.TradingStatus.OnHold:
            #return 0, Watchlist_Morning_Refined
            Entry_Flag  =       1
        #chart = pd.DataFrame()
        Open_Position_Count = 0
        curr_time = datetime.now().strftime(Const.Time_Format)
        WatchlistType = TE.Watchlist_Type.P50TO250
        WatchlistType = self.WatchlistType
        WatchlistType = TE.Watchlist_Type.TODAY
        WatchlistType = TE.Watchlist_Type.P50TO250
        WatchlistID   = WatchlistType.value

        if curr_time >= Const.Data_Loading_Time and Watchlist_Morning_Refined.empty and TradingStatus==TE.TradingStatus.Allowed:   
            #Get the watchlist
            Watchlist_Morning = HW.GetWatchlist(tsl, WatchlistType)
            self.TSL = tsl

            if WatchlistID == TE.Watchlist_Type.TODAY.value:
                WatchlistID = self.TodayWatchlistID
            # Call Get Momentum Data to refine the watchlist
            Watchlist_Morning_Refined = HW.GetHistoricalMomentumData(tsl,self.Today, "rowid, *", WatchlistID)
            #Historical_Data_Loaded = True
        
        #and curr_time <= self.StrategyTradingEndTime
        if curr_time >= self.StrategyTradingStartTime  and Entry_Flag == 0:    
            #Run if Open Positions are < Max Order Count
            #Open_Position_Count = TrLib.GetOpenPositionCount(tsl)[0]
            #Open_Position_Count = self.StrategyOpenOrderCount
            #if self.StrategyOpenOrderCount < self.StrategyMaxTradesAtOnce:
            # Call Two Sisters Candle function to get the final list
            Two_Sisters_Watchlist = ALib.Get_Two_Sisters_Candles(Watchlist_Morning_Refined, self.StrategyExchange,self.StrategyPrimaryCandleDuration, tsl, self.StrategyTotalValueBasis, self.StrategyMaxPrice)
            
            # If list is not empty create orders
            if not Two_Sisters_Watchlist.empty:
                #For SYMBOL in Watchlist
                for index, WatchlistRow in Two_Sisters_Watchlist.iterrows():   
                    Symbol = WatchlistRow['SYMBOL']
                    
                    if TradingStatus == TE.TradingStatus.NotAllowed:
                        #Entry_Flag = 1
                        break
                    elif TradingStatus == TE.TradingStatus.OnHold:
                        break
                    elif TradingLib.IsStockActive(TradingLib, Symbol):
                        continue

                    #if not (self.StrategyMaxTradesAtOnceReached and self.DailyStrategyMaxTradesReached and Daily :
                    #chart = tsl.get_intraday_data(Symbol, self.StrategyExchange, self.StrategyPrimaryCandleDuration)
                    
                    #Uptrend = False
                    Uptrend = WatchlistRow['BULLISH']
                    
                    
                    # Calculate Qty                            
                    Qty = self.AvailableQty(tsl, Symbol)

                    if Qty > 0:
                        #Get intraday data for 1,3 and 5 minutes for future analysis
                        DL1M, DL3M, DL5M = ALib.Get_1_3_5M_Indicators(tsl, Symbol, self.StrategyExchange.name)
                        
                        TotalValue      = WatchlistRow['TOTALVALUE']
                        ReverseOrder    = self.ReverseOrder
                        if (Uptrend and not ReverseOrder) or (not Uptrend and ReverseOrder):
                            DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.BUY, tsl)   
                            #Entry_Flag = 1                                          
                            print("\n" + str(Qty) + " " + Symbol + " bought @" + str(DL["OrderPrice"]) + " at " + str(curr_time))
                        else: #Downtrend
                            DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.SELL, tsl)
                            #Entry_Flag = 1
                            print("\n" + str(Qty) + " " + Symbol + " sold @" + str(DL["OrderPrice"]) + " at " + str(curr_time))

                        #Set order ID for Indicators
                        DL1M["OrderID"] = DL3M["OrderID"] = DL5M["OrderID"] = DL["OrderID"]

                        TrLib.UpdateInOrderMomentumIndicators(DL1M, DL3M, DL5M)

                        #Increase Open position count
                        #Open_Position_Count += 1
                        #Entry_Flag = 1
                    TradingStatus       =      self.TradingStatus
            else:
                pass
                #fetch order data for exit loop
                #Entry_Flag = 1   
        # if Entry_Flag==0 and not self.Loop:
        #     Entry_Flag = 1

        return TradingStatus, Watchlist_Morning_Refined   """
    
"""  #Exit Time
    def exit_921_927(self, Watchlist):
        if self.Now >= self._StrategyTradingEndTime:
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

                TrLib.UpdateDBRecord(Watchlist.iloc[index]) """
    
    

