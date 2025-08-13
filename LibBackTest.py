import pandas as pd
from LibDBOps import DBOps
from LibAnalysis import AnaLysisLib
from LibEnum import TradingEnums as TE
from LibFinance import FinLib
from datetime import datetime, timedelta
from LibConstants import Const

import os

class BackTest:

    def __init__(self):    
        #get strategy details
        self._DataLoopStartRow          =   21
        self._OrderQty                  =   1000
        self._TimeBound                 =   False
        self._StrategyTradingStartTime  =   "09:30:00"
        self._StrategyTradingEndTime    =   "11:30:00"
        self._CandleDuration            =   3
        self._DayTradingEndTime         =   "15:00:00"
        self._SingleTradeAtATime        =   True
        self._GapBetweenTwoTrades       =   3


    @property
    def DataLoopStartRow(self):
        return self._DataLoopStartRow

    def GetSymbolData(self, Symbol, Date):
        DBO = DBOps()

        return DBO.GetSymbolHistDataForADate(Symbol, Date)

    def SplitDF(self, DF):
        pass
        #return two DF
        #it can be a part of method execution

    def ExecutionPath(self, DF):
        pass
        #   Execution Path Analysis
        #   Create DF, one row for each execution path
        #   Start Time, Number of trades, Success, Failure count, overall profit/loss

    def GetSymbolDates(self, Symbol):
        DBO = DBOps()

        return DBO.GetSymbolDates(Symbol)
        
    def GetTimeFromTimeStamp(self, TimeStamp):
         pass


    def BTIntraday(self, Symbol):
        ListDates       =   self.GetSymbolDates(Symbol)
        ALib            =   AnaLysisLib()
        FLib            =   FinLib()

        OrderRows       =   []
        DayWiseData     =   []
        ReportStartTime =   datetime.now().strftime("%Y%m%d_%H%M%S")
        DBO             =   DBOps()
        ActiveTrade     =   False
        TradeFinishTime =   None
        ExitTime        =   datetime.now().strftime(Const.Time_Format)
        EntryTime       =   None

        #GetSymbolData
        for Date in ListDates:
            DFSD    =   self.GetSymbolData(Symbol, Date)
            DayWiseDataRow = {}
            DayOrderCount = 0
            DayWinCount = 0
            DayLooseCount = 0
            DayFinalPnL = 0.0
            CombinedIndicatorDF1M = CombinedIndicatorDF3M = CombinedIndicatorDF5M = pd.DataFrame()


            #Loop Row by row from the start row
            for i, (index, DataRow) in enumerate(DFSD.iloc[self._DataLoopStartRow:].iterrows()):   
                absolute_row_index = self._DataLoopStartRow + i
                OrderRow = {}

                #If max loss a day is reached
                if DayFinalPnL <= Const.Max_Loss_Per_Day:
                    break

                #Check if Gap between 2 trades is respected
                EntryTime                           =   self.GetTime(DataRow['timestamp'])
                ExitTimeObj                         =   datetime.strptime(ExitTime, "%H:%M:%S")
                OrderStartTime                      =   datetime.strptime(EntryTime, "%H:%M:%S")
                # Add gap
                NextPossibleEntryTime               =   ExitTimeObj + timedelta(minutes=self._GapBetweenTwoTrades)

                # Now compare
                if self._SingleTradeAtATime and ActiveTrade and (NextPossibleEntryTime >= OrderStartTime):
                    continue

                # Part 1: from start to current row (inclusive)
                DF1 = DFSD.iloc[:absolute_row_index + 1]
                LTP = DataRow["close"]     #DF1.iloc[-1]['close']
                DLChart = ALib.Get_Indicators(DF1, None, True, True, True, True, TE.LiveMode.BackTest, "", False)
                DLStrategyData = ALib.Get_BB_Call(LTP,DF1, DLChart, TE.TradeType.SCALPING, TE.LiveMode.BackTest)
                
                
                
                DLBB = ALib.Get_Volume_Driven_Indicators(DF1, TE.LiveMode.BackTest)

                INDCall, BuyScore, SellScore = ALib.GetIndicatorCall(DLChart, DLBB)
                BBCall  = DLStrategyData["BBCall"]

                #Set the call
                Call = self.GetFinalCAll(INDCall, BBCall)

                #Act as per the Call
                if Call == TE.OrderDirection.PASS:
                    continue
                elif Call == TE.OrderDirection.LEAD:
                    continue
                elif Call == TE.OrderDirection.BUY or TE.OrderDirection.SELL:
                    #Mark order, find when it will be closed
                    
                    SLPrice = DLStrategyData["INDICATORS"]["SLLastPrice"]
                    TargetPrice = DLStrategyData["INDICATORS"]["TargetLastPrice"]
                    OrderID = datetime.now().strftime('%Y%m%d%H%M%S')
                    ActiveTrade = True

                    #set row columns
                    OrderRow["Date"]                    =   Date
                    OrderRow["OrderPrice"]              =   LTP
                    OrderRow["OrderID"]                 =   OrderID
                    OrderRow["SLPrice"]                 =   SLPrice
                    OrderRow["TargetPrice"]             =   TargetPrice
                    OrderRow["OrderInQty"]              =   self._OrderQty
                    OrderRow["OrderOutQty"]             =   self._OrderQty
                    OrderRow["OrderStartTime"]          =   self.GetTime(DataRow['timestamp'])
                    OrderRow["Strategy"]                =   0
                    OrderRow["SYMBOL"]                  =   Symbol
                    OrderRow["Exchange"]                =   0
                    OrderRow["SLPricePerc"]             =   DLStrategyData["SLPricePerc"]
                    OrderRow["TargetPricePerc"]         =   DLStrategyData["TargetPricePerc"]
                    OrderRow["PrimeCandleDuration"]     =   self._CandleDuration

                    DFINDData135                        =   DBO.Get_1_3_5M_Data_For_Timestamp(DataRow['timestamp'], Symbol)

                    #Get 1, 3 and 5 min indicators. Pass IN to set in indicators
                    DI_1M_in = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData1"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="IN", BB=True)
                    DI_3M_in = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData3"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="IN", BB=True)
                    DI_5M_in = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData5"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="IN", BB=True)
                    DI_1M_in["OrderID"] = DI_3M_in["OrderID"] = DI_5M_in["OrderID"] = OrderID

                    # Part 2: from current row + 1 to end
                    DF2 = DFSD.iloc[absolute_row_index + 1:]
                    #Count the distance from the order candle
                    SLHit           =   False
                    TargetHit       =   False
                    EndTimeReached  =   False
                    CandleCount = 0
                    #loop DF2 to find the closing row
                    for index, ResultRow in DF2.iterrows(): 

                        #Increase candle count
                        CandleCount += 1
                        ExitTime                =   self.GetTime(ResultRow["timestamp"])
                        if ResultRow['low'] <= SLPrice <= ResultRow['high']:
                            #SLHit
                            FinalExecutedPrice  =   SLPrice
                            TradeClosingSource  =   "SLHit"
                            SLHit               =   True
                            
                        elif ResultRow['low'] <= TargetPrice <= ResultRow['high']:
                            #TargetHit
                            FinalExecutedPrice  =   TargetPrice
                            TradeClosingSource  =   "TargetHit"
                            TargetHit           =   True
                        elif (self._TimeBound and (ExitTime >= self._StrategyTradingEndTime)) or ExitTime >= self._DayTradingEndTime:
                            FinalExecutedPrice  =   ResultRow['close']
                            TradeClosingSource  =   "TimeOut"
                            EndTimeReached      =   True

                        if SLHit or TargetHit or EndTimeReached:
                            #calculate exp, profit/Loss, Net Profit/Loss
                            #Update the current data row with data
                            if(Call == TE.OrderDirection.SELL):
                                Exp = FLib.Expenses(self._OrderQty, FinalExecutedPrice, self._OrderQty, LTP)
                                PnL = FLib.PnLWithExpenses(self._OrderQty, self._OrderQty, FinalExecutedPrice, LTP)
                            else: #bought at closing
                                Exp = FLib.Expenses(self._OrderQty, LTP, self._OrderQty, FinalExecutedPrice)
                                PnL = FLib.PnLWithExpenses(self._OrderQty, self._OrderQty, LTP,  FinalExecutedPrice)

                            if PnL > 0: 
                                TradeStatusOnPnL = "Success"
                                DayWinCount += 1
                            else: 
                                TradeStatusOnPnL = "Failure"
                                DayLooseCount += 1

                            #Print order result
                            print("\n Date: " + str(Date) + " Order No: " + str(DayOrderCount) + " : " + TradeStatusOnPnL + " PnL: " + str(PnL))

                            OrderRow["OrderExpenses"]       =   Exp
                            OrderRow["PLStatus"]            =   PnL
                            OrderRow["FinalExecutedPrice"]  =   FinalExecutedPrice
                            OrderRow["TradeClosingSource"]  =   TradeClosingSource
                            OrderRow["TradeStatusOnPnL"]    =   TradeStatusOnPnL
                            OrderRow["OrderEndTime"]        =   ExitTime
                            OrderRow["TOTALVALUE"]        =   CandleCount

                            
                            #Get 1, 3 and 5 min indicators. Pass IN to set in indicators
                            DFINDData135                        =   DBO.Get_1_3_5M_Data_For_Timestamp(ResultRow['timestamp'], Symbol)

                            #Get 1, 3 and 5 min indicators. Pass IN to set in indicators
                            DI_1M_out = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData1"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="OUT", BB=True)
                            DI_3M_out = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData3"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="OUT", BB=True)
                            DI_5M_out = ALib.Get_Indicators(DFINDData135["SymbolHistoricalData5"], None, RSI=True, SMA=True, SK=True, MACD=True, LiveMode=TE.LiveMode.BackTest, Postfix="OUT", BB=True)
                            
                            #combine IN and OUT and add to the DFs
                            DI_combined1M = {**DI_1M_in, **DI_1M_out}
                            DI_combined3M = {**DI_3M_in, **DI_3M_out}
                            DI_combined5M = {**DI_5M_in, **DI_5M_out}

                            CombinedIndicatorDF1M = pd.concat([CombinedIndicatorDF1M, pd.DataFrame([DI_combined1M])], ignore_index=True)
                            CombinedIndicatorDF3M = pd.concat([CombinedIndicatorDF3M, pd.DataFrame([DI_combined3M])], ignore_index=True)
                            CombinedIndicatorDF5M = pd.concat([CombinedIndicatorDF5M, pd.DataFrame([DI_combined5M])], ignore_index=True)

                            OrderRows.append(OrderRow)

                            DayOrderCount += 1
                            
                            DayFinalPnL += PnL

                            ActiveTrade = False

                            #TradeFinishTime = self.GetTime()
                            
                            break

                        
            DayWiseDataRow["DayOrderCount"] = DayOrderCount
            DayWiseDataRow["Date"]          = Date
            DayWiseDataRow["DayWinCount"]   = DayWinCount
            DayWiseDataRow["DayLooseCount"] = DayLooseCount
            DayWiseDataRow["DayFinalPnL"]   = DayFinalPnL


            print("\n" + str(DayWiseDataRow))
            DayWiseData.append(DayWiseDataRow)

        OrderDF = pd.DataFrame(OrderRows)
        #set execution timestamp to query the result for one execution
        OrderDF["RunTimestamp"] = datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
        OrderDF = OrderDF.reindex(columns= self.GetColumns("Orders"))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

        #1-3-5 min indicators, BB Indicators and Orders should be saved to DB
        DBO.InsertBTOrderData(OrderDF, CombinedIndicatorDF1M, CombinedIndicatorDF3M, CombinedIndicatorDF5M)
        print("\nReport started at: " + str(ReportStartTime))
        print("\nReport Finished at: " + str(timestamp))
        # Define file path with timestamp
        file_path = fr"D:\AI Trading\Data\OrderDF_{timestamp}.csv"

        # Save to CSV
        OrderDF.to_csv(file_path, index=False)

        # Open the file (Windows only)
        os.startfile(file_path)

        #print(DayWiseData)

                        

    def GetColumns(self, Table):
        OrderColumns = [
    'Date', 'Strategy', 'Watchlist', 'SYMBOL', 'OrderID', 'OrderPrice', 'BULLISH', 'TOTALVALUE',
    'OrderInQty', 'SLPrice', 'SLOrderID', 'TargetPrice', 'TargetOrderID', 'OrderExpenses',
    'OrderClosingType', 'FinalExecutedPrice', 'PLStatus', 'TradeStatus', 'TradeClosingSource',
    'Exchange', 'OrderOutQty', 'BalanceQty', 'TradeType', 'CallType', 'OrderStartTime',
    'OrderEndTime', 'TimeTaken', 'TradeStatusOnPnL', 'Monitoring', 'SLPricePerc', 'SLTargetPerc',
    'PrimaryCandleDuration', 'TotalValueBasis', 'OrderDirection', 'Comments'
    ]
        
        MomentumColumns = [
    'OrderID', 'RSID1IN', 'RSID2IN', 'SK1IN', 'SK2IN', 'SD1IN', 'SD2IN', 'SM501IN', 'SM211IN',
    'RSID1OUT', 'RSID2OUT', 'SK1OUT', 'SK2OUT', 'SD1OUT', 'SD2OUT', 'SM502IN', 'SM212IN',
    'SM501OUT', 'SM502OUT', 'SM211OUT', 'SM212OUT', 'MACD1IN', 'MACD2IN', 'MACDSIGNAL1IN',
    'MACDSIGNAL2IN', 'MACDFAST1IN', 'MACDFAST2IN', 'MACD1OUT', 'MACD2OUT', 'MACDSIGNAL1OUT',
    'MACDSIGNAL2OUT', 'MACDFAST1OUT', 'MACDFAST2OUT', 'VOL1IN', 'VOL2IN', 'VOL1OUT', 'VOL2OUT', 
    'VWAP1', 'VWAP2', 'BBU1', 'BBU2', 'BBM1', 'BBM2', 'BBB1', 'BBB2',
    'TargetBB', 'TargetBBLastPrice', 'SLBB', 'SLBBLastPrice', 'TargetLastPrice',
    'SLLastPrice', 'LTPPosition', 'VWAPPosition', 'MonitoringCriteria',
    'TimeStamp', 'ChartInterval'
    ]
        
        BBColumns = [
    'OrderID', 'VWAP1', 'VWAP2', 'BBU1', 'BBU2', 'BBM1', 'BBM2', 'BBB1', 'BBB2',
    'TargetBB', 'TargetBBLastPrice', 'SLBB', 'SLBBLastPrice', 'TargetLastPrice',
    'SLLastPrice', 'LTPPosition', 'VWAPPosition', 'MonitoringCriteria',
    'TimeStamp', 'ChartInterval'
    ]
        
        if Table == "Orders": return OrderColumns
        elif Table == "Momentum": return MomentumColumns
        elif Table == "BB": return BBColumns
        

    def GetTime(self, TimeStamp):
         return datetime.fromisoformat(TimeStamp).strftime('%H:%M:%S')
    

    def GetFinalCAll(self, INDCall, BBCall):
        Call = TE.OrderDirection.PASS

        if ((INDCall==BBCall and (INDCall==TE.OrderDirection.BUY or INDCall==TE.OrderDirection.SELL)) 
        or 
        (INDCall==TE.OrderDirection.LEAD or INDCall==TE.OrderDirection.PASS)):
            Call = INDCall
        
        
        return Call
    
        #RSIIndicator
        #BBIndicators

        #call SplitDF
        #Call Strategy method, pass first DF
        #If Pass - continue
        #If Lead - Call the lead function of strategy
        #   return the call (buy/sell) 
        #If Buy/Sell 
        #   Call Analyse result
        #   Return result details
        #   update row with the results
        #Once loop is finished, 
        #Call ExecutionPath
