from LibAnalysis import AnaLysisLib
from LibDhan import Dhan
from LibEnum import TradingEnums as TE
from LibTrading import TradingLib

ALib = AnaLysisLib()
DH              = Dhan()
tsl             =   DH.DhanConnection



# Chart = tsl.get_intraday_data('HINDWAREAP', 'NSE', 3)

# DLChart = ALib.Get_Indicators(Chart, tsl)
# LTP = Chart.iloc[-1]["close"]
# #Call BBAnalysis function
# DLBB = ALib.Get_BB_Call(LTP,Chart,DLChart, TE.TradeType.SCALPING)
# print(DLBB["BBCall"])

# DLBB["INDICATORS"]["OrderID"]               =   2143544336
# DLBB["INDICATORS"]["TargetBB"]              =   "BBU"
# DLBB["INDICATORS"]["SLBB"]                  =   "BBM"
# DLBB["INDICATORS"]["SLBBLastPrice"]         =   217.80
# DLBB["INDICATORS"]["TargetBBLastPrice"]     =   219.10
# DLBB["INDICATORS"]["TargetLastPrice"]       =   219.00
# DLBB["INDICATORS"]["SLLastPrice"]           =   217.60
# DLBB["INDICATORS"]['VWAP1']                 =   217.40
# DLBB["INDICATORS"]['VWAP2']                 =   217.35


# #BBU
# DLBB["INDICATORS"]['BBU1']                  =   219.80
# DLBB["INDICATORS"]['BBU2']                  =   219.70
# #BBM
# DLBB["INDICATORS"]['BBM1']                  =   217.80
# DLBB["INDICATORS"]['BBM2']                  =   217.60
# #BBB
# DLBB["INDICATORS"]['BBB1']                  =   216.50
# DLBB["INDICATORS"]['BBB2']                  =   216.60


# ALib.StoreOrderBBData(DLBB["INDICATORS"])
# print("Insert done")
# DLRes = ALib.GetOrderBBData(DLBB["INDICATORS"]["OrderID"])
# print(DLRes)
# print("Update")
# DL={}
# DL["TargetBBLastPrice"] =   230.10
# DL["SLBBLastPrice"]     =   237.80
# DL["TargetLastPrice"]   =   239.10
# DL["SLLastPrice"]       =   237.60
# DL["OrderID"]           =   DLBB["INDICATORS"]["OrderID"]

# ALib.UpdateOrderBBData(DL)


#def order(self, Symbol, Qty, Watchlist, Bullish, TotalValue, OrderDirection, Conn, TargetPricePerc=None, SLPricePerc=None):
    #print("buy")
        #if TargetPricePerc is None:
            #TargetPricePerc = self._StrategyTargetPerc
        #if SLPricePerc is None:
            #SLPricePerc = self._StrategySLPerc

#TradingLib.Order(TradingLib, tsl, 5, Watchlist, 'ITC',  Bullish, TotalValue,  'NSE', TE.OrderGroupType.MARKET_SL_TARGET, Qty,TE.TradeType.MIS, TE.CallType.NA, OrderDirection, SLPricePerc, TargetPricePerc, 3, .2)
        #return DL

#print(str(3125061717961))
#Use order_type="LIMIT" for limit price, 
# DCBBANK
# Order Type: Market, SLMarket, Limit
# Purchase price: 141.73
# SL:             141.32
# Target:         142.32

# Need to modify SL: 141.52
modified_order = tsl.modify_order(order_id=3125061724291,order_type="STOPLIMIT",quantity=1,price=141.45, trigger_price=141.55)
print(modified_order)

