from Dhan_Tradehull import Tradehull
import pandas as pd
from LibEnum import TradingEnums as TE
from LibFinance import FinLib
from LibDBBase import DBBase
from LibDBOps import DBOps
from LibDhan import Dhan

import LibDBBase
from datetime import date
from datetime import datetime, timedelta
from LibConstants import Const
import datetime as dt
from LibGeneric import GeneicLib as GL
from LibAnalysis import AnaLysisLib

# Create Simple order

# Create SL Order
# Create SL Target Order
# Cancel Target Order
# Cancel Order (including SL and Target)
# Trail SL
# Close all positions
# Cancel all pending orders
# Close a position
# Today's number of Trades
# Today's profitable trades
# Today's loss trades
# Is order stagnated
# Is a better opportunity (If yes then we can exit from a slow moving or stangnent position)


curr_time   =   datetime.now().strftime(Const.Time_Format)   

class TradingLib:
    FLib = FinLib()
    #con = Connection()
    today       =   str(date.today())
    

    def CreateOrder(self, Con, Symbol, Exchange, Qty, Price, TriggerPrice, OrderType, TransactionType, TradeType):
        return Con.order_placement(tradingsymbol=Symbol ,exchange=Exchange, quantity=Qty, price=Price, trigger_price=TriggerPrice, order_type=OrderType, transaction_type=TransactionType,   trade_type=TradeType)
    
    def CancelOrder(self, Con, CancelOrderID):
    
        Order_status  = Con.get_order_status(orderid=CancelOrderID)
        if Order_status== TE.OrderStatus.TRANSIT.name or TE.OrderStatus.PENDING.name:
            Con.cancel_order(OrderID=CancelOrderID)

    def ModifyOrder(self, Con, Qty, TargetOrderID=None, TargetOrderPrice=None, SLOrderID=None, SLOrderPrice=None, Symbol=None, Exchange=None, ReverseOrderDirection=None, TradeType=None, OrderID = None):
        if TargetOrderID is not None and TargetOrderPrice is not None:
            modified_order = Con.modify_order(order_id=TargetOrderID,order_type="LIMIT",quantity=Qty,price=TargetOrderPrice)

        if SLOrderID is not None:    
            #SLOrderID = Con.modify_order(order_id=SLOrderID,order_type="STOPLIMIT",quantity=Qty,price=SLOrderPrice, trigger_price=SLOrderPrice)
            # as per chatgpt, I should use SL not STOPLIMIT
            #SLOrderID = Con.modify_order(order_id=SLOrderID,order_type='STOPLIMIT',quantity=Qty,price= (SLOrderPrice-0.05), trigger_price=SLOrderPrice, disclosed_quantity=0, validity='DAY',leg_name = 'STOP_LOSS_LEG' )
            
            #Cancel previous SL Order
            CancelledSLOrderID = Con.cancel_order(OrderID=SLOrderID)
            #Add new SL Order
            SLOrderID = TradingLib.CreateOrder(self, Con,Symbol, Exchange.name, Qty, 0, SLOrderPrice, TE.OrderType.STOPMARKET.name, ReverseOrderDirection.name, TradeType.name)
            
        #Update DB Record
        DL                      =   {}
        DL["SLOrderID"]         =   SLOrderID
        DL["TargetOrderID"]     =   TargetOrderID
        DL["SLPrice"]           =   SLOrderPrice
        DL["TargetPrice"]       =   TargetOrderPrice
        DL["OrderID"]           =   OrderID

        DBO = DBOps()
        DBO.UpdateOrderTargetSL(DL)

        

    def Order(self, Con, Strategy, Watchlist, Symbol, Bullish, TotalValue, Exchange, OrderGroupType, Qty, TradeType, CallType, OrderDirection,   SLPricePerc=0, TargetPricePerc=0, PrimaryCandleDuration=0, TotalValueBasis=0,LimitPrice=0, SLPrice=0, TargetPrice=0, ParentOrderID=0):
        DL = {}
        OrderPrice = 0
        SLOrderID = 0
        TargetOrderID = 0
        Expenses = 0.0
        curr_time   =   datetime.now().strftime(Const.Time_Format)  
        #New Order
        if ParentOrderID==0:
            if OrderDirection == TE.OrderDirection.BUY:
                ReverseOrderDirection = TE.OrderDirection.SELL
            else:
                ReverseOrderDirection = TE.OrderDirection.BUY

            if OrderGroupType == TE.OrderGroupType.MARKET_SL_TARGET or OrderGroupType == TE.OrderGroupType.MARKET:
                OrderID                         =   TradingLib.CreateOrder(self, Con, Symbol, Exchange.name, Qty, 0,0, TE.OrderType.MARKET.name, OrderDirection.name, TradeType.name) 
                #OrderID       =   TradingLib.CreateOrder(self, Con, Symbol, Exchange.name, Qty, 0,0, 'MARKET', 'BUY', 'MIS')
                DL["OrderID"]                   =   OrderID
                OrderPrice                      =   Con.get_executed_price(orderid=DL["OrderID"])
                DL["OrderPrice"]                =   OrderPrice
                Expenses                        =   TradingLib.FLib.Expenses(Qty, DL["OrderPrice"]) / Qty

                if OrderGroupType == TE.OrderGroupType.MARKET_SL_TARGET:
                    if SLPrice == 0:
                        if OrderDirection == TE.OrderDirection.BUY:
                            SLPrice             =   OrderPrice - (OrderPrice*(SLPricePerc/100))
                            TargetPrice         =   OrderPrice + (Expenses + (OrderPrice*(TargetPricePerc/100)))
                        else:
                            SLPrice             =   OrderPrice + (OrderPrice*(SLPricePerc/100))
                            TargetPrice         =   OrderPrice - (Expenses + (OrderPrice*(TargetPricePerc/100)))

                        SLOrderID               =   TradingLib.CreateOrder(self, Con,Symbol, Exchange.name, Qty, 0, SLPrice, TE.OrderType.STOPMARKET.name, ReverseOrderDirection.name, TradeType.name)
                        TargetOrderID           =   TradingLib.CreateOrder(self, Con, Symbol, Exchange.name, Qty, TargetPrice, 0, TE.OrderType.LIMIT.name, ReverseOrderDirection.name, TradeType.name)
                
                DL["SLOrderID"]                 =   SLOrderID
                DL["OrderExpenses"]             =   round(Expenses,2)
                DL["TargetOrderID"]             =   TargetOrderID
                DL["OrderClosingType"]          =   ReverseOrderDirection.value
                DL["SLPrice"]                   =   round(SLPrice,2)
                DL["TargetPrice"]               =   round(TargetPrice,2)
                DL["OrderStartTime"]            =   curr_time
                DL["OrderInQty"]                =   Qty
                DL["OrderOutQty"]               =   0
                # if FreshOrder:
                #     DL["OrderInQty"]            =   Qty
                #     DL["OrderOutQty"]           =   0
                # else
                #     DL["OrderInQty"]            =   Qty
                #     DL["OrderOutQty"]           =   Qty
                DL["Strategy"]                  =   Strategy.value
                DL["Watchlist"]                 =   Watchlist.value
                DL["Exchange"]                  =   Exchange.value
                DL["TradeType"]                 =   TradeType.value
                DL["CallType"]                  =   CallType.value
                DL["Monitoring"]                =   True
                DL["SYMBOL"]                    =   Symbol
                DL["BULLISH"]                   =   Bullish
                DL["TOTALVALUE"]                =   TotalValue
                DL["BalanceQty"]                =   Qty
                DL["SLPricePerc"]               =   SLPricePerc
                DL["TargetPricePerc"]           =   TargetPricePerc
                DL["PrimaryCandleDuration"]     =   PrimaryCandleDuration
                DL["TotalValueBasis"]           =   TotalValueBasis
                DL["OrderDirection"]            =   OrderDirection.value
                DL["Comments"]                  =   "RSI1>RSI2, 40<RSI1<70: Buy"
                #TradingLib.__CreateOrderInDB(DL)
                DBO = DBOps()
                DBO.CreateOrderInDB(DL)
                
        
        #Update order    
        else: 
            if OrderGroupType == TE.OrderGroupType.MARKET:
                OrderID       =   TradingLib.CreateOrder(self, Con, Symbol, Exchange.name, Qty, 0,0, TE.OrderType.MARKET.name, OrderDirection.name, TradeType.name) 
                #OrderID       =   TradingLib.CreateOrder(self, Con, Symbol, Exchange.name, Qty, 0,0, 'MARKET', 'BUY', 'MIS')
                DL["OrderID"]  = OrderID
                OrderPrice          =   Con.get_executed_price(orderid=OrderID)
                DL["OrderPrice"]    =   OrderPrice
                #Expenses            =   TradingLib.FLib.Expenses(Qty, DL["OrderPrice"]) / Qty
                

        return DL
            
    def __CreateOrderInDB(DL):
        # if FreshOrder:
        #     OrderQtyString  =   "OrderInQty"
        #     OrderQty        =   DL["OrderInQty"]
        # else:
        #     OrderQtyString  =   "OrderOutQty"
        #     OrderQty        =   DL["OrderOutQty"]
        
        Query = 'INSERT INTO Orders (Date, Strategy, Watchlist, OrderID,  OrderPrice, SYMBOL, BULLISH,TOTALVALUE,' \
                       'OrderInQty,  SLPrice, SLOrderID, TargetPrice, TargetOrderID,   OrderExpenses,' \
                       'OrderClosingType,' \
                       'Exchange, BalanceQty, TradeType, CallType, OrderStartTime, ' \
                       'Monitoring, SLPricePerc, SLTargetPerc, TradeStatus, PrimaryCandleDuration, TotalValueBasis)' \
                        'VALUES ' \
                       '('+ '"' + str(TradingLib.today) + '"' + ', :Strategy, :Watchlist, :OrderID, :OrderPrice,  :SYMBOL, :BULLISH, :TOTALVALUE,' \
                       ':OrderInQty, :SLPrice,  :SLOrderID, :TargetPrice, :TargetOrderID, :OrderExpenses,' \
                       ':OrderClosingType,' \
                       ':Exchange, :BalanceQty, :TradeType, :CallType, :OrderStartTime,' \
                       ' :Monitoring, :SLPricePerc, :TargetPricePerc, 1, :PrimaryCandleDuration, :TotalValueBasis)'

        DBOps.UpdateWithDL(Query, DL)

        # DBConn = LibDBOps.GetDBConn()
        # cursor = DBConn.cursor()
        # cursor.execute(Query, DL)

        # # Commit and close
        # DBConn.commit()
        # DBConn.close()

        
        #TradingLib.UpdateInOrderIndicators()
    
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
            DBO = DBOps()
            DBO.UpdateWithDL(sql_insert1M, DL1M)
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
            DBO = DBOps()
            DBO.UpdateWithDL(sql_insert3M, DL3M)
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
            DBO = DBOps()
            DBO.UpdateWithDL(sql_insert5M, DL5M)

    def UpdateOutOrderMomentumIndicators(OrderID, ExchangeName, DBO):
        #Get symbol from Orders table
        Query = "select symbol from Orders where OrderID=?"
        Params = (OrderID,)
        #Symbol = DBBase.ScalarQuery(Query, Params)
        #DBO = DBOps()
        Symbol = DBO.ScalarQuery(Query, Params)
        #Get tsl connection
        DH              = Dhan()
        Conn             =   DH.DhanConnection

        #Get Intraday data for the Symbol, Get Indicators 
        #DL1M = ALib.Get_Indicators(ALib, Conn.get_intraday_data(Symbol, "NSE", 1), Conn)
        #DL3M = ALib.Get_Indicators(ALib, Conn.get_intraday_data(Symbol, "NSE", 3), Conn)
        #DL5M = ALib.Get_Indicators(ALib, Conn.get_intraday_data(Symbol, "NSE", 5), Conn)
        ALib = AnaLysisLib()
        DL1M, DL3M, DL5M = ALib.Get_1_3_5M_Indicators(Conn, Symbol, ExchangeName)
        
        DL1M["OrderID"] = DL3M["OrderID"] = DL5M["OrderID"] = OrderID
        
        DBO.UpdateOutOrderMomentumIndicators(OrderID, DL1M, DL3M, DL5M)


        # #1M
        # sql_update1M = """
        # UPDATE OrderMomentumIndicators1M
        # SET
        #     RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
        #     SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
        #     MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        # WHERE
        #     OrderID=:OrderID
        # """
        # DBO = DBOps()
        # DBO.UpdateWithDL(sql_update1M, DL1M)

        # #3M
        # sql_update3M = """
        # UPDATE OrderMomentumIndicators3M
        # SET
        #     RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
        #     SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
        #     MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        # WHERE
        #     OrderID=:OrderID
        # """

        # DBO = DBOps()
        # DBO.UpdateWithDL(sql_update3M, DL3M)

        # sql_update5M = """
        # UPDATE OrderMomentumIndicators5M
        # SET
        #     RSID1OUT = :RSID1,RSID2OUT = :RSID2, SK1OUT = :SK1, SK2OUT = :SK2, SD1OUT = :SD1, SD2OUT = :SD2, SM501OUT = :SM501,
        #     SM502OUT = :SM502, SM211OUT = :SM211, SM212OUT = :SM212, MACD1OUT = :MACD1, MACD2OUT = :MACD2, MACDSIGNAL1OUT = :MACDSIGNAL1,
        #     MACDSIGNAL2OUT = :MACDSIGNAL2, MACDFAST1OUT = :MACDFAST1, MACDFAST2OUT = :MACDFAST2, VOL1OUT = :VOL1, VOL2OUT = :VOL2
        # WHERE
        #     OrderID=:OrderID
        # """

        # DBO = DBOps()
        # DBO.UpdateWithDL(sql_update5M, DL5M)
        
    
    def UpdateOrder(self, DL, ExchangeName):
        
        Query = 'update Orders set OrderExpenses=:OrderExpenses, FinalExecutedPrice=:FinalExecutedPrice, PLStatus=:PLStatus,' \
        'TradeStatus=:TradeStatus, TradeClosingSource=:TradeClosingSourceName, OrderOutQty=:OrderOutQty, BalanceQty=:BalanceQty, OrderEndTime=:OrderEndTime,' \
        'TimeTaken=:TimeTaken, TradeStatusOnPnL =:TradeStatusOnPnL where OrderID=:OrderID'

        DBO = DBOps()
        DBO.UpdateOrder(DL)
        #DBO.UpdateWithDL(Query, DL)
        TradingLib.UpdateOutOrderMomentumIndicators(DL["OrderID"], ExchangeName, DBO)
        #DBO.UpdateOutOrderMomentumIndicators(DL["OrderID"])


    def GetActiveOrders(self, StrategyData=False, Strategy=TE.Strategy.All):
        #Query
        if Strategy==TE.Strategy.All:
            Query = "Select * from Orders where Date = ? and TradeStatus=? order by Strategy"
            StrategyQuery = "select StrategyID,StrategyName, count(OrderID) as count,st.TradeMonitorScript, st.LeadMonitorScript  from Orders od join Strategies st on od.Strategy=st.StrategyID where Date = ? and TradeStatus=? group by Strategy order by count"
            #TradingLib.today = TradingLib.today + dt.timedelta(days=1)
            Params = (str(TradingLib.today),TE.TradeStatus.Active.value,)
            #Strategy_Params = (str(TradingLib.today),2,)
        else:
            Query = "Select * from Orders where Date = ? and TradeStatus=? and Strategy=?"
            params = (str(TradingLib.today),TE.TradeStatus.Active.value, Strategy.value,)

        #DBConn = LibDBOps.GetDBConn()
        #close connection
        
        DBO = DBOps()
        # Use pandas to execute the query and load results into a DataFrame
        if StrategyData:
            #DF = pd.read_sql_query(Query, DBConn, params=Params)
            #GDF = pd.read_sql_query(StrategyQuery, DBConn, params=Params)
            
            
            DF = DBO.DFReadSQLQuery(Query, Params)
            GDF = DBO.DFReadSQLQuery(StrategyQuery, Params)
            #DBConn.close()
            return DF, GDF
        else:
            #DF = pd.read_sql_query(Query, DBConn, params=Params)
            DF = DBO.DFReadSQLQuery(Query, Params)
            #DBConn.close()
            return DF

        #return data frame
        #return DF, GDF

    def UpdateDBRecord(self, DLWatchlist):
        #Current time
        curr_time = datetime.now().strftime(Const.Time_Format) 

        #PnL
        if DLWatchlist["TradeClosingSource"] == TE.TradeClosingSource.ManuallyClosed:
            PnL = TradingLib.FLib.PnLWithExpenses(DLWatchlist['OrderInQty'], DLWatchlist["BalanceQty"], DLWatchlist['OrderPrice'], DLWatchlist['OrderPrice']) #Source order was a buy order
        else:
            if(TE.OrderDirection(DLWatchlist['OrderClosingType']) == TE.OrderDirection.SELL):
                PnL =  TradingLib.FLib.PnLWithExpenses(DLWatchlist['OrderInQty'], DLWatchlist["BalanceQty"], DLWatchlist['OrderPrice'], DLWatchlist["FinalExecutedPrice"])
            else: #bought at closing
                PnL =  TradingLib.FLib.PnLWithExpenses(DLWatchlist["BalanceQty"], DLWatchlist['OrderInQty'],  DLWatchlist["FinalExecutedPrice"], DLWatchlist['OrderPrice'])

        DLWatchlist['PLStatus'] = round(PnL,2)

        if PnL >= 0:
            DLWatchlist["TradeStatusOnPnL"] = TE.TradeStatusOnPnL.Success.name
        else:
            DLWatchlist["TradeStatusOnPnL"] = TE.TradeStatusOnPnL.Failure.name


        #Update closing columns
        # DLWatchlist["TradeStatus"] = TE.TradeStatus.Completed.value
        # DLWatchlist["OrderOutQty"] = DLWatchlist["BalanceQty"]
        # DLWatchlist["BalanceQty"] = 0
        # DLWatchlist["CallType"] = TE.CallType.NA.value
        # DLWatchlist["OrderEndTime"] = curr_time
        # DLWatchlist["TimeTaken"] =  GL.GetTimeDiff(DLWatchlist["OrderStartTime"],curr_time)
        # DLWatchlist["TradeClosingSourceName"] = TE.TradeClosingSource(DLWatchlist["TradeClosingSource"]).name
        DL = {}
        DL["OrderExpenses"]               =   DLWatchlist["OrderExpenses"]
        DL["FinalExecutedPrice"]          =   DLWatchlist["FinalExecutedPrice"]
        DL["PLStatus"]                    =   DLWatchlist["PLStatus"]
        DL["TradeStatus"]                 =   TE.TradeStatus.Completed.value
        DL["TradeClosingSourceName"]      =   TE.TradeClosingSource(DLWatchlist["TradeClosingSource"]).name
        DL["OrderOutQty"]                 =   int(DLWatchlist["BalanceQty"])
        DL["BalanceQty"]                  =   0
        DL["OrderEndTime"]                =   curr_time
        DL["TimeTaken"]                   =   GL.GetTimeDiff(DLWatchlist["OrderStartTime"],curr_time)
        DL["TradeStatusOnPnL"]            =   DLWatchlist["TradeStatusOnPnL"]
        DL["OrderID"]                     =   str(DLWatchlist["OrderID"])
        #Update DB Record    
        TradingLib.UpdateOrder(self, DL,  TE.Exchange(DLWatchlist["Exchange"]).name)
    
    def GetTodayPnL():
        DBO = DBOps()
        # RealisedPnLQuery        =   "select sum(PLStatus) as RealisedPnL from Orders where Date=? and PLStatus is not NULL"
        # UnrealisedExpQuery      =   "select sum(OrderExpenses) as Exp from Orders where Date=? and PLStatus is NULL"
        # UnrealisedSLQuery       =   "select sum((SLPricePerc/100)*Orderprice*BalanceQty) as UnrealisedPnL from Orders where Date=? and PLStatus is NULL"
        # Param                   =   (str(TradingLib.today),) 
        # RealisedPnL             =   DBO.ScalarQuery(RealisedPnLQuery, Param)
        # UnrealisedExp           =   DBO.ScalarQuery(UnrealisedExpQuery, Param)
        # UnrealisedSL            =   DBO.ScalarQuery(UnrealisedSLQuery, Param)
 
        RealisedPnL, UnrealisedExp, UnrealisedSL = DBO.GetTodayPnL()

        if RealisedPnL is None: RealisedPnL = 0
        if UnrealisedExp is None: UnrealisedExp = 0
        if UnrealisedSL is None: UnrealisedSL = 0
        TodayPnL                =   round((RealisedPnL + -UnrealisedExp + -UnrealisedSL),2)

        return TodayPnL, RealisedPnL 

    def GetPositions(self, Conn):
        positions = Conn.get_positions()
        return positions

    def GetOrders(self, Conn):
        orderbook = Conn.get_orderbook()
        return orderbook

    def GetTrades(self, Conn):
        tradebook = Conn.get_trade_book()
        return tradebook

    def GetHoldings(self, Conn):
        holdings = Conn.get_holdings()
        return holdings

    def GetTodayTradeCount(self, Conn):
        tradebook = Conn.get_trade_book()

    def GetOpenPositionCount(self, Conn):
        positions = self.GetPositions(Conn)
        Total = 0
        Short = 0
        Long = 0
        if not positions.empty:
            for index, DFRow in positions.iterrows():
                if DFRow['positionType'] == 'SHORT': #Sold
                    Short = Short + 1
                elif DFRow['positionType'] == 'LONG': #Sold
                    Long = Long + 1
        
        Total = Short + Long
        return Total, Short, Long
    
    def GetOpenOrdersCount(self, Conn):
        orderbook = self.GetOrders(Conn)
        Total = 0
        Buy = 0
        Sell = 0

        if not orderbook.empty:
            for index, DFRow in orderbook.iterrows():
                if DFRow['orderStatus'] == 'PENDING': #Sold
                    if DFRow['transactionType'] == 'BUY': #Sold
                        Buy = Buy + 1
                    elif DFRow['positionType'] == 'SELL': #Sold
                        Sell = Sell + 1

        Total = Buy + Sell
        return Total, Buy, Sell
    
    def GetStrategyDetails(self, Strategy = TE.Strategy.All):
        #DBConn = LibDBOps.GetDBConn()      
          
        DBO = DBOps()

        return DBO.GetStrategyDetails(Strategy)
    
        # if Strategy == TE.Strategy.All:
        #     Query = "select * from Strategies"
        #     #DF = pd.read_sql_query(Query, DBConn)
        #     DF = DBO.DFReadSQLQuery(Query)
        #     #DBConn.close()
        #     return DF
        # else:
        #     Query = "select * from Strategies where StrategyID = ? "
        #     Params = (str(Strategy.value),) 
        #     #DF = pd.read_sql_query(Query, DBConn, params=Params)
        #     DF = DBO.DFReadSQLQuery(Query, Params)
        #     #DBConn.close()
        #     return DF.iloc[0].to_dict()
        #close connection
        

    def GetStrategyScriptNames(self, Strategy):
        DL = {}
        RDL = TradingLib.GetStrategyDetails(self, Strategy)   
        DL["StrategyScript"] = RDL["StrategyScript"]
        DL["TradeMonitorScript"] = RDL["TradeMonitorScript"]
        DL["LeadMonitorScript"] = RDL["LeadMonitorScript"]

        return DL

    def GetStrategyScriptName(self, Strategy):
        RDL = TradingLib.GetStrategyDetails(self, Strategy)
        return RDL["StrategyScript"]

    def GetStrategyLeadScriptName(self, Strategy):
        RDL = TradingLib.GetStrategyDetails(self, Strategy)
        return RDL["LeadMonitorScript"]

    def GetStrategyMonitorScriptName(self, Strategy):
        RDL = TradingLib.GetStrategyDetails(self, Strategy)
        return RDL["TradeMonitorScript"]

    
    def TradingStatus(TradeType):
        DBO = DBOps()
        PnL, RealisedPnL            =       TradingLib.GetTodayPnL()
        #TradeCount                  =       15
        
        SelectQueryKillSwitch = "Select KillSwitchIsOn from KillSwitch where Date=?"
        UpdateQueryKillSwitch = "Update KillSwitch Set KillSwitchIsOn=1 where Date=?"

        #Params                = (str(TradingLib.today),)
        #KillSwitch            = DBO.ScalarQuery(SelectQueryKillSwitch, Params)
        KillSwitch            = DBO.GetKillSwitch()
        KillSwitch            = not ((KillSwitch is None) or KillSwitch == 0)
        Status               = TE.TradingStatus.Allowed

        
        if KillSwitch:
            Status = TE.TradingStatus.NotAllowed
        elif  (
            (RealisedPnL < 0 and RealisedPnL < Const.Max_Loss_Per_Day)
        or  (RealisedPnL > 0 and RealisedPnL > Const.Max_Profit_Per_Day)
        
        ):
            #DBO.ScalarQuery(UpdateQueryKillSwitch, Params)
            DBO.SetKillSwitch()
            Status               = TE.TradingStatus.NotAllowed

        elif (
            (PnL < 0 and PnL < Const.Max_Loss_Per_Day)
        or  (PnL > 0 and PnL > Const.Max_Profit_Per_Day)
        ):
            
            Status = TE.TradingStatus.OnHold
        elif TradeType != TE.TradeType.COMMODITY and curr_time >= Const.Stock_Trading_End_Time:
            Status = TE.TradingStatus.OnHold
        elif TradeType == TE.TradeType.COMMODITY and curr_time >= Const.Stock_Trading_End_Time:
            Const.KillSwitchIsOn = True
            #DBO.ScalarQuery(UpdateQueryKillSwitch, Params)
            DBO.SetKillSwitch()
            Status = TE.TradingStatus.NotAllowed

        return Status

    #verify whether stock is already in open state
    def IsStockActive(self, Symbol):
        DBO = DBOps() 

        return DBO.IsStockActive(Symbol)

        # Query = "select count(OrderID) as Count from Orders where Date=? and Symbol=? and TradeClosingSource is NULL"
        
        # Params                = (str(TradingLib.today), Symbol,)
        # return (DBO.ScalarQuery(Query, Params) > 0)
    
    #Calculate the available qty as per the available funds
    def CalculateQtyToOrder(self, Conn, Symbol, MaxQty):
         # Get available money   
        FundsAvailable = Conn.get_balance()
        LTP = Conn.get_ltp_data(names = Symbol)[Symbol]
        # Get Margin money
        Leverage = Conn.margin_calculator(Symbol,TE.Exchange.NSE.name, TE.OrderDirection.BUY.name, 1, TE.TradeType.MIS.name, LTP, 0)['leverage'][:1]
        MarginMoney = LTP/float(Leverage)
        
        # Calculate Qty
        Qty = round(FundsAvailable/((MarginMoney*1.1)*3))
        if Qty > MaxQty:
            Qty = MaxQty

        return Qty

    def GetOrdersCountFromDB(self, Strategy=None, Status=TE.TradeStatus.Active):
        DBO = DBOps()

        return DBO.GetOrdersCountFromDB(Strategy, Status)
    
    def GapBetweenTwoTrades(self, Symbol):
        DBO = DBOps()

        ClosingTime = DBO.GetSymbolLastTradeClosingTime(Symbol)
        if ClosingTime is not None:
            curr_time = datetime.now().strftime(Const.Time_Format)
            # Convert to datetime object
            time_obj = datetime.strptime(ClosingTime, '%H:%M:%S')

            # Add seconds (e.g., 20 seconds)
            new_time_obj = time_obj + timedelta(seconds=Const.GapOfTwoTradesForASymbol)
             # Convert back to string
            new_time_str = new_time_obj.strftime('%H:%M:%S')

            if curr_time>new_time_str:
                return True
            else:
                return False
        else:
            return True
            
    

        # if Status==TE.TradeStatus.Active:
        #     StatusQuery = " and TradeClosingSource is NULL "
        # elif  Status==TE.TradeStatus.Completed: 
        #     StatusQuery = " and TradeClosingSource is not NULL "
        # else:
        #     StatusQuery = ""

        # if Strategy is None:
        #     Query   = "select count(OrderID) as Count from Orders where Date=? " + StatusQuery
        #     Params  = (str(TradingLib.today),)
        # else:
        #     Query = "select count(OrderID) as Count from Orders where Date=? and Strategy=? " + StatusQuery
        #     Params  = (str(TradingLib.today), Strategy,)

        # return DBO.ScalarQuery(Query, Params)
        
    
    #def SellOrder_Market_SL_Target(Con, Symbol, Exchange, OrderGroupType, Qty, SLPrice, TargetPrice, TradeType):
    #global str_Order_ID, str_SL_Order_ID, str_Target_Order_ID, str_Closing_Type, flt_LST
        # DL = {}

        # if OrderGroupType == TE.OrderGroupType.MARKET_SL_TARGET:
        #     DL["OrderID"]          =    TradingLib.CreateOrder(Con, Symbol, Exchange.name, Qty, 0,0, TE.OrderType.MARKET.name, TE.OrderDirection.SELL.name, TradeType.name) 
        #     DL["OrderPrice"]       =    Con.get_executed_price(orderid=DL["OrderID"])
        #     DL["SLOrderID"]        =    TradingLib.CreateOrder(Con, Symbol, Exchange.name, Qty, 0, SLPrice, TE.OrderType.STOPMARKET.name, TE.OrderDirection.BUY.name, TradeType.name)
        #     DL["Expenses"]         =   TradingLib.FLib.Expenses(Qty, DL["OrderPrice"]) / Qty
        #     DL["TargetOrderID"]    =    TradingLib.CreateOrder(Con, Symbol, Exchange.name, Qty, TargetPrice, 0, TE.OrderType.LIMIT.name, TE.OrderDirection.BUY.name, TradeType.name)
        #     DL["OrderClosingType"]       =   TE.OrderDirection.BUY
        #     return DL