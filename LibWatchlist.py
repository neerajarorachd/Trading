#Historical Watchlist class
#Two candles Watchlist class
#GetWatchlist function
#Fetch Historical watchlist in DB
#return Historical Watchlist for the day from DB, call Fetch function if not fetched already
import pandas as pd
import sqlite3
import LibDBBase
from LibDBBase import DBBase
from LibAnalysis import AnaLysisLib
from LibEnum import TradingEnums as TE
from datetime import date
from datetime import datetime
from LibConstants import Const 
from LibDBBase import DBBase
from LibDBOps import DBOps

#import mysql.connector
#from sqlalchemy import create_engine
ALib = AnaLysisLib()
today       =   str(date.today())

class HistoricalWatchlist:
    today = str(date.today())

    def __init__(cls):
        pass

    # def __newdf__(cls, df):
    #     conn = sqlite3.connect("Trading.db")

        # Insert the DataFrame into a table named 'flags'
        #df.to_sql("HistoricalWatchlist", conn, if_exists="replace", index=False)

    def __new__(cls, DATE, SYMBOL, DIRECTION ,PRICEUP,FIRSTCANDLEPERC,SECONDCANDLEPERC,FIRSTCANDLEPRICEDIFF,RSIOVER50,SKDOVERSDD,SKD1OVERSKD2,SKDOVER70, VOLOVERSM50, BULLISHCROSS, SM21OVERSM50, BEARISHCROSS, RSIBELOW40, SKDBELOWSDD, SKDBELOW30, VOLBELOWM50, SM21BELOWSM50):
        DATE=DATE
        SYMBOL=SYMBOL
        DIRECTION =DIRECTION
        PRICEUP=PRICEUP
        FIRSTCANDLEPERC=FIRSTCANDLEPERC
        SECONDCANDLEPERC=SECONDCANDLEPERC
        FIRSTCANDLEPRICEDIFF=FIRSTCANDLEPRICEDIFF
        RSIOVER50=RSIOVER50
        SKDOVERSDD=SKDOVERSDD
        SKD1OVERSKD2=SKD1OVERSKD2
        SKDOVER70=SKDOVER70
        VOLOVERSM50=VOLOVERSM50
        BULLISHCROSS=BULLISHCROSS
        SM21OVERSM50=SM21OVERSM50
        BEARISHCROSS=BEARISHCROSS
        RSIBELOW40=RSIBELOW40
        SKDBELOWSDD=SKDBELOWSDD
        SKDBELOW30=SKDBELOW30
        VOLBELOWM50=VOLBELOWM50
        SM21BELOWSM50=SM21BELOWSM50

    def GetIndexMomentumData(Conn):
        return HistoricalWatchlist.GetHistoricalMomentumData(Conn, HistoricalWatchlist.today, "rpwid, *", TE.Watchlist_Type.INDEXES.value)

    def GetTodaysWatchlist(Conn):
        #if GetTodaysWatchlistFromDB == None
        
        df = HistoricalWatchlist.GetIndexMomentumData(Conn)

        if not df.empty:
            TodayWatchlist = df.iloc[0]["SYMBOL"]
        
            #get watchlist id from watchlist where WatchlistName=df.iloc[0]["SYMBOL"]
            #setTodaysWatchlistInDB
        
        #wdf = get Symbol from watcgliststocks where watchlisttype = WatchlistID
        #return wdf
            

    def GetHistoricalMomentumData(Conn, WatchlistDate = today, Columns = "rowid, *", WatchlistID=0):
        curr_time = datetime.now().strftime(Const.Time_Format) 
        DBO = DBOps()

        #Get Historical data from db
        #df = HistoricalWatchlist.__Get_Historical_Momentum_Data_From_DB(WatchlistDate, Columns, WatchlistID)
        df = DBO.Get_Historical_Momentum_Data_From_DB(WatchlistDate, Columns, WatchlistID)
        #call internal function to generate data
        if df.empty:

            df = HistoricalWatchlist.__SetHistoricalMomentumData(Conn, WatchlistID)
        else:
            print("\nHistorical data collected from DB at " + str(curr_time))
        if df is not None:
            if df["TOP"][0] == 0 and WatchlistID!=TE.Watchlist_Type.INDEXES.value:              
                today = datetime.today().strftime('%A')
                if not (today=='Saturday' or today=='Sunday'):
                    
                    if curr_time >= Const.Stock_Trading_Start_Time and curr_time <= Const.Stock_Trading_End_Time:
                        
                        HistoricalWatchlist.__SetTodayPrices(Conn, df)
                        df = HistoricalWatchlist.__Get_Historical_Momentum_Data_From_DB(WatchlistDate, Columns, WatchlistID)

        return df
        #store in db

    def __SetHistoricalMomentumData(Conn, WatchlistID):
        #DBConn = LibDBBase.GetDBConn()
        DBO = DBOps()

        List = HistoricalWatchlist.GetWatchlist(Conn, TE.Watchlist_Type(WatchlistID))


        df = ALib.Get_Momentum_Data(List, Conn, WatchlistID)

        if df is not None and (not df.empty):
            if WatchlistID==TE.Watchlist_Type.INDEXES.value:
                
                df.drop(columns=['WATCHLISTID'], errors='ignore', inplace=True)
                #df.to_sql("IndexMomentumData", DBConn, if_exists="append", index=False)
                DBO.SaveIndexMomentumData(df)
                

                #set today's trending index
                Symbol = df.iloc[0]["SYMBOL"]
                IndexWatchlistID = TE.Watchlist_Type[Symbol].value
                #HistoricalWatchlist.__SetTodayTradingStream(Symbol, IndexWatchlistID)
                DBO.SetTodayTradingStream(Symbol, IndexWatchlistID)
            else:
                #df.to_sql("HistoricalMomentumData", DBConn, if_exists="append", index=False)
                DBO.SaveHistoricalMomentumData(df)
        return df


    def __SetTodayPrices(Conn, df):
        #if day ! Saturday or Sunday
        #if current time is > 9:15 and < 3:30
        #df = HistoricalWatchlist.__Get_Historical_Momentum_Data_From_DB(Conn, str(date.today()), "SYMBOL, PDP")
        DBO = DBOps()

        Symbols = df["SYMBOL"].astype(str).tolist()
        
        all_ltp_data = ALib.Get_All_LTP_Data(Symbols, Conn)
        #all_ltp_data   = Conn.get_ltp_data(names = Symbols)
        #DBconn = LibDBBase.GetDBConn()
        #cursor = DBconn.cursor()

        for index, WatchlistRow in df.iterrows():
            TOP             =   all_ltp_data[WatchlistRow["SYMBOL"]]
            PDP             =   WatchlistRow["PDP"]
            TOPGreaterPDP   =   TOP > PDP

            #update records
            #query = "SELECT " + Columns + " from HistoricalMomentumData where Date='" + str(WatchlistDate) +"'"
            
            DBO.SetTodayPrices(TOP, TOPGreaterPDP, WatchlistRow["rowid"])
            # query = '''
            # UPDATE HistoricalMomentumData
            # SET TOP = ?, PRICEUP = ?
            # WHERE rowid = ?
            # '''
            # params = (TOP, TOPGreaterPDP, WatchlistRow["rowid"])

            # cursor.execute(query, params)

            # # Commit the changes
            # DBconn.commit()

            #if df = none then fetch the data

            # Close the connection
        #DBconn.close()    



        
    def __Get_Historical_Momentum_Data_From_DB(WatchlistDate, Columns = "rowid, *", WatchlistID = 0):
          # Query to fetch data
          # "SYMBOL, DIRECTION, BULLISH "
        if WatchlistID==TE.Watchlist_Type.INDEXES.value:
            query = "SELECT " + Columns + " from IndexMomentumData where Date='" + str(WatchlistDate) +"'"
        else:
            query = "SELECT " + Columns + " from HistoricalMomentumData where Date='" + str(WatchlistDate) +"' and WatchlistID=" + str(WatchlistID)

        DBconn = LibDBBase.GetDBConn()
        # Load data into a DataFrame
        df = pd.read_sql_query(query, DBconn)

        #if df = none then fetch the data

        # Close the connection
        DBconn.close()
        return df

    def Get_Watchlist_For_2_Sisters(WatchlistDate):
        # Query to fetch data
        Columns = "SYMBOL, DIRECTION, BULLISH"
        df = HistoricalWatchlist.__Get_Historical_Watchlist_From_DB(WatchlistDate, Columns)

        # query = "SELECT SYMBOL, DIRECTION, BULLISH from HistoricalWatchlist where Date=?", (WatchlistDate)
        # conn = LibConnection.GetDBConn()
        # # Load data into a DataFrame
        # df = pd.read_sql_query(query, conn)

        # #if df = none then fetch the data
        # # Close the connection
        # conn.close()
        # return df
    
    def GetWatchlist(Conn = None, ListType = TE.Watchlist_Type.TODAY):
        DBO = DBOps()
        
        #Get watchlist from db
        WatchlistID = ListType.value
        if ListType == TE.Watchlist_Type.TODAY:
            WatchlistID = HistoricalWatchlist.__GetTodayWatchlist(Conn)
            #if WatchlistID >= 0:
            ListType = TE.Watchlist_Type(WatchlistID)
        #return HistoricalWatchlist.__GetWatchlistFromDB(ListType)
        return DBO.GetWatchlistFromDB(ListType)
        

    def __SetTodayTradingStream(Symbol, WatchlistID):
        #call GetTodayTradingStream()
        #if not avalable then analyze
        #Analyse indexes and decide where to trade today
        #Symbol = None
        #WatchlistID = -1

        
        #update db record
        Query = "insert into todaywatchlist (WatchlistDate, IndexSymbol, WatchlistID) values (?,?,?)"
        Params = (str(HistoricalWatchlist.today), Symbol, WatchlistID)
        
        DBconn = LibDBBase.GetDBConn()
        cursor = DBconn.cursor()
        cursor.execute(Query, Params)

        DBconn.commit()
        
        return WatchlistID, Symbol



    def GetTodayTradingStream():
        #Get Today Stream from db
        #if not avalable then analyze
        #Analyse indexes and decide where to trade today
        Query = "select watchlistid, indexsymbol from todaywatchlist where WATCHLISTDATE = ?"
        Params = (str(HistoricalWatchlist.today),)
        #if not available call SetTodayTradingStream() columns Date, Stream
        #Fetch the symbols for today's stream
        #return df
        DBconn = LibDBBase.GetDBConn()
        cursor = DBconn.cursor()

        # Example: Get a scalar value (e.g., count of rows in a table)
        cursor.execute(Query, Params)
        result = cursor.fetchone()
        cursor.close()
        DBconn.close() 
        return result
    
    def __GetTodayWatchlist(Conn):
        #get watchlist for today
        DBO = DBOps()

        #result = HistoricalWatchlist.GetTodayTradingStream()
        result = DBO.GetTodayTradingStream()
        #return 50 to 250 watchlist if there is some issue with watchlist
        WatchlistID = TE.Watchlist_Type.P50TO250

        if result == None:
            #call Set Today's Trading Stream
            
            df = HistoricalWatchlist.GetHistoricalMomentumData(Conn, HistoricalWatchlist.today, "rowid, *", TE.Watchlist_Type.INDEXES.value)
            if df is not None:
                if not df.empty:
                    Symbol = df.iloc[0]["SYMBOL"]    
                    WatchlistID = TE.Watchlist_Type[Symbol]
        else:
            WatchlistID = result[0]
        
        return WatchlistID

     

        # result is a tuple like (42,), so get the scalar value with [0]
        #count = result[0]

        

        # Clean up
        
    
    def __GetWatchlistFromDB(ListType):
        query = "SELECT SYMBOL from WatchlistStocks where WATCHLISTTYPE="+ (str(ListType.value))
        DBconn = LibDBBase.GetDBConn()
        # Load data into a DataFrame
        #df = pd.read_sql_query(query, conn)
        # Fetch all results into a list (array)
        
        cursor = DBconn.cursor()

        # Execute your query
        cursor.execute(query)
        results = cursor.fetchall()

        # Optionally, flatten the result if it's a single column
        names = [row[0] for row in results]
        #if df = none then fetch the data

        # Close the connection
        DBconn.close()
        return names

    def SaveTest():
        conn = sqlite3.connect("Trading.db")

    def IsHistoricalDataLoaded(WatchlistID):
        DBO = DBOps()
        Query = "select count(Symbol) as Count from HistoricalMomentumData where Date=? and WatchlistID=?"
        
        Params                = (str(HistoricalWatchlist.today), WatchlistID,)
        return (DBO.ScalarQuery(Query, Params) > 0)
        # Insert the DataFrame into a table named 'flags'
        #df.to_sql("flags", conn, if_exists="replace", index=False)

    def GetTodaysWatchListID():  
        DBO = DBOps()

        return DBO.GetTodaysWatchListID()
    


    
        # Query = "select WatchlistID from TodayWatchlist where WatchlistDate=?"
        
        # Params                = (str(HistoricalWatchlist.today),)
        # return DBO.ScalarQuery(Query, Params)
    #Scenario 1
    #9:16 Call the empty constructor Watchlist()
    # Call df = GetHistoricalWatchlist()
    # LoadHistoricalWatchlist - Check db, if list available for the date, return from db
    # elif not available in db, call the HistoricalWatchlist function and store the list in db. return df.

    #Scenario 2
    #9:21 Get the 
    # If not available then run the watchlist function and fetch the function

        