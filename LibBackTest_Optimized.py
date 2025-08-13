import os
import pandas as pd
from datetime import datetime, timedelta
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from LibDBOps import DBOps
from LibAnalysis import AnaLysisLib
from LibEnum import TradingEnums as TE
from LibFinance import FinLib
from datetime import datetime, timedelta
from LibConstants import Const
from LibBackTest_Plotting import BTPlotter

# Assume TE, Const, ALib, FLib, DBOps, AnaLysisLib, FinLib are already imported or defined elsewhere

class BTIntradayEngine:
    
    def __init__(self):
        self._OrderQty = 1
        self._CandleDuration = "1m"
        self._GapBetweenTwoTrades = 5
        self._DataLoopStartRow = 0
        self._SingleTradeAtATime = True
        self._TimeBound = True
        self._StrategyTradingEndTime = "14:45:00"
        self._DayTradingEndTime = "15:15:00"
        self._IndicatorCache = {}

    def GetSymbolDates(self, Symbol):
        raise NotImplementedError("Define method to get trading dates for the symbol.")

    def GetSymbolData(self, Symbol, Date):
        raise NotImplementedError("Define method to fetch 1-minute OHLCV data.")

    def GetFinalCAll(self, INDCall, BBCall):
        raise NotImplementedError("Define method to resolve final trade signal.")

    def GetTime(self, timestamp):
        return pd.to_datetime(timestamp).strftime("%H:%M:%S")

    def GetColumns(self, TableName):
        return [
            "Date", "OrderPrice", "OrderID", "SLPrice", "TargetPrice",
            "OrderInQty", "OrderOutQty", "OrderStartTime", "Strategy",
            "SYMBOL", "Exchange", "SLPricePerc", "TargetPricePerc",
            "PrimeCandleDuration", "OrderExpenses", "PLStatus",
            "FinalExecutedPrice", "TradeClosingSource", "TradeStatusOnPnL",
            "OrderEndTime", "TOTALVALUE", "RunTimestamp"
        ]

    @lru_cache(maxsize=2048)
    def get_cached_135m_indicator_data(self, timestamp_str, symbol):
        DBO = DBOps()
        ALib = AnaLysisLib()
        data = DBO.Get_1_3_5M_Data_For_Timestamp(timestamp_str, symbol)
        return {
            "1M_IN": ALib.Get_Indicators(data["SymbolHistoricalData1"], None, True, True, True, True, TE.LiveMode.BackTest, "IN", True),
            "3M_IN": ALib.Get_Indicators(data["SymbolHistoricalData3"], None, True, True, True, True, TE.LiveMode.BackTest, "IN", True),
            "5M_IN": ALib.Get_Indicators(data["SymbolHistoricalData5"], None, True, True, True, True, TE.LiveMode.BackTest, "IN", True),
            "1M_OUT": ALib.Get_Indicators(data["SymbolHistoricalData1"], None, True, True, True, True, TE.LiveMode.BackTest, "OUT", True),
            "3M_OUT": ALib.Get_Indicators(data["SymbolHistoricalData3"], None, True, True, True, True, TE.LiveMode.BackTest, "OUT", True),
            "5M_OUT": ALib.Get_Indicators(data["SymbolHistoricalData5"], None, True, True, True, True, TE.LiveMode.BackTest, "OUT", True)
        }

    def get_exit_indicators_with_cache(self, Symbol, ResultRow):
        exit_timestamp = ResultRow['timestamp']
        key_1M = f"{Symbol}_1M_{exit_timestamp}_OUT"
        key_3M = f"{Symbol}_3M_{exit_timestamp}_OUT"
        key_5M = f"{Symbol}_5M_{exit_timestamp}_OUT"

        if key_1M not in self._IndicatorCache:
            DFINDData135 = DBOps().Get_1_3_5M_Data_For_Timestamp(exit_timestamp, Symbol)

            self._IndicatorCache[key_1M] = AnaLysisLib().Get_Indicators(
                DFINDData135["SymbolHistoricalData1"], None,
                RSI=True, SMA=True, SK=True, MACD=True, BB=True,
                LiveMode=TE.LiveMode.BackTest, Postfix="OUT"
            )
            self._IndicatorCache[key_3M] = AnaLysisLib().Get_Indicators(
                DFINDData135["SymbolHistoricalData3"], None,
                RSI=True, SMA=True, SK=True, MACD=True, BB=True,
                LiveMode=TE.LiveMode.BackTest, Postfix="OUT"
            )
            self._IndicatorCache[key_5M] = AnaLysisLib().Get_Indicators(
                DFINDData135["SymbolHistoricalData5"], None,
                RSI=True, SMA=True, SK=True, MACD=True, BB=True,
                LiveMode=TE.LiveMode.BackTest, Postfix="OUT"
            )

        return (
            self._IndicatorCache[key_1M],
            self._IndicatorCache[key_3M],
            self._IndicatorCache[key_5M]
        )

    def _ProcessSingleDay(self, Symbol, Date):
        ALib = AnaLysisLib()
        FLib = FinLib()
        DBO = DBOps()

        DFSD = self.GetSymbolData(Symbol, Date)
        OrderRows, indicators_1m, indicators_3m, indicators_5m = [], [], [], []
        DayOrderCount = DayWinCount = DayLooseCount = 0
        DayFinalPnL = 0.0
        ActiveTrade = False
        ExitTime = datetime.now().strftime(Const.Time_Format)

        for i, (index, DataRow) in enumerate(DFSD.iloc[self._DataLoopStartRow:].iterrows()):
            absolute_row_index = self._DataLoopStartRow + i
            if DayFinalPnL <= Const.Max_Loss_Per_Day:
                break

            EntryTime = self.GetTime(DataRow['timestamp'])
            OrderStartTime = datetime.strptime(EntryTime, "%H:%M:%S")
            ExitTimeObj = datetime.strptime(ExitTime, "%H:%M:%S")
            if self._SingleTradeAtATime and ActiveTrade and (ExitTimeObj + timedelta(minutes=self._GapBetweenTwoTrades)) >= OrderStartTime:
                continue

            DF1 = DFSD.iloc[:absolute_row_index + 1]
            LTP = DataRow["close"]
            DLChart = ALib.Get_Indicators(DF1, None, True, True, True, True, TE.LiveMode.BackTest, "", False)
            DLBB = ALib.Get_Volume_Driven_Indicators(DF1, TE.LiveMode.BackTest)
            DLStrategyData = ALib.Get_BB_Call(LTP, DF1, DLChart, TE.TradeType.SCALPING, TE.LiveMode.BackTest)

            Call = self.GetFinalCAll(*ALib.GetIndicatorCall(DLChart, DLBB), DLStrategyData["BBCall"])
            if Call not in [TE.OrderDirection.BUY, TE.OrderDirection.SELL]:
                continue

            OrderID = datetime.now().strftime('%Y%m%d%H%M%S')
            SLPrice = DLStrategyData["INDICATORS"]["SLLastPrice"]
            TargetPrice = DLStrategyData["INDICATORS"]["TargetLastPrice"]
            OrderRow = {
                "Date": Date, "OrderPrice": LTP, "OrderID": OrderID, "SLPrice": SLPrice,
                "TargetPrice": TargetPrice, "OrderInQty": self._OrderQty, "OrderOutQty": self._OrderQty,
                "OrderStartTime": EntryTime, "Strategy": 0, "SYMBOL": Symbol, "Exchange": 0,
                "SLPricePerc": DLStrategyData["SLPricePerc"], "TargetPricePerc": DLStrategyData["TargetPricePerc"],
                "PrimeCandleDuration": self._CandleDuration
            }

            data135 = self.get_cached_135m_indicator_data(DataRow["timestamp"], Symbol)
            DI_1M_in = data135["1M_IN"]; DI_1M_in["OrderID"] = OrderID
            DI_3M_in = data135["3M_IN"]; DI_3M_in["OrderID"] = OrderID
            DI_5M_in = data135["5M_IN"]; DI_5M_in["OrderID"] = OrderID

            SLHit = TargetHit = EndTimeReached = False
            CandleCount = 0
            for _, ResultRow in DFSD.iloc[absolute_row_index + 1:].iterrows():
                CandleCount += 1
                ExitTime = self.GetTime(ResultRow["timestamp"])
                low, high = ResultRow['low'], ResultRow['high']

                if low <= SLPrice <= high:
                    FinalExecutedPrice = SLPrice
                    TradeClosingSource = "SLHit"
                    SLHit = True
                elif low <= TargetPrice <= high:
                    FinalExecutedPrice = TargetPrice
                    TradeClosingSource = "TargetHit"
                    TargetHit = True
                elif (self._TimeBound and ExitTime >= self._StrategyTradingEndTime) or ExitTime >= self._DayTradingEndTime:
                    FinalExecutedPrice = ResultRow['close']
                    TradeClosingSource = "TimeOut"
                    EndTimeReached = True

                if SLHit or TargetHit or EndTimeReached:
                    if Call == TE.OrderDirection.SELL:
                        Exp = FLib.Expenses(self._OrderQty, FinalExecutedPrice, self._OrderQty, LTP)
                        PnL = FLib.PnLWithExpenses(self._OrderQty, self._OrderQty, FinalExecutedPrice, LTP)
                    else:
                        Exp = FLib.Expenses(self._OrderQty, LTP, self._OrderQty, FinalExecutedPrice)
                        PnL = FLib.PnLWithExpenses(self._OrderQty, self._OrderQty, LTP, FinalExecutedPrice)

                    TradeStatusOnPnL = "Success" if PnL > 0 else "Failure"
                    DayWinCount += (PnL > 0)
                    DayLooseCount += (PnL <= 0)
                    DayFinalPnL += PnL
                    DayOrderCount += 1

                    print(f"\n Date: {Date} Order No: {DayOrderCount} : {TradeStatusOnPnL} PnL: {PnL}")

                    OrderRow.update({
                        "OrderExpenses": Exp, "PLStatus": PnL, "FinalExecutedPrice": FinalExecutedPrice,
                        "TradeClosingSource": TradeClosingSource, "TradeStatusOnPnL": TradeStatusOnPnL,
                        "OrderEndTime": ExitTime, "TOTALVALUE": CandleCount
                    })

                    DI_1M_out, DI_3M_out, DI_5M_out = self.get_exit_indicators_with_cache(Symbol, ResultRow)

                    indicators_1m.append({**DI_1M_in, **DI_1M_out})
                    indicators_3m.append({**DI_3M_in, **DI_3M_out})
                    indicators_5m.append({**DI_5M_in, **DI_5M_out})
                    OrderRows.append(OrderRow)
                    ActiveTrade = False
                    break

        return {
            "Orders": OrderRows,
            "Indicators1M": indicators_1m,
            "Indicators3M": indicators_3m,
            "Indicators5M": indicators_5m,
            "DayStats": {
                "Date": Date, "DayOrderCount": DayOrderCount,
                "DayWinCount": DayWinCount, "DayLooseCount": DayLooseCount,
                "DayFinalPnL": DayFinalPnL
            }
        }

    def BTIntraday(self, Symbol):
        ListDates = self.GetSymbolDates(Symbol)
        ReportStartTime = datetime.now()
        print(f"\nBacktest started at: {ReportStartTime}")

        AllOrderRows, indicators_1m, indicators_3m, indicators_5m, DayWiseData = [], [], [], [], []

        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda date: self._ProcessSingleDay(Symbol, date), ListDates))

        for res in results:
            AllOrderRows += res["Orders"]
            indicators_1m += res["Indicators1M"]
            indicators_3m += res["Indicators3M"]
            indicators_5m += res["Indicators5M"]
            DayWiseData.append(res["DayStats"])
            print(f"\n{res['DayStats']}")

        OrderDF = pd.DataFrame(AllOrderRows)
        OrderDF["RunTimestamp"] = datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
        OrderDF = OrderDF.reindex(columns=self.GetColumns("Orders"))

        CombinedIndicatorDF1M = pd.DataFrame(indicators_1m)
        CombinedIndicatorDF3M = pd.DataFrame(indicators_3m)
        CombinedIndicatorDF5M = pd.DataFrame(indicators_5m)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = fr"D:\AI Trading\Data\OrderDF_{timestamp}.csv"

        DBOps().InsertBTOrderData(OrderDF, CombinedIndicatorDF1M, CombinedIndicatorDF3M, CombinedIndicatorDF5M)

        print(f"\nBacktest finished at: {datetime.now()} (started at {ReportStartTime})")
        OrderDF.to_csv(file_path, index=False)
        plotter = BTPlotter(OrderDF, output_dir="D:/AI Trading/Plots", symbol="RELIANCE")
        plotter.plot_all()

        os.startfile(file_path)
