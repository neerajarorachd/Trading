from LibTrading import TradingLib
from LibEnum import TradingEnums as TE
from LibConstants import Const
from datetime import date
from datetime import datetime
from  LibWatchlist import HistoricalWatchlist as HW
from LibDBBase import DBBase
from LibFinance import FinLib
from LibAnalysis import AnaLysisLib
from LibGeneric import GeneicLib
import pandas as pd
import time
from LibDhan import Dhan
from LibDBOps import DBOps
import tzlocal


class Strategy:

    def __init__(self, StrategyType):    
        #get strategy details
        DL = TradingLib.GetStrategyDetails(TradingLib, StrategyType)
        if DL is not None and (DL):
            self._StrategyType                      = StrategyType
            self._StrategyID                        = DL["StrategyID"]
            self._StrategyName                      = DL["StrategyName"]
            self._StrategyScript                    = DL["StrategyName"]
            self._TradeMonitorScript                = DL["TradeMonitorScript"]
            self._LeadMonitorScript                 = DL["LeadMonitorScript"]
            self._StrategyMaxPrice                  = DL["StrategyMaxPrice"]
            self._StrategyMaxQty                    = DL["StrategyMaxQty"]
            self._StrategyTotalValueBasis           = DL["StrategyTotalValueBasis"]
            self._StrategyTradingStartTime          = DL["StrategyTradingStartTime"]
            self._StrategyTradingEndTime            = DL["StrategyTradingEndTime"]
            self._StrategyNewOrderEndTime            = DL["StrategyNewOrderEndTime"]
            self._StrategyExchange                  = TE.Exchange(DL["StrategyExchange"])
            self._StrategyPrimaryCandleDuration     = DL["StrategyPrimaryCandleDuration"]
            self._StrategyTargetPerc                = DL["StrategyTargetPerc"]
            self._StrategySLPerc                    = DL["StrategySLPerc"]
            self._StrategyMaxTradesAtOnce           = DL["StrategyMaxTradesAtOnce"]
            
            
            self._StrategyDailyMaxTradeCount        = DL["StrategyDailyMaxTradeCount"]
            self._Loop                              = DL["Loop"]
            self._ReverseOrder                      = DL["ReverseOrder"]
            self._TimeBound                         = DL["TimeBound"]
            self._BBSticky                          =DL["BBSticky"]
            self._MonitorIndicators                 = DL["MonitorIndicators"]

            self._TradingStatus                     = TE.TradingStatus.Allowed
            self._EntryFlag                         = 0

            #Watchlist ID - Start
            self._StrategyWatchlistID               = DL["StrategyWatchlist"]
            if self._StrategyWatchlistID is None:
                self._StrategyWatchlist                 = TE.Watchlist_Type.TODAY
                self._StrategyWatchlistID           = TE.Watchlist_Type.TODAY.value
            else:
                self._StrategyWatchlist                 = TE.Watchlist_Type(self._StrategyWatchlistID)
            #Watchlist ID - Start

            self._TradeType                         = TE.TradeType.MIS
            self._Symbol                            = None

    TradingStatus = TE.TradingStatus.Allowed

    _EntryFlag = 0
    #WatchlistType = TE.Watchlist_Type.TODAY
    TradeType = TE.TradeType.MIS

    @property
    def StrategyID(self):
        return  self._StrategyID

    @property
    def StrategyName(self):
        return self._StrategyName

    @property
    def StrategyScript(self):
        return self._StrategyScript

    @property
    def TradeMonitorScript(self):
        return self._TradeMonitorScript

    @property
    def LeadMonitorScript(self):
        return self._LeadMonitorScript

    @property
    def StrategyMaxPrice(self):
        return self._StrategyMaxPrice

    @property
    def StrategyMaxQty(self):
        return self._StrategyMaxQty

    @property
    def StrategyTotalValueBasis(self):
        return self._StrategyTotalValueBasis

    @property
    def StrategyTradingStartTime(self):
        return self._StrategyTradingStartTime

    @property
    def StrategyNewOrderEndTime(self):
        return self._StrategyNewOrderEndTime
    
    @property
    def StrategyTradingEndTime(self):
        return self._StrategyTradingEndTime

    @property
    def StrategyExchange(self):
        return self._StrategyExchange

    #Writable exchange
    @StrategyExchange.setter
    def StrategyExchange(self, value):
        self._StrategyExchange = value

    @property
    def StrategyPrimaryCandleDuration(self):
        return self._StrategyPrimaryCandleDuration

    @property
    def StrategyTargetPerc(self):
        return self._StrategyTargetPerc

    @property
    def StrategySLPerc(self):
        return self._StrategySLPerc

    @property    
    def StrategyMaxTradesAtOnce(self):
        return self._StrategyMaxTradesAtOnce

    @property
    def StrategyWatchlistID(self):
        return self._StrategyWatchlistID

    @property
    def StrategyWatchlist(self):
        return self._StrategyWatchlist

    @StrategyWatchlist.setter
    def StrategyWatchlist(self, value):
        self._StrategyWatchlist = value
        self._StrategyWatchlistID = self._StrategyWatchlist.value

    @property
    def StrategyDailyMaxTradeCount(self):
        return self._StrategyDailyMaxTradeCount
    


        if Count < self._StrategyMaxTradesAtOnce: return False
        else: return True

    @property
    def StrategyOpenOrderCount(self):
        return TradingLib.GetOrdersCountFromDB(TradingLib, self._StrategyID, TE.TradeStatus.Active)

    @property
    def StrategyClosedOrderCount(self):
        return TradingLib.GetOrdersCountFromDB(TradingLib, self._StrategyID, TE.TradeStatus.Completed)
    
    @property
    def StrategyDaysOrderCount(self):
        return TradingLib.GetOrdersCountFromDB(TradingLib, self._StrategyID, TE.TradeStatus.All)
    
    @property
    def DailyStrategyMaxTradesReached(self):
        TradingLib.GetOrdersCountFromDB(TradingLib, self._StrategyID, TE.TradeStatus.All) >= self._StrategyDailyMaxTradeCount

    @property
    def DailyMaxTradesReached(self):
        return TradingLib.GetOrdersCountFromDB(TradingLib, None, TE.TradeStatus.All) >= Const.Max_Trades_Per_Day

    @property
    def StrategyMaxTradesAtOnceReached(self):
        return TradingLib.GetOrdersCountFromDB(TradingLib, self._StrategyID, TE.TradeStatus.Active) >= self._StrategyMaxTradesAtOnce

    @property
    def Now(self):
        return datetime.now().strftime(Const.Time_Format)
    
    @property
    def Today(self):
        return str(date.today())
    
    @property
    def Symbol(self):
        return self._Symbol

    @Symbol.setter
    def Symbol(self, value):
        self._Symbol = value

    @property
    def TSL(self):
        return self._TSL

    @TSL.setter
    def TSL(self, value):
        self._TSL = value

    @property
    def Loop(self):
        if self._Loop is None or self._Loop == 0: self._Loop=False
        else: self._Loop=True
        return self._Loop
    
    @property
    def ReverseOrder(self):
        if self._ReverseOrder is None or self._ReverseOrder==0 : self._ReverseOrder=False
        else: self._ReverseOrder = True
        return self._ReverseOrder
    
    @property
    def TradingStatus(self):
        _TradingStatus = TradingLib.TradingStatus(TE.TradeType.MIS)
        if _TradingStatus == TE.TradingStatus.Allowed or  _TradingStatus == TE.TradingStatus.OnHold:
            if self.DailyMaxTradesReached or self.DailyStrategyMaxTradesReached:
                _TradingStatus = TE.TradingStatus.NotAllowed
            elif self.StrategyMaxTradesAtOnceReached:
                _TradingStatus = TE.TradingStatus.OnHold
        
        return _TradingStatus


    # Calculate Qty    
    
    def AvailableQty(self, Conn, Symbol):                        
        Qty = TradingLib.CalculateQtyToOrder(TradingLib, Conn, Symbol, self._StrategyMaxQty)

        # If MaxQty < Qty then Qty = MaxQty
        if Qty >  self.StrategyMaxQty:
            Qty = self.StrategyMaxQty

        return Qty

    @property
    def TodayWatchlistID(self):                        
        WatchlistID = HW.GetTodaysWatchListID()
        if WatchlistID is None:
            WatchlistID = self._StrategyWatchlistID
        return WatchlistID
    
    def GetTradingStatus(TradeType):
        TradingStatus = TradingLib.TradingStatus(TradeType)


    def order(self, Symbol, Qty, Watchlist, Bullish, TotalValue, OrderDirection, Conn, TargetPricePerc=None, SLPricePerc=None):
    #print("buy")
        if TargetPricePerc is None:
            TargetPricePerc = self._StrategyTargetPerc
        if SLPricePerc is None:
            SLPricePerc = self._StrategySLPerc

        DL                  =   TradingLib.Order(TradingLib, Conn, self._StrategyType, Watchlist, Symbol,  Bullish, TotalValue,  self._StrategyExchange, TE.OrderGroupType.MARKET_SL_TARGET, Qty,TE.TradeType.MIS, TE.CallType.NA, OrderDirection, SLPricePerc, TargetPricePerc, self._StrategyPrimaryCandleDuration, self._StrategyTotalValueBasis)
        return DL
    
    def Exit(self, Watchlist, Conn):
        TimeOver = False

        if self._TimeBound:
            TimeOver = self.TimeBound(Watchlist, Conn)

        if not TimeOver:
            if self._MonitorIndicators:
                Watchlist = self.MonitorIndicatorChanges(Watchlist, Conn)

            if self._BBSticky:
                self.MonitorBBChanges(Watchlist, Conn)



    def Enter_TimeBound(self, Watchlist_Morning_Refined):
        curr_time = datetime.now().strftime(Const.Time_Format)

        #check if today is a trading holiday
        self.CheckHolidays()

        if ((curr_time <= Const.Stock_Trading_Start_Time) or (curr_time >= Const.Stock_Trading_End_Time)):
            TradingStatus = TE.TradingStatus.NotAllowed
        else:

            DH              = Dhan()
            tsl             =   DH.DhanConnection #Tradehull(str_Client_Code,str_Token_ID)
            FLib            =   FinLib()
            ALib            =   AnaLysisLib()
            GLib            =   GeneicLib()
            TrLib            =   TradingLib()
            #Check whether further orders are allowed
            #it must be a part of each strategy entry function
            
            #Entry_Flag          =       0
            TradingStatus       =       self.TradingStatus
            
            
            # WatchlistType = TE.Watchlist_Type.P50TO250
            # WatchlistType = self.WatchlistType
            # WatchlistType = TE.Watchlist_Type.TODAY
            # WatchlistType = TE.Watchlist_Type.P50TO250
            

            #This watchlist-block will run everytime
            if self.StrategyWatchlist == TE.Watchlist_Type.TODAY:
                WatchlistID     =   self.TodayWatchlistID
            else:
                WatchlistID     =   self._StrategyWatchlistID
            WatchlistType   =   TE.Watchlist_Type(WatchlistID)

            if curr_time >= Const.Data_Loading_Time and Watchlist_Morning_Refined.empty and TradingStatus==TE.TradingStatus.Allowed:   
                #Get the watchlist
                Watchlist_Morning = HW.GetWatchlist(tsl, WatchlistType)
                self.TSL = tsl

                #This watchlist-block will run first time
                if self.StrategyWatchlist == TE.Watchlist_Type.TODAY:
                    WatchlistID     =   self.TodayWatchlistID
                else:
                    WatchlistID     =   self._StrategyWatchlistID
                WatchlistType   =   TE.Watchlist_Type(WatchlistID)

                #Call Get Momentum Data to refine the watchlist
                Watchlist_Morning_Refined = HW.GetHistoricalMomentumData(tsl,self.Today, "rowid, *", WatchlistID)
            
            #and curr_time <= self.StrategyTradingEndTime
            if curr_time >= self._StrategyTradingStartTime and curr_time <= self._StrategyNewOrderEndTime and TradingStatus==TE.TradingStatus.Allowed:    
                # Call Two Sisters Candle function to get the final list
                Two_Sisters_Watchlist = ALib.Get_Two_Sisters_Candles(Watchlist_Morning_Refined, self.StrategyExchange,self.StrategyPrimaryCandleDuration, tsl, self.StrategyTotalValueBasis, self.StrategyMaxPrice)
                
                # If list is not empty create orders
                if not Two_Sisters_Watchlist.empty:
                    DBO = DBOps()

                    for index, WatchlistRow in Two_Sisters_Watchlist.iterrows():   
                        Symbol = WatchlistRow['SYMBOL']
                        print("Indicator Analysis for "+ WatchlistRow['SYMBOL'] + " started at " + self. Now)

                        #Check whether Trading is allowed
                        if TradingStatus == TE.TradingStatus.NotAllowed:
                            break
                        elif TradingStatus == TE.TradingStatus.OnHold:
                            break
                        elif TradingLib.IsStockActive(TradingLib, Symbol):
                        #elif DBO.IsStockActive(Symbol):
                            continue

                        Uptrend = WatchlistRow['BULLISH']
                        
    
                        # Calculate Qty                            
                        Qty = self.AvailableQty(tsl, Symbol)

                        DL1M=DL3M=DL5M=None

                        if Qty > 0 and self.GapBetweenTwoTrades(Symbol):
                            #Get intraday data for 1,3 and 5 minutes for future analysis
                            #Chart1
                            #Chart3 = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 3)
                            
                            # if self.StrategyPrimaryCandleDuration==1 or self.Now < "10:15:00":
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 1)
                                
                            # elif self.StrategyPrimaryCandleDuration==3:
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 3)
                            
                            # elif self.StrategyPrimaryCandleDuration==5:
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 5)

                            Chart, ChartInterval = self.GetSymbolChart(tsl, Symbol)
                            DLChart = ALib.Get_Indicators(Chart, tsl)
                            DLBBChart = ALib.Get_Volume_Driven_Indicators(Chart)
                            INDCall = ALib.GetIndicatorCall(DLChart, DLBBChart)
                            #LTP = tsl.get_ltp_data(names = [Symbol])[Symbol]
                            LTP = Chart.iloc[-1]["close"]
                            #Call BBAnalysis function
                            DLBB = ALib.Get_BB_Call(LTP,Chart,DLChart, TE.TradeType.SCALPING)
                            
                            RSIUptrend  = self.UpTrend(DLChart)
                            
                            TotalValue      = WatchlistRow['TOTALVALUE']
                            ReverseOrder    = self.ReverseOrder

                            BBCall          = DLBB["BBCall"]

                            #Bypass BBCall for the time being
                            BBCall = INDCall

                            TargetPricePerc = DLBB["TargetPricePerc"]
                            SLPricePerc     = DLBB["SLPricePerc"]

                            if BBCall == TE.OrderDirection.PASS or INDCall == TE.OrderDirection.PASS:
                                continue
                            elif BBCall == TE.OrderDirection.LEAD or INDCall == TE.OrderDirection.LEAD:
                                 continue
                            #elif ((RSIUptrend and BBCall == TE.OrderDirection.BUY) and not ReverseOrder) or ((not RSIUptrend and BBCall == TE.OrderDirection.SELL) and ReverseOrder):
                            elif ((INDCall == BBCall == TE.OrderDirection.BUY) and not ReverseOrder) or ((INDCall == BBCall == TE.OrderDirection.SELL) and ReverseOrder):
                            #if (Uptrend and not ReverseOrder) or (not Uptrend and ReverseOrder):
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.BUY, tsl, TargetPricePerc, SLPricePerc)  
                                print("\n" + str(Qty) + " " + Symbol + " bought @" + str(DL["OrderPrice"]) + " at " + str(curr_time))
                            else: #Downtrend
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.SELL, tsl, TargetPricePerc, SLPricePerc)
                                print("\n" + str(Qty) + " " + Symbol + " sold @" + str(DL["OrderPrice"]) + " at " + str(curr_time)) 

                            """
                            TargetPricePerc = self._StrategyTargetPerc
                            SLPricePerc     = self._StrategySLPerc

                            if ((RSIUptrend) and not ReverseOrder) or ((not RSIUptrend) and ReverseOrder):
                            #if (Uptrend and not ReverseOrder) or (not Uptrend and ReverseOrder):
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.BUY, tsl, TargetPricePerc, SLPricePerc)  
                                print("\n" + str(Qty) + " " + Symbol + " bought @" + str(DL["OrderPrice"]) + " at " + str(curr_time))
                            else: #Downtrend
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.SELL, tsl, TargetPricePerc, SLPricePerc)
                                print("\n" + str(Qty) + " " + Symbol + " sold @" + str(DL["OrderPrice"]) + " at " + str(curr_time))

                            """
                            DL1M, DL3M, DL5M = ALib.Get_1_3_5M_Indicators(tsl, Symbol, self.StrategyExchange.name)
                            #Set order ID for Indicators
                            DLBB["INDICATORS"]["OrderID"] = DL1M["OrderID"] = DL3M["OrderID"] = DL5M["OrderID"] = DL["OrderID"]
                            DLBB["INDICATORS"]["ChartInterval"] = ChartInterval
                            DLBB["INDICATORS"]["TimeStamp"] = self.GetLastTimestamp(Chart)

                            DBO.UpdateInOrderMomentumIndicators(DL1M, DL3M, DL5M)
                            
                            #Update BB Data                            
                            ALib.StoreOrderBBData(DLBB["INDICATORS"])

                        TradingStatus       =      self.TradingStatus
                else:
                    pass

        return TradingStatus, Watchlist_Morning_Refined  
    
    def Enter_Indicator_Call(self, Watchlist_Morning_Refined):
        curr_time = datetime.now().strftime(Const.Time_Format)

        #check if today is a trading holiday
        self.CheckHolidays()

        if ((curr_time <= Const.Stock_Trading_Start_Time) or (curr_time >= Const.Stock_Trading_End_Time)):
            TradingStatus = TE.TradingStatus.NotAllowed
        else:

            DH              = Dhan()
            tsl             =   DH.DhanConnection #Tradehull(str_Client_Code,str_Token_ID)
            FLib            =   FinLib()
            ALib            =   AnaLysisLib()
            GLib            =   GeneicLib()
            TrLib            =   TradingLib()
            #Check whether further orders are allowed
            #it must be a part of each strategy entry function
            
            #Entry_Flag          =       0
            TradingStatus       =       self.TradingStatus
            
            
            # WatchlistType = TE.Watchlist_Type.P50TO250
            # WatchlistType = self.WatchlistType
            # WatchlistType = TE.Watchlist_Type.TODAY
            # WatchlistType = TE.Watchlist_Type.P50TO250
            

            #This watchlist-block will run everytime
            if self.StrategyWatchlist == TE.Watchlist_Type.TODAY:
                WatchlistID     =   self.TodayWatchlistID
            else:
                WatchlistID     =   self._StrategyWatchlistID
            WatchlistType   =   TE.Watchlist_Type(WatchlistID)

            if curr_time >= Const.Data_Loading_Time and Watchlist_Morning_Refined.empty and TradingStatus==TE.TradingStatus.Allowed:   
                #Get the watchlist
                Watchlist_Morning = HW.GetWatchlist(tsl, WatchlistType)
                self.TSL = tsl

                #This watchlist-block will run first time
                if self.StrategyWatchlist == TE.Watchlist_Type.TODAY:
                    WatchlistID     =   self.TodayWatchlistID
                else:
                    WatchlistID     =   self._StrategyWatchlistID
                WatchlistType   =   TE.Watchlist_Type(WatchlistID)

                #Call Get Momentum Data to refine the watchlist
                Watchlist_Morning_Refined = HW.GetHistoricalMomentumData(tsl,self.Today, "rowid, *", WatchlistID)
            
            #and curr_time <= self.StrategyTradingEndTime
            if curr_time >= self._StrategyTradingStartTime and curr_time <= self._StrategyNewOrderEndTime and TradingStatus==TE.TradingStatus.Allowed:    
                # Call Two Sisters Candle function to get the final list
                #Two_Sisters_Watchlist = ALib.Get_Two_Sisters_Candles(Watchlist_Morning_Refined, self.StrategyExchange,self.StrategyPrimaryCandleDuration, tsl, self.StrategyTotalValueBasis, self.StrategyMaxPrice)
                Indicator_Watchlist = ALib.Get_Indicator_Calls_for_Watchlist(Watchlist_Morning_Refined, self.StrategyExchange,self.StrategyPrimaryCandleDuration, tsl, self.StrategyTotalValueBasis, self.StrategyMaxPrice)
                # If list is not empty create orders
                if not Indicator_Watchlist.empty:
                    DBO = DBOps()

                    for index, WatchlistRow in Indicator_Watchlist.iterrows():   
                        Symbol = WatchlistRow['SYMBOL']
                        print("Indicator Analysis for "+ WatchlistRow['SYMBOL'] + " started at " + self. Now)

                        #Check whether Trading is allowed
                        if TradingStatus == TE.TradingStatus.NotAllowed:
                            break
                        elif TradingStatus == TE.TradingStatus.OnHold:
                            break
                        elif TradingLib.IsStockActive(TradingLib, Symbol):
                        #elif DBO.IsStockActive(Symbol):
                            continue

                        #Uptrend = WatchlistRow['BULLISH']
                        Uptrend = (WatchlistRow['CallType'] == TE.OrderDirection.BUY)
    
                        # Calculate Qty                            
                        Qty = self.AvailableQty(tsl, Symbol)

                        DL1M=DL3M=DL5M=None

                        if Qty > 0 and self.GapBetweenTwoTrades(Symbol):
                            #Get intraday data for 1,3 and 5 minutes for future analysis
                            #Chart1
                            #Chart3 = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 3)
                            
                            # if self.StrategyPrimaryCandleDuration==1 or self.Now < "10:15:00":
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 1)
                                
                            # elif self.StrategyPrimaryCandleDuration==3:
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 3)
                            
                            # elif self.StrategyPrimaryCandleDuration==5:
                            #     Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, 5)
                            
                            #if self.StrategyPrimaryCandleDuration==3:
                            #    ChartInterval = 5
                            

                            Chart, ChartInterval = self.GetSymbolChart(tsl, Symbol)
                            DLChart = ALib.Get_Indicators(Chart, tsl)
                            #DLBBChart = ALib.Get_Volume_Driven_Indicators(Chart)
                            #INDCall = ALib.GetIndicatorCall(DLChart, DLBBChart)
                            #LTP = tsl.get_ltp_data(names = [Symbol])[Symbol]
                            LTP = Chart.iloc[-1]["close"]
                            #Call BBAnalysis function
                            DLBB = ALib.Get_BB_Call(LTP,Chart,DLChart, TE.TradeType.SCALPING)
                            
                            #RSIUptrend  = self.UpTrend(DLChart)
                            
                            TotalValue      = WatchlistRow['HighScore']
                            ReverseOrder    = self.ReverseOrder

                            #BBCall          = DLBB["BBCall"]
                            
                            #print("5 Min BB Call " + BBCall.name)

                            #Bypass BBCall for the time being
                            #BBCall = INDCall
                            INDCall = WatchlistRow['CallType']
                            TargetPricePerc = DLBB["TargetPricePerc"]
                            SLPricePerc     = DLBB["SLPricePerc"]
                            BBCall          =   INDCall

                            if INDCall != BBCall:
                                continue
                            if INDCall == TE.OrderDirection.PASS:
                                continue
                            elif INDCall == TE.OrderDirection.LEAD:
                                 continue
                            #elif ((RSIUptrend and BBCall == TE.OrderDirection.BUY) and not ReverseOrder) or ((not RSIUptrend and BBCall == TE.OrderDirection.SELL) and ReverseOrder):
                            elif ((INDCall == TE.OrderDirection.BUY) and not ReverseOrder) or ((INDCall == TE.OrderDirection.SELL) and ReverseOrder):
                            #if (Uptrend and not ReverseOrder) or (not Uptrend and ReverseOrder):
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.BUY, tsl, TargetPricePerc, SLPricePerc)  
                                print("\n" + str(Qty) + " " + Symbol + " bought @" + str(DL["OrderPrice"]) + " at " + str(curr_time))
                            else: #Downtrend
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.SELL, tsl, TargetPricePerc, SLPricePerc)
                                print("\n" + str(Qty) + " " + Symbol + " sold @" + str(DL["OrderPrice"]) + " at " + str(curr_time)) 

                            """
                            TargetPricePerc = self._StrategyTargetPerc
                            SLPricePerc     = self._StrategySLPerc

                            if ((RSIUptrend) and not ReverseOrder) or ((not RSIUptrend) and ReverseOrder):
                            #if (Uptrend and not ReverseOrder) or (not Uptrend and ReverseOrder):
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.BUY, tsl, TargetPricePerc, SLPricePerc)  
                                print("\n" + str(Qty) + " " + Symbol + " bought @" + str(DL["OrderPrice"]) + " at " + str(curr_time))
                            else: #Downtrend
                                DL = self.order(Symbol, Qty, WatchlistType, Uptrend, TotalValue, TE.OrderDirection.SELL, tsl, TargetPricePerc, SLPricePerc)
                                print("\n" + str(Qty) + " " + Symbol + " sold @" + str(DL["OrderPrice"]) + " at " + str(curr_time))

                            """
                            DL1M, DL3M, DL5M = ALib.Get_1_3_5M_Indicators(tsl, Symbol, self.StrategyExchange.name)
                            #Set order ID for Indicators
                            DLBB["INDICATORS"]["OrderID"] = DL1M["OrderID"] = DL3M["OrderID"] = DL5M["OrderID"] = DL["OrderID"]
                            DLBB["INDICATORS"]["ChartInterval"] = ChartInterval
                            DLBB["INDICATORS"]["TimeStamp"] = self.GetLastTimestamp(Chart)

                            DBO.UpdateInOrderMomentumIndicators(DL1M, DL3M, DL5M)
                            
                            #Update BB Data                            
                            ALib.StoreOrderBBData(DLBB["INDICATORS"])

                        TradingStatus       =      self.TradingStatus
                else:
                    pass

        return TradingStatus, Watchlist_Morning_Refined  
    
    def Init(self):
        #ST930 = Strategy921()
        
        DF = pd.DataFrame()
        if self.Loop:            
            while True:
                TradingStatus, DF = self.Enter(DF)

                if TradingStatus==TE.TradingStatus.NotAllowed:
                    break
                else:
                    print("Sleeping")
                    time.sleep(60)
                    print("running")
        else:
            self.Enter(DF)

    def CheckHolidays(self):
        DBO = DBOps()

        DBO.CheckHolidays()

    def UpTrend(self, DL):
        UpTrend = False

        if DL is not None and DL:
            if DL["RSID1"] > DL["RSID2"]:
                #if 40 < DL["RSID1"] < 73:
                UpTrend = True

        return UpTrend 
    
    def GapBetweenTwoTrades(self, Symbol):
        TLib = TradingLib()

        return TLib.GapBetweenTwoTrades(Symbol)
    
    def GetSymbolChart(self, tsl, Symbol, ChartInterval=None):
        
        if ChartInterval is None:
            if self.StrategyPrimaryCandleDuration==1 or self.Now < "10:15:00":
                ChartInterval = 1
            elif self.StrategyPrimaryCandleDuration==3:
                ChartInterval = 3
            elif self.StrategyPrimaryCandleDuration==5:
                ChartInterval = 5
        
        Chart = tsl.get_intraday_data(Symbol, self.StrategyExchange.name, ChartInterval)

        return Chart, ChartInterval
    

    def TimeBound(self, Watchlist, Conn):
        TimeOver = False

        if self.Now >= self._StrategyTradingEndTime:
            TimeOver = True

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
                DLOrder = TradingLib.Order(TradingLib, Conn, TE.Strategy.Morning921, TE.Watchlist_Type.NONE, WatchlistRow['SYMBOL'], False, 0, TE.Exchange.NSE, TE.OrderGroupType.MARKET,WatchlistRow['BalanceQty'],TE.TradeType.MIS, TE.CallType.NA, TE.OrderDirection(WatchlistRow['OrderClosingType']),0,0,0, 0,0, 0, 0, WatchlistRow['OrderID'])
                
                TradingLib.CancelOrder(TradingLib, Conn, str_SL_Order_ID)
                TradingLib.CancelOrder(TradingLib, Conn, str_Target_Order_ID)

                Watchlist.at[index, "TradeClosingSource"] = TE.TradeClosingSource.TimeOut
                Watchlist.at[index, "FinalExecutedPrice"] = DLOrder["OrderPrice"]

                TradingLib.UpdateDBRecord(TradingLib, Watchlist.iloc[index])

    
        print("exit from Timebound monitor")
        return TimeOver
    
    def MonitorBBChanges(self, Watchlist, Conn):
        ALib = AnaLysisLib()

        for index, WatchlistRow in Watchlist.iterrows():
                OrderID                     =   WatchlistRow['OrderID']
                DLOrderBB                   =   ALib.GetOrderBBData(OrderID)
                
                if DLOrderBB is not None:
                    Symbol                  =   WatchlistRow['SYMBOL']
                    Chart, TimeInterval     =   self.GetSymbolChart(Conn, Symbol, DLOrderBB["ChartInterval"])
                    TimeStamp               =   self.GetLastTimestamp(Chart)
                    if TimeStamp == DLOrderBB["TimeStamp"]:
                        continue
                
                    DLBB                    =   ALib.Get_Volume_Driven_Indicators(Chart)
                    SLBB                    =   DLOrderBB["SLBB"]
                    TargetBB                =   DLOrderBB["TargetBB"]
                    SLBBPrice               =   DLOrderBB["SLBBLastPrice"]
                    SLLastPrice             =   DLOrderBB["SLLastPrice"]
                    TargetLastPrice         =   DLOrderBB["TargetLastPrice"]
                    TargetBBPrice           =   DLOrderBB["TargetBBLastPrice"]
                    NewSLBBPrice            =   None
                    NewTargetBBPrice        =   None
                    NewSLPrice              =   None
                    NewTargetPrice          =   None
                    DLBBRes                 =   {}
                    Exchange                =   TE.Exchange(WatchlistRow["Exchange"])
                    ReverseOrderDirection   =   TE.OrderDirection(WatchlistRow["OrderClosingType"])
                    

                    if DLBB[SLBB +"1"] != SLBBPrice or DLBB[TargetBB +"1"] != TargetBBPrice:
                        #Reset prices
                        NewSLPrice =   DLBB[SLBB +"1"] + (SLLastPrice - SLBBPrice)
                        NewTargetPrice      =   DLBB[TargetBB +"1"] + (TargetLastPrice - TargetBBPrice)
                        NewSLBBPrice        =   DLBB[SLBB +"1"]
                        NewTargetBBPrice    =   DLBB[TargetBB +"1"]

                        #reset SL and Targets
                        str_SL_Order_ID     = WatchlistRow['SLOrderID']
                        str_Target_Order_ID = WatchlistRow['TargetOrderID']

                        #Update BB Data
                        
                        DLBBRes["SLLastPrice"]          =   round(NewSLPrice,2)
                        DLBBRes["TargetLastPrice"]      =   round(NewTargetPrice,2)
                        DLBBRes["OrderID"]              =   OrderID
                        DLBBRes["SLBBLastPrice"]        =   round(NewSLBBPrice,4)
                        DLBBRes["TargetBBLastPrice"]    =   round(NewTargetBBPrice,4)
                        DLBBRes["TimeStamp"]            =   TimeStamp   

                        #Modify SL and Target orders
                        self.ModifyOrder(Conn, WatchlistRow['BalanceQty'], str_Target_Order_ID, NewTargetPrice, str_SL_Order_ID, NewSLPrice, Symbol, Exchange, ReverseOrderDirection, TE.TradeType.MIS, OrderID)

                    

                        ALib.UpdateOrderBBData(DLBBRes)

    def MonitorIndicatorChanges(self, Watchlist, Conn):
        ALib = AnaLysisLib()

        for index, WatchlistRow in Watchlist.iterrows():
                Symbol                  =   WatchlistRow['SYMBOL']
                Chart, TimeInterval     =   self.GetSymbolChart(Conn, Symbol)
                DLIN                    =   ALib.Get_Indicators(Chart, Conn)

                #Check indicator conditions - Call existing function

                    #Close the order
                    #Delete record from Watchlisy
                #if watchlist modified, reindex

        return Watchlist
    
    def GetLastTimestamp(self, Chart: pd.DataFrame, PreviousTimeStamp=None):
        if Chart.empty:
            raise ValueError("Chart DataFrame is empty.")

        # Try using index as datetime, fallback to 'timestamp' column
        if isinstance(Chart.index, pd.DatetimeIndex):
            last_timestamp = Chart.index[-1]
        elif 'timestamp' in Chart.columns:
            last_timestamp = pd.to_datetime(Chart['timestamp'].iloc[-1]).tz_localize(None)
            #last_timestamp = last_timestamp.tz_localize(None)
        else:
            raise ValueError("No datetime index or 'timestamp' column found.")

        if PreviousTimeStamp is None:
            return str(last_timestamp)

        return last_timestamp != pd.to_datetime(PreviousTimeStamp)

    def CloseAnOrder(self, Conn, Strategy, Exchange, TradeType, OrderGroupType, Symbol, Qty, OrderDirection, OrderID, SLOrderID, TargetOrderID):
        DLOrder = TradingLib.Order(TradingLib, Conn, Strategy, TE.Watchlist_Type.NONE, Symbol, False, 0, Exchange, OrderGroupType,Qty, TradeType, TE.CallType.NA, OrderDirection,0,0,0, 0,0, 0, 0, OrderID)
                
        TradingLib.CancelOrder(TradingLib, Conn, SLOrderID)
        TradingLib.CancelOrder(TradingLib, Conn, TargetOrderID)

        return DLOrder["OrderPrice"]

    def ModifyOrder(self, Con, Qty, TargetOrderID=None, TargetOrderPrice=None, SLOrderID=None, SLOrderPrice=None, Symbol=None, Exchange=None, ReverseOrderDirection=None, TradeType=None, OrderID=None):
        TradingLib.ModifyOrder(TradingLib, Con, Qty, TargetOrderID, TargetOrderPrice, SLOrderID, SLOrderPrice, Symbol, Exchange, ReverseOrderDirection, TradeType, OrderID)