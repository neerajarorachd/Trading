from ClassStrategyBase import Strategy
from LibEnum import TradingEnums as TE

class Strategy921(Strategy):
    def __init__(self):
        super().__init__(TE.Strategy.Morning921)

    def Enter(self, Watchlist_Morning_Refined):
        #global int_Entry_Flag, Watchlist_Refined, Historical_Data_Loaded, Watchlist_Morning
        return super().Enter_TimeBound(Watchlist_Morning_Refined)

    def Exit(self, Watchlist, Conn):
        super().Exit(Watchlist, Conn)

class Strategy930To1130(Strategy):
    def __init__(self):
        super().__init__(TE.Strategy.Morning_930_1130)

    def Enter(self, Watchlist_Morning_Refined):
        #global int_Entry_Flag, Watchlist_Refined, Historical_Data_Loaded, Watchlist_Morning
        return super().Enter_TimeBound(Watchlist_Morning_Refined)

    def Exit(self, Watchlist, Conn):
        super().Exit(Watchlist, Conn)

class Strategy930To1130Rev(Strategy):
    def __init__(self):
        super().__init__(TE.Strategy.Morning_930_1130_Rev)

    def Enter(self, Watchlist_Morning_Refined):
        #global int_Entry_Flag, Watchlist_Refined, Historical_Data_Loaded, Watchlist_Morning
        return super().Enter_Indicator_Call(Watchlist_Morning_Refined)

    def Exit(self, Watchlist, Conn):
        super().Exit(Watchlist, Conn)
