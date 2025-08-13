from LibDBBase import DBBase
#import LibDBBase

from datetime import date
#from datetime import datetime
from LibEnum import TradingEnums as TE
from LibGeneric import GeneicLib as GL
#from LibAnalysis import AnaLysisLib as ALib
#from LibTrading import TradingLib
import pandas as pd
#from LibDhan import Dhan
import sys

class DBOps(DBBase):
    def __init__(self):
        super().__init__()
        self.today       =   str(date.today())


    def CreateOrderInDB(self, DL):

        Query = 'INSERT INTO Orders (Date, Strategy, Watchlist, OrderID,  OrderPrice, SYMBOL, BULLISH,TOTALVALUE,' \
                        'OrderInQty,  SLPrice, SLOrderID, TargetPrice, TargetOrderID,   OrderExpenses,' \
                        'OrderClosingType,' \
                        'Exchange, BalanceQty, TradeType, CallType, OrderStartTime, ' \
                        'Monitoring, SLPricePerc, SLTargetPerc, TradeStatus, PrimaryCandleDuration, TotalValueBasis, OrderDirection, Comments)' \
                            'VALUES ' \
                        '('+ '"' + str(self.today) + '"' + ', :Strategy, :Watchlist, :OrderID, :OrderPrice,  :SYMBOL, :BULLISH, :TOTALVALUE,' \
                        ':OrderInQty, :SLPrice,  :SLOrderID, :TargetPrice, :TargetOrderID, :OrderExpenses,' \
                        ':OrderClosingType,' \
                        ':Exchange, :BalanceQty, :TradeType, :CallType, :OrderStartTime,' \
                        ' :Monitoring, :SLPricePerc, :TargetPricePerc, 1, :PrimaryCandleDuration, :TotalValueBasis, :OrderDirection, :Comments)'

        self.UpdateWithDL(Query, DL)

    def UpdateInOrderMomentumIndicators(self, DL1M=None, DL3M=None, DL5M=None):
        #1M
        if DL1M is not None:
            sql_insert1M = """
            INSERT INTO OrderMomentumIndicators1M (
                OrderID,RSID1IN,RSID2IN,SK1IN,SK2IN,SD1IN,SD2IN,SM501IN,SM211IN,SM502IN,SM212IN,MACD1IN,MACD2IN,MACDSIGNAL1IN,MACDSIGNAL2IN,MACDFAST1IN,MACDFAST2IN,VOL1IN,VOL2IN
            )
            VALUES (
                :OrderID,:RSID1,:RSID2,:SK1,:SK2,:SD1,:SD2,:SM501,:SM211,:SM502,:SM212,:MACD1,:MACD2,:MACDSIGNAL1,:MACDSIGNAL2,
                :MACDFAST1,:MACDFAST2, :VOL1, :VOL2
            );
            """
            self.UpdateWithDL(sql_insert1M, DL1M)
        #3M
        if DL3M is not None:
            sql_insert3M = """
            INSERT INTO OrderMomentumIndicators3M (
                OrderID,RSID1IN,RSID2IN,SK1IN,SK2IN,SD1IN,SD2IN,SM501IN,SM211IN,SM502IN,SM212IN,MACD1IN,MACD2IN,MACDSIGNAL1IN,MACDSIGNAL2IN,MACDFAST1IN,MACDFAST2IN,VOL1IN,VOL2IN
            )
            VALUES (
                :OrderID,:RSID1,:RSID2,:SK1,:SK2,:SD1,:SD2,:SM501,:SM211,:SM502,:SM212,:MACD1,:MACD2,:MACDSIGNAL1,:MACDSIGNAL2,
                :MACDFAST1,:MACDFAST2, :VOL1, :VOL2
            );
            """
            self.UpdateWithDL(sql_insert3M, DL3M)
        #5M
        if DL5M is not None:
            sql_insert5M = """
            INSERT INTO OrderMomentumIndicators5M (
                OrderID,RSID1IN,RSID2IN,SK1IN,SK2IN,SD1IN,SD2IN,SM501IN,SM211IN,SM502IN,SM212IN,MACD1IN,MACD2IN,MACDSIGNAL1IN,MACDSIGNAL2IN,MACDFAST1IN,MACDFAST2IN,VOL1IN,VOL2IN
            )
            VALUES (
                :OrderID,:RSID1,:RSID2,:SK1,:SK2,:SD1,:SD2,:SM501,:SM211,:SM502,:SM212,:MACD1,:MACD2,:MACDSIGNAL1,:MACDSIGNAL2,
                :MACDFAST1,:MACDFAST2, :VOL1, :VOL2
            );
            """
            self.UpdateWithDL(sql_insert5M, DL5M)

    def UpdateOutOrderMomentumIndicators(self, OrderID, DL1M, DL3M, DL5M):
        #Get symbol from Orders table
        Query = "select symbol from Orders where OrderID=?"
        Params = (OrderID,)
        #Symbol = DBBase.ScalarQuery(Query, Params)
        
        #Get tsl connection
        #DH              = Dhan()
        #Conn             =   DH.DhanConnection

        

        #1M
        sql_update1M = """
        UPDATE OrderMomentumIndicators1M
        SET
            RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
            SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
            MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        WHERE
            OrderID=:OrderID
        """
        self.UpdateWithDL(sql_update1M, DL1M)

        #3M
        sql_update3M = """
        UPDATE OrderMomentumIndicators3M
        SET
            RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
            SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
            MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        WHERE
            OrderID=:OrderID
        """

        self.UpdateWithDL(sql_update3M, DL3M)

        sql_update5M = """
        UPDATE OrderMomentumIndicators5M
        SET
            RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
            SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
            MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        WHERE
            OrderID=:OrderID
        """

        self.UpdateWithDL(sql_update5M, DL5M)

    def UpdateOrder(self, DL):
        
        Query = 'update Orders set OrderExpenses=:OrderExpenses, FinalExecutedPrice=:FinalExecutedPrice, PLStatus=:PLStatus,' \
        'TradeStatus=:TradeStatus, TradeClosingSource=:TradeClosingSourceName, OrderOutQty=:OrderOutQty, BalanceQty=:BalanceQty, OrderEndTime=:OrderEndTime,' \
        'TimeTaken=:TimeTaken, TradeStatusOnPnL=:TradeStatusOnPnL where OrderID=:OrderID'

        self.UpdateWithDL(Query, DL)
        #self.UpdateOutOrderMomentumIndicators(DL["OrderID"], ExchangeName)

    def UpdateOrderTargetSL(self, DL):
        
        Query = 'update Orders set SLOrderID=:SLOrderID, TargetOrderID=:TargetOrderID, SLPrice=:SLPrice,' \
        'TargetPrice=:TargetPrice where OrderID=:OrderID'

        self.UpdateWithDL(Query, DL)

    def GetActiveOrders(self, StrategyData=False, Strategy=TE.Strategy.All):
        #Query
        if Strategy==TE.Strategy.All:
            Query = "Select * from Orders where Date = ? and TradeStatus=? order by Strategy"
            StrategyQuery = "select StrategyID,StrategyName, count(OrderID) as count,st.TradeMonitorScript, st.LeadMonitorScript  from Orders od join Strategies st on od.Strategy=st.StrategyID where Date = ? and TradeStatus=? group by Strategy order by count"
            #TradingLib.today = TradingLib.today + dt.timedelta(days=1)
            Params = (str(self.today),TE.TradeStatus.Active.value,)
            #Strategy_Params = (str(TradingLib.today),2,)
        else:
            Query = "Select * from Orders where Date = ? and TradeStatus=? and Strategy=?"
            params = (str(self.today),TE.TradeStatus.Active.value, Strategy.value,)

        # Use pandas to execute the query and load results into a DataFrame
        if StrategyData:
            #DF = pd.read_sql_query(Query, DBConn, params=Params)
            #GDF = pd.read_sql_query(StrategyQuery, DBConn, params=Params)
            DF = self.DFReadSQLQuery(Query, Params)
            GDF = self.DFReadSQLQuery(StrategyQuery, Params)
            #DBConn.close()
            return DF, GDF
        else:
            #DF = pd.read_sql_query(Query, DBConn, params=Params)
            DF = self.DFReadSQLQuery(Query, Params)
            #DBConn.close()
            return DF
        

    def GetTodayPnL(self):
        RealisedPnLQuery        =   "select sum(PLStatus) as RealisedPnL from Orders where Date=? and PLStatus is not NULL"
        UnrealisedExpQuery      =   "select sum(OrderExpenses) as Exp from Orders where Date=? and PLStatus is NULL"
        UnrealisedSLQuery       =   "select sum((SLPricePerc/100)*Orderprice*BalanceQty) as UnrealisedPnL from Orders where Date=? and PLStatus is NULL"
        Param                   =   (str(self.today),) 
        RealisedPnL             =   self.ScalarQuery(RealisedPnLQuery, Param)
        UnrealisedExp           =   self.ScalarQuery(UnrealisedExpQuery, Param)
        UnrealisedSL            =   self.ScalarQuery(UnrealisedSLQuery, Param)

        return RealisedPnL, UnrealisedExp, UnrealisedSL


    def GetStrategyDetails(self, Strategy = TE.Strategy.All):
        #DBConn = LibDBOps.GetDBConn()        

        if Strategy == TE.Strategy.All:
            Query = "select * from Strategies"
            #DF = pd.read_sql_query(Query, DBConn)
            DF = self.DFReadSQLQuery(Query)
            #DBConn.close()
            return DF
        else:
            Query = "select * from Strategies where StrategyID = ? "
            Params = (str(Strategy.value),) 
            #DF = pd.read_sql_query(Query, DBConn, params=Params)
            DF = self.DFReadSQLQuery(Query, Params)
            #DBConn.close()
            return DF.iloc[0].to_dict()
        

    def GetKillSwitch(self):
        #PnL, RealisedPnL            =       TradingLib.GetTodayPnL()
        #TradeCount                  =       15
        
        SelectQueryKillSwitch = "Select KillSwitchIsOn from KillSwitch where Date=?"
        Params                = (str(self.today),)
        KillSwitch            = self.ScalarQuery(SelectQueryKillSwitch, Params)

        return KillSwitch

    def SetKillSwitch(self):
        UpdateQueryKillSwitch = "Update KillSwitch Set KillSwitchIsOn=1 where Date=?"
        Params                = (str(self.today),)
        return self.ScalarQuery(UpdateQueryKillSwitch, Params)


    #verify whether stock is already in open state
    def IsStockActive(self, Symbol):
        Query = "select count(OrderID) as Count from Orders where Date=? and Symbol=? and TradeClosingSource is NULL"
        
        Params                = (str(self.today), Symbol,)
        return (self.ScalarQuery(Query, Params) > 0)
    

    def GetOrdersCountFromDB(self, Strategy=None, Status=TE.TradeStatus.Active):
        if Status==TE.TradeStatus.Active:
            StatusQuery = " and TradeClosingSource is NULL "
        elif  Status==TE.TradeStatus.Completed: 
            StatusQuery = " and TradeClosingSource is not NULL "
        else:
            StatusQuery = ""

        if Strategy is None:
            Query   = "select count(OrderID) as Count from Orders where Date=? " + StatusQuery
            Params  = (str(self.today),)
        else:
            Query = "select count(OrderID) as Count from Orders where Date=? and Strategy=? " + StatusQuery
            Params  = (str(self.today), Strategy,)

        return self.ScalarQuery(Query, Params)
    
    def SetTodayPrices(self, TOP, TOPGreaterPDP, RowID):
        query = '''
            UPDATE HistoricalMomentumData
            SET TOP = ?, PRICEUP = ?
            WHERE rowid = ?
            '''
        params = (TOP, TOPGreaterPDP, RowID)
        self.ExecuteUpdateQuery(query, params)

    def SaveIndexMomentumData(self, DF):
        DBConn = self.DBConnection
        DF.to_sql("IndexMomentumData", DBConn , if_exists="append", index=False)

    
    def SaveHistoricalMomentumData(self, DF):
        DBConn = self.DBConnection
        DF.to_sql("HistoricalMomentumData", DBConn, if_exists="append", index=False)


    def Get_Historical_Momentum_Data_From_DB(self, WatchlistDate, Columns = "rowid, *", WatchlistID = 0):
          # Query to fetch data
          # "SYMBOL, DIRECTION, BULLISH "
        if WatchlistID==TE.Watchlist_Type.INDEXES.value:
            query = "SELECT " + Columns + " from IndexMomentumData where Date='" + str(WatchlistDate) +"'"
        else:
            query = "SELECT " + Columns + " from HistoricalMomentumData where Date='" + str(WatchlistDate) +"' and WatchlistID=" + str(WatchlistID)

        DBconn = self.DBConnection
        # Load data into a DataFrame
        df = pd.read_sql_query(query, DBconn)

        #if df = none then fetch the data

        # Close the connection
        DBconn.close()
        return df
    

    def SetTodayTradingStream(self, Symbol, WatchlistID):
        #call GetTodayTradingStream()
        #if not avalable then analyze
        #Analyse indexes and decide where to trade today
        #Symbol = None
        #WatchlistID = -1

        
        #update db record
        Query = "insert into todaywatchlist (WatchlistDate, IndexSymbol, WatchlistID) values (?,?,?)"
        Params = (str(self.today), Symbol, WatchlistID)
        
        DBconn = self.DBConnection
        cursor = DBconn.cursor()
        cursor.execute(Query, Params)

        DBconn.commit()
        
        return WatchlistID, Symbol
    

    def GetTodayTradingStream(self):
        #Get Today Stream from db
        #if not avalable then analyze
        #Analyse indexes and decide where to trade today
        Query = "select watchlistid, indexsymbol from todaywatchlist where WATCHLISTDATE = ?"
        Params = (str(self.today),)
        #if not available call SetTodayTradingStream() columns Date, Stream
        #Fetch the symbols for today's stream
        #return df
        DBconn = self.DBConnection
        cursor = DBconn.cursor()

        # Example: Get a scalar value (e.g., count of rows in a table)
        cursor.execute(Query, Params)
        result = cursor.fetchone()
        cursor.close()
        DBconn.close() 
        return result
    

    def GetWatchlistFromDB(self, ListType):
        Query = "SELECT SYMBOL from WatchlistStocks where WATCHLISTTYPE=?"
        Params = (str(ListType.value),)
        return self.OneColumnListQuery(Query, Params)    

    def IsHistoricalDataLoaded(self, WatchlistID):
        Query = "select count(Symbol) as Count from HistoricalMomentumData where Date=? and WatchlistID=?"
        
        Params                = (str(self.today), WatchlistID,)
        return (self.ScalarQuery(Query, Params) > 0)
        # Insert the DataFrame into a table named 'flags'
        #df.to_sql("flags", conn, if_exists="replace", index=False)

    def GetTodaysWatchListID(self):  
        Query = "select WatchlistID from TodayWatchlist where WatchlistDate=?"
        
        Params                = (str(self.today),)
        return self.ScalarQuery(Query, Params)
    
    def CheckHolidays(self):
        excluded_dates = []
        with open("Holidays.txt") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Skip empty lines and full-line comments
                line = line.split("#")[0].strip()  # Remove inline comments
                try:
                    excluded_dates.append(date.fromisoformat(line))
                except ValueError:
                    print(f"Skipping invalid date line: {line}")

        if date.today() in excluded_dates:
            print("Today is a holiday. Skipping script.")
            sys.exit()

        print("Running main script...")


    def isHistoricalOnRun(self, Time):
        Query   = "select HMDOnRun, Date, Time from HistoricalMomentumDataOnRun where date=?"
        Params  = (str(self.today), )
        DBconn = self.DBConnection

        cursor = DBconn.cursor()
        
        # Example: Get a scalar value (e.g., count of rows in a table)
        cursor.execute(Query, Params)
        result = cursor.fetchone()

        if result is None:
            State = 0
            self.SetHistoricalRunState(State, Time)
        elif result[0]==1 and GL.GetTimeDiff(result[2], Time,  True)>=300:
            State = 0
            self.SetHistoricalRunState(State, Time)
        else:
            State =result[0]

        return (State == 1)
    
    def SetHistoricalRunState(self, State, Time):
        Query   = "Update HistoricalMomentumDataOnRun set date=?, HMDOnRun=?, Time=?"
        Params  = (str(self.today), State, Time)

        self.ExecuteUpdateQuery(Query, Params)

    """ def isTwoSistersOnRun(self):
        Query   = "select TSOnRun from HistoricalMomentumDataOnRun where date=?"
        Params  = (str(self.today),)

        State = self.ScalarQuery(Query, Params)

        return (State == 1)
    
    def SetTwoSistersRunState(self, State):
        Query   = "Update HistoricalMomentumDataOnRun set TSOnRun=? where date=?"
        Params  = (State, str(self.today),)

        self.ExecuteUpdateQuery(Query, Params) """

    def GetSymbolLastTradeClosingTime(self, Symbol):
        Query   =   "select OrderEndTime from Orders where Symbol=? and Date=? order by OrderID Desc"

        Params  = (Symbol, str(self.today),)
        return self.ScalarQuery(Query, Params)
    
    def InsertOrderBBData(self, DL):

        Query = 'INSERT INTO OrderBBIndicators (OrderID, VWAP1, VWAP2, BBU1,BBU2, BBM1, BBM2, BBB1, BBB2, TargetBB, TargetBBLastPrice,SLBB,' \
                                 'SLBBLastPrice, TargetLastPrice, SLLastPrice, LTPPosition, VWAPPosition, TimeStamp, ChartInterval)' \
                              'VALUES '\
			                                  '(:OrderID, :VWAP1, :VWAP2, :BBU1, :BBU2, :BBM1, :BBM2, :BBB1, :BBB2, :TargetBB, :TargetBBLastPrice,:SLBB,' \
                                 ':SLBBLastPrice, :TargetLastPrice, :SLLastPrice, :LTPPosition, :VWAPPosition, :TimeStamp, :ChartInterval)'


        self.UpdateWithDL(Query, DL)

    def UpdateOrderBBData(self, DL):
        Query = 'update OrderBBIndicators set TargetBBLastPrice=:TargetBBLastPrice, SLBBLastPrice=:SLBBLastPrice, TargetLastPrice=:TargetLastPrice,' \
             ' TimeStamp=:TimeStamp, SLLastPrice=:SLLastPrice where OrderID=:OrderID' 
        
        self.UpdateWithDL(Query, DL)

    def GetOrderBBData(self, OrderID):
        Query = 'select * from OrderBBIndicators where OrderID=?'
        Params  = (OrderID,)

        DF = self.DFReadSQLQuery(Query, Params)

        if not DF.empty:
            return DF.iloc[0].to_dict()
        else:
            return None
        
    def GetSymbolDates(self, Symbol):
        Query = "SELECT DISTINCT Date FROM SymbolHistoricalData WHERE Symbol = ? ORDER BY Date"
        Params  = (Symbol,)
        return self.OneColumnListQuery(Query, Params) 
        

    def GetSymbolHistDataForADate(self, Symbol, Date):
        Query = 'select * from SymbolHistoricalData where Symbol = ? and Date = ? order by timestamp'
        Params  = (Symbol, Date,)

        return self.DFReadSQLQuery(Query, Params)
    
    def InsertSymbolHistData(self, df, Candle):
        DBConn = self.DBConnection
        df.to_sql(("SymbolHistoricalData"+str(Candle)), DBConn, if_exists="append", index=False) 

    def Get_1_3_5M_Data_For_Timestamp(self, Timestamp, Symbol):

        tables = {
            'SymbolHistoricalData1': 1,
            'SymbolHistoricalData3': 3,
            'SymbolHistoricalData5': 5
        }

        Params = (Timestamp, Symbol)
        result = {}

        for table, interval in tables.items():
            Query = f"""
                SELECT * FROM {table}
                WHERE timestamp <= ? and symbol=?
                ORDER BY timestamp DESC
                LIMIT 2;
            """
            #df = pd.read_sql_query(query, DBConn, params=(Timestamp,))
            df = self.DFReadSQLQuery(Query, Params)
            result[table] = df

        return result  # returns a dict of 3 DataFrames
    
    def InsertBTOrderData(self, DFOrders, DFIndicators1M, DFIndicators3M, DFIndicators5M):
        self.InsertFromDF("BTOrders", DFOrders)
        self.InsertFromDF("BTOrderMomentumIndicators1M", DFIndicators1M)
        self.InsertFromDF("BTOrderMomentumIndicators3M", DFIndicators3M)
        self.InsertFromDF("BTOrderMomentumIndicators5M", DFIndicators5M)

    def GetSymbolHistLastDate(self, Symbol):
        Query = "select max(date) from SymbolHistoricalData1 where symbol = ?"
        Params = (Symbol,)
        return self.ScalarQuery(Query,Params)

        