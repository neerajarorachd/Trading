from enum import Enum

class TradingEnums:
    class Direction(Enum):
        SIDEWAY = 0
        UP = 1 
        DOWN = -1

    class WideNarrow(Enum):
        UltraWide = 0
        Wide = 1
        Narrow = 2
        UltraNarrow = 3

    class Watchlist_Type(Enum):
        P50TO250 = 0
        SENSEX = 1
        NIFTY = 2
        BANKNIFTY = 3
        NIFTYIT = 4
        MIDCPNIFTY = 5
        NIFTYMIDCAP100 = 6
        NIFTYSMALLCAP50 = 7
        NIFTYSMALLCAP100 = 8
        NIFTYREALTY = 9
        NIFTYPHARMA = 10
        NIFTYAUTO = 11
        NIFTYFMCG =12
        NIFTYPSUBANK = 13
        NIFTYHEALTHCARE = 14
        NIFTYCONSUMERDURABLES = 15
        NIFTYOILNGASES = 16
        NIFTYMIDSMALLHEALTHCARE = 17
        FINNIFTY = 18
        NIFTYMEDIA = 19
        NIFTYMETAL = 20
        NIFTYENERGY = 21
        INDEXES = 22
        BANKS = 24
        NONE = 99
        TODAY = 100

    class TradeClosingSource(Enum):
        NotPlaced = 0
        TargetHit = 1
        SLHit = 2
        TimeOut = 3
        ManuallyClosed = 4

    class TradeStatus(Enum):
        Pending = 0
        Active = 1
        Completed = 2
        Cancelled = 3
        InTransit = 4
        All = 5
        

    class TradeType(Enum):
        MIS = 0
        DELIVERY = 1
        OPTION = 2
        FUTURE = 3
        COMMODITY = 4
        SCALPING = 5

    class OrderStatus(Enum):
        TRANSIT = 0
        PENDING = 1
        TRADED = 2
        CANCELLED = 3
        REJECTED = 4
        
    class OrderType(Enum):
        MARKET = 0
        LIMIT = 1
        STOPLIMIT = 2
        STOPMARKET = 3

    class OrderDirection(Enum):
        BUY = 0
        SELL = 1
        NOTSET = 2
        PASS = 3
        LEAD = 4
        
    class Exchange(Enum):
        NSE = 0
        BSE = 1
        MCX = 2

    class OrderGroupType(Enum):
        MARKET_SL_TARGET = 0
        LIMIT_SL_TARGET = 1
        MARKET_SL = 2
        LIMIT_SL = 3
        MARKET = 4
        LIMIT = 5

    class Strategy(Enum):
        Morning921 = 0
        Morning915 = 1
        ReverseTrade = 2
        VWAP_BB = 3
        Morning_930_1130 = 5
        Morning_930_1130_Rev = 6
        All = 100

    class CallType(Enum):
        Call = 0
        Put = 1
        NA = 2

    class TradeStatusOnPnL(Enum):
        Jackpot = 0
        Success = 1
        AboveCost = 2
        BelowCost = 3
        Failure = 4
        Disaster = 5
        NONE = 6

    class StrategyDataType(Enum):
        FullRecord = 0
        AllScripts = 1
        Strategy = 2
        Monitor = 3
        Lead = 4

    class TradingStatus(Enum):
        Allowed = 0
        OnHold = 1
        NotAllowed = 2

    class LiveMode(Enum):
        Live = 0
        Dummy = 1
        BackTest = 2
    class BB_VWAP_LTP_Position(Enum):
        #VWAP_Above_BBU = 0 #Over priced
        Above_BBU = 1
        On_BBU = 2
        TH_75 = 3
        TH_50 = 4
        TH_25 = 5
        On_Center = 6
        BH_75 = 7
        BH_50 = 8
        BH_25 = 9
        On_BBB = 10
        Below_BBB = 11
        #VWAP_Below_BBB = 12 #BUnder priced
        Above_Center = 13
        Above_BBB = 14
        NotSet = 20