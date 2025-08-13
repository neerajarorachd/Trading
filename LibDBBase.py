from Dhan_Tradehull import Tradehull
import sqlite3
import pandas as pd

def GetDBConn():
    conn = sqlite3.connect("Trading.db")
    return conn

# str_Client_Code =   "1106451789"
# str_Token_ID    =   "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5ODc5NDczLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.04Hzj4_Fr1jS2kuXwkWtOxRt4HWL5pNtw-oR-zO_g2Z18nCqS_mEIusYKLh53Zm4nBwKsbwpsAbWhC8NSjQpdQ"

class DBBase:
    """ def __new__(cls):
        tsl     =   Tradehull(str_Client_Code,str_Token_ID)
        return tsl """
    def __init__(self):
        self._Connection = sqlite3.connect("Trading.db")

    @property
    def DBConnection(self):
        return self._Connection

    def UpdateWithDL(self, Query, DL):
        DBConn = GetDBConn()
        cursor = DBConn.cursor()
        cursor.execute(Query, DL)

        # Commit and close
        DBConn.commit()
        DBConn.close()

    def DFReadSQLQuery(self, Query, Params=None):
        DBConn = GetDBConn()

        if Params is None:
            DF = pd.read_sql_query(Query, DBConn)
        else:
            DF = pd.read_sql_query(Query, DBConn, params=Params)
        return DF

    def ExecuteQuery(self, Query, Params=None):
        DBConn = GetDBConn()
        cursor = DBConn.cursor()

        if Params is None:
            result = cursor.execute(Query)
        else:
            result = cursor.execute(Query, Params)

        cursor.close()
        DBConn.close()

        return result
         

    def ExecuteUpdateQuery(self, Query, Params=None):
        DBConn = GetDBConn()
        cursor = DBConn.cursor()

        if Params is None:
            cursor.execute(Query)
        else:
            cursor.execute(Query, Params)

        DBConn.commit()
        cursor.close()
        DBConn.close()
    
    def ScalarQuery(self, Query, Params=None):
        DBConn = GetDBConn()
        cursor = DBConn.cursor()

        if Params is not None:
            #return pd.read_sql_query(Query, DBConn)         
            val = cursor.execute(Query, Params)
           
        else:
            #return pd.read_sql_query(Query, DBConn, params=Params)
            val = cursor.execute(Query)
            

        val = cursor.fetchone()
        if val is None:
            val = None
        else:
            val = val[0]

        cursor.close()
        DBConn.close()

        return val
    
    def OneColumnListQuery(self, Query, Params=None):
        DBConn = GetDBConn()
        cursor = DBConn.cursor()
        
        if Params is not None:
            #return pd.read_sql_query(Query, DBConn)         
            cursor.execute(Query, Params)   
        else:
            cursor.execute(Query)
                
        results = cursor.fetchall()
        # Optionally, flatten the result if it's a single column
        names = [row[0] for row in results]
    
        # Close the connection
        DBConn.close()
        return names
    
    def InsertFromDF(self, Table, DF):
        DBConn = GetDBConn()

        # Save DataFrame to table
        DF.to_sql(Table, DBConn, if_exists="append", index=False)

        # Optional: close connection
        DBConn.close()


        