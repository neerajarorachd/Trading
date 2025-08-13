import talib
import LibEnum
import pandas as pd
import time
from LibEnum import TradingEnums as TE
from LibConstants import Const
from datetime import date
from datetime import datetime, timedelta
from LibDBOps import DBOps
from LibDBBase import DBBase
import numpy as np

# Get 921 Direction
# Get Sensex Direction
# Get Nifty Direction
# Get First Candle Direction
# Pre-market Direction

class AnaLysisLib:
    def GetRSI(self, chart):
        chart['rsi'] = talib.RSI(chart['close'], timeperiod=14)
        RSI = chart.iloc[-1]['rsi']
        return RSI

    def GetRSI_5C_Direction(self, chart):
        df = pd.DataFrame
        df = chart['rsi'] = talib.RSI(chart['close'], timeperiod=14)
        R1 = chart.iloc[-1]['rsi']
        R2 = chart.iloc[-2]['rsi']
        R3 = chart.iloc[-3]['rsi']
        R4 = chart.iloc[-4]['rsi']
        R5 = chart.iloc[-5]['rsi']

        #print(talib.MOM(chart['rsi'].to_numpy(), timeperiod=5))

        if R1>R5 and R1>60 and R1>R2:
            return LibEnum.Direction.UP
        else:
            return LibEnum.Direction.DOWN
        
        
        
        
     

    def GetStochastics_5C_Direction(self, chart):
        #https://stackoverflow.com/questions/72046727/how-can-i-get-last-value-of-stochrsi-with-ta-lib
        #output = talib.MOM(close, timeperiod=5) #Get the momentum
        #narr = chart['high'].to_numpy(),  chart['low'].to_numpy(), chart['open'].to_numpy()
        slowk, slowd = talib.STOCH(chart['high'].to_numpy(), chart['low'].to_numpy(),chart['close'].to_numpy(), 5, 3, 0, 3, 0)
        #%k blue, %d red
        print(str(slowd[-1]) + "-" + str(slowk[-1]))
        print(str(slowd[-2]) + "-" + str(slowk[-2]))
        print(str(slowd[-3]) + "-" + str(slowk[-3]))
        print(str(slowd[-4]) + "-" + str(slowk[-4]))
        print(str(slowd[-5]) + "-" + str(slowk[-5]))

        if(slowk[-1]>slowd[-1] and slowk[-2]<slowd[-2]):
            print("Bullish Crossover")
        elif (slowk[-1]<slowd[-1] and slowk[-2]>slowd[-2]):
            print("Bearish Crossover")
        if (slowk[-2]>slowd[-2] and slowk[-3]>slowd[-3]):
            print("Running over")
        #chart['stoch'] = talib.STOCHRSI(chart['close'], timeperiod=14)
        print(talib.STOCHRSI(chart['close'], timeperiod=14))
        

    def Pre_Market_Watchlist(self, List, tsl):
        #pre_market_watchlist = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC', 'BPCL', 'WIPRO', 'SHRIRAMFIN', 'ADANIPORTS', 'JSWSTEEL', 'COALINDIA', 'ULTRACEMCO', 'BAJAJ-AUTO', 'LT', 'POWERGRID', 'ADANIENT', 'SBIN', 'HCLTECH', 'TCS', 'EICHERMOT', 'BAJAJFINSV', 'TECHM', 'LTIM', 'HINDUNILVR', 'BHARTIARTL', 'AXISBANK', 'GRASIM', 'HEROMOTOCO', 'DRREDDY', 'ICICIBANK', 'HDFCBANK', 'BAJFINANCE', 'SBILIFE', 'RELIANCE', 'KOTAKBANK', 'ITC', 'TITAN', 'SUNPHARMA', 'INDUSINDBK', 'APOLLOHOSP', 'BRITANNIA', 'NESTLEIND', 'HDFCLIFE', 'DIVISLAB', 'CIPLA', 'ASIANPAINT', 'TATACONSUM']


        body_dict = {}
        tarde_info = {}




        for name in List:
            time.sleep(1)
            print(f"Pre market scanning {name}")
            daily_data = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")
            ldc = daily_data.iloc[-1]  #last_day_candle
            body_percentage = ((ldc['close'] - ldc['open'])/ldc['open'])*100

            body_dict[name] = round(body_percentage, 2)



        script_having_max_body = max(body_dict, key=body_dict.get)
        daily_data = tsl.get_historical_data(tradingsymbol = script_having_max_body, exchange = 'NSE',timeframe="DAY")
        ldc = daily_data.iloc[-1]  #last_day_candle
        tarde_info = {"Direction":"buy", "level":ldc['high']}


        print(script_having_max_body)
        print(tarde_info)

    def Get_Momentum_Data(self, List, tsl, WatchlistID=0):    
        watchlist_921 = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC', 'BPCL', 'WIPRO', 'SHRIRAMFIN', 'ADANIPORTS', 'JSWSTEEL', 'COALINDIA', 'ULTRACEMCO', 'BAJAJ-AUTO', 'LT', 'POWERGRID', 'ADANIENT', 'SBIN', 'HCLTECH', 'TCS', 'EICHERMOT', 'BAJAJFINSV', 'TECHM', 'LTIM', 'HINDUNILVR', 'BHARTIARTL', 'AXISBANK', 'GRASIM', 'HEROMOTOCO', 'DRREDDY', 'ICICIBANK', 'HDFCBANK', 'BAJFINANCE', 'SBILIFE', 'RELIANCE', 'KOTAKBANK', 'ITC', 'TITAN', 'SUNPHARMA', 'INDUSINDBK', 'APOLLOHOSP', 'BRITANNIA', 'NESTLEIND', 'HDFCLIFE', 'DIVISLAB', 'CIPLA', 'ASIANPAINT', 'TATACONSUM']


        body_dict = {}
        tarde_info = {}
        bull_dict = {}
        Bear_dict = {}
        crossover_dict = {}
        #use dataframe instead of dict.
        #Name, Body_Percentage, RSI, Stoch, Volume, Open, high, low

        #Buy - Sensex is positive, Nifty50 is positive, Midcap is positive
        #sort by volume - desc
        #If Volume > SMA
        #IF RSI > 60
        #If Stoch > 70
        #If Stoch > signal
        #If Open > Prev day close
        #If LTP > Open

        #Sell - Else
        #sort by volume - desc
        #IF RSI < 40
        #If Stoch < 30
        #If Stoch < signal
        #If Open < Prev day close
        #If LTP < Open

        columns = ['DATE', 'SYMBOL', 'DIRECTION', 'PDP', 'TOP', 'PRICEUP', 'TOTALMOVEMENT','FIRSTCANDLEPERC','SECONDCANDLEPERC','FIRSTCANDLEPRICEDIFF','RSIOVER50','SKDOVERSDD','SKD1OVERSKD2','SKDOVER70', 'VOLOVERSM50', 'BULLISHCROSS', 'SM21OVERSM50', 'BEARISHCROSS', 'RSIBELOW40', 'SKDBELOWSDD', 'SKDBELOW30', 'VOLBELOWM50', 'SM21BELOWSM50', 'WATCHLISTID']
        rows = []

        #all_ltp_data   = tsl.get_ltp_data(names = ['NIFTY 17 APR 25400 CALL', 'NIFTY 17 APR 25400 PUT', "ACC", "CIPLA"])
        #all_ltp_data   = tsl.get_ltp_data(watchlist_921)

        curr_time       = datetime.now().strftime(Const.Time_Format) 
        TodaysPrice = (curr_time >= Const.Stock_Trading_Start_Time and curr_time <= Const.Stock_Trading_End_Time)

        print("Entered into Historical Data collection function: " + str(curr_time))
        #wait if another thread is running this function
        self.HDAvailable()

        for name in List:
            time.sleep(1)
            name = name.strip()

            print(f"Pre market scanning {name}")
            
            #Chart3 = tsl.get_intraday_data(name, 'NSE', 3)
            #Chart1 = tsl.get_intraday_data(name, 'NSE', 1)
            try:
                ChartD = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")

                #verify the none and empty

                if ChartD is None:
                    continue
                else:
                    if ChartD.empty:
                        continue
                #ChartD = List
                # Get Indicators
                DL              = self.Get_Indicators(ChartD, tsl)
                #RSI
                RSI1           = DL['RSID1'] #round(talib.RSI(ChartD['close']).iloc[-1],2)
                RSI2           = DL['RSID2'] #round(talib.RSI(ChartD['close']).iloc[-2],2)
                #RSI1           = round(talib.RSI(Chart1['close']).iloc[-1],2)
                #RSI3           = round(talib.RSI(chart1['close']).iloc[-1],2)

                #Stochastics
                #ChartD['sk'], ChartD['sd'] = talib.STOCH(ChartD['high'].to_numpy(), ChartD['low'].to_numpy(),ChartD['close'].to_numpy(), 5, 3, 0, 3, 0)
                SK1                = DL['SK1'] #ChartD['sk'].iloc[-1]
                SD1                = DL['SD1'] #ChartD['sd'].iloc[-1]
                SK2                = DL['SK2'] #ChartD['sk'].iloc[-2]
                SD2                = DL['SD2'] #ChartD['sd'].iloc[-2]
                PDSM50V          = DL['SM501'] #talib.SMA(ChartD['volume'].to_numpy(), 50)[-1] #Previous day SM50
                PDSM21V          = DL['SM211'] #talib.SMA(ChartD['volume'].to_numpy(), 21)[-1] #Previous day SM21
                #VWAP                = DL['VWAP']
                #SK1, SD1 = talib.STOCH(Chart1['high'].to_numpy(), Chart1['low'].to_numpy(),Chart1['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
                #SK3, SD3 = talib.STOCH(Chart3['high'].to_numpy(), Chart3['low'].to_numpy(),Chart3['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
                #SKD1, SDD1 = talib.STOCH(ChartD['high'].to_numpy(), ChartD['low'].to_numpy(),ChartD['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
                #SKD2, SDD2 = talib.STOCH(ChartD['high'].to_numpy(), ChartD['low'].to_numpy(),ChartD['close'].to_numpy(), 5, 3, 0, 3, 0)[-2]
                #check iloc of daily data and other charts. verify the location data i.e. [-1] [0]
                #verify all data 

                #Daily analysis
                #Price and Volume
                PDC_Price       = ChartD.iloc[-1]['close']  #Previous day close
                PDV             = ChartD.iloc[-1]['volume']  #Previous day volume
                
                PD_LastCD          = ChartD.iloc[-1]  #last_candle daily
                PD_body_perc1 = ((PD_LastCD['close'] - PD_LastCD['open'])/PD_LastCD['open'])*100
                PD_LastCD          = ChartD.iloc[-2]  #last_candle daily
                PD_body_perc2 = ((PD_LastCD['close'] - PD_LastCD['open'])/PD_LastCD['open'])*100
                price_change    =   0.0
                body_dict[name] = round(PD_body_perc1, 2)
                direction       =   "SIDEWAY"
                BullishCross    = (SK2<SD2 and SK1>SD1 and SK2<=30 and SK1>30) # or RSI crosses 60 and SKD crosses 70 then tere are chance of reversal
                BearishCross    = (SK2>SD2 and SK1<SD1 and SK2 > 70 and SK1 < 70)
                Add = False
                TotalMovement   =   round(abs(PD_body_perc1+PD_body_perc2),4)

                if TodaysPrice:
                    TO_Price            =   tsl.get_ltp_data(names = name)[name]     #Today open
                    price_change        =   (TO_Price-PDC_Price)/PDC_Price
                    TotalMovement       =   round(abs(TotalMovement + price_change),4)

                    if TO_Price > PDC_Price and RSI1 > 50 and SK1 >= 70 and PDV > PDSM50V:
                    #bullish
                        print("bullish")
                        direction = 'BULLISH'
                        bull_dict[name] = price_change
                        Add = True
                    elif TO_Price < PDC_Price and RSI1 < 40 and SK1 < SD1 and SK1 <= 30:
                        #bearish
                        print("bearish")
                        direction = 'BEARISH'
                        Bear_dict[name] = price_change
                        Add = True
                    elif TO_Price > PDC_Price and RSI1 > 50 and SK1 >= 60:
                        print("bullish trend")
                        direction = 'BULLISH TREND'
                        bull_dict[name] = price_change
                        Add = True
                    elif RSI1 < 40 and SK1 <= 40:
                        #bearish
                        print("bearish trend")
                        direction = 'BEARISH TREND'
                        Bear_dict[name] = price_change
                        Add = True
                    elif TO_Price > PDC_Price:
                        direction = 'PRICE UP'
                        print("PRICE UP")
                        Add = True
                    elif TO_Price <= PDC_Price:
                        direction = 'PRICE DOWN'
                        print("PRICE DOWN")
                        Add = True
                else:
                    if RSI1 > 50 and SK1 >= 70 and PDV > PDSM50V:
                        #bullish
                        print("bullish")
                        direction = 'BULLISH'
                        bull_dict[name] = price_change
                        Add = True
                    elif RSI1 < 40 and SK1 < SD1 and SK1 <= 30:
                        #bearish
                        print("bearish")
                        direction = 'BEARISH'
                        Bear_dict[name] = price_change
                        Add = True
                    elif RSI1 > 50 and SK1 >= 60:
                        print("bullish trend")
                        direction = 'BULLISH TREND'
                        bull_dict[name] = price_change
                        Add = True
                    elif RSI1 < 40 and SK1 <= 40:
                        #bearish
                        print("bearish trend")
                        direction = 'BEARISH TREND'
                        Bear_dict[name] = price_change
                        Add = True
                    
                #3M analysis
                
                

                #daily_thi = daily_data.iloc[0]['high']s
                #now_sma = talib.SMA(Chart1['volume'].to_numpy())
                #now_vol = Chart1[-1]['volume']
                #now_ltp = Chart1[0]['close']
                ##ldc = chart3.iloc[-1]  #last_candle
                #body_percentage = ((ldc['close'] - ldc['open'])/ldc['open'])*100
                #body_dict[name] = round(PD_body_percentage, 2)

                #if TO_Price > PDC_Price and RSID1 > RSID2 and RSID1 > 60 and SKD2 < SDD2 and SKD1 > SDD1 and SKD1 > 70 and PDV > PDSM50:
                #    print("crossover")
                #    crossover_dict[name] = price_change
                
                
                #daily_data = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")
                    #'SYMBOL', 'DIRECTION' ,'PRICEUP','FIRSTCANDLEPERC','SECONDCANDLEPERC','FIRSTCANDLEPRICEDIFF','RSIOVER50'
                    #['SYMBOL', 'DIRECTION','PRICEUP','RSIOVER50','SKDOVERSDD', 'SKD1OVERSKD2', 'SKDOVER70', 'VOLOVERSM50', 'BULLISHCROSS', 'SM21OVERSM50', 'BEARISHCROSS', 'RSIBELOW40', 'SKDBELOWSDD', 'SKDBELOW30', 'VOLBELOWM50', 'SM21BELOWSM50']
                #if direction != 'SIDEWAY':
                if Add == True:
                    if TodaysPrice:
                        row = [date.today(), name, direction, PDC_Price, TO_Price, TO_Price >= PDC_Price, TotalMovement, PD_body_perc1, PD_body_perc2, price_change, RSI1 > 50, SK1 > SD1, SK1 > SK2, SK1 > 70, PDV > PDSM50V, BullishCross, PDSM21V > PDSM50V, BearishCross, RSI1<40, SK1 < SD1, SK1 < 30, PDV<PDSM50V, PDSM21V < PDSM50V, WatchlistID]
                    else:
                        row = [date.today(), name, direction, PDC_Price, 0, None, TotalMovement, PD_body_perc1, PD_body_perc2, price_change, RSI1 > 50, SK1 > SD1, SK1 > SK2, SK1 > 70, PDV > PDSM50V, BullishCross, PDSM21V > PDSM50V, BearishCross, RSI1<40, SK1 < SD1, SK1 < 30, PDV<PDSM50V, PDSM21V < PDSM50V, WatchlistID]
                    rows.append(row)
            except:
                print("\nerror")
        if(len(rows)>0):      
            df = pd.DataFrame(rows, columns=columns)
            direction_order = ['BULLISH', 'BEARISH', 'BULLISH TREND', 'BEARISH TREND', 'PRICE UP', 'PRICE DOWN']

            # Filter and sort by DIRECTION according to the custom order
            #Start-----------------commented to test sorting by totalmovement-------------------------
            #filtered_df = df[df['DIRECTION'].isin(direction_order)].copy()
            #filtered_df['DIRECTION'] = pd.Categorical(filtered_df['DIRECTION'], categories=direction_order, ordered=True)
            #filtered_df = filtered_df.sort_values(['DIRECTION', 'FIRSTCANDLEPERC'], ascending=[True, False]).reset_index(drop=True)
            #End-----------------commented to test sorting by totalmovement---------------------------
            filtered_df = df.sort_values(['TOTALMOVEMENT'], ascending=[False]).reset_index(drop=True).head(10)
            #filtered_df = filtered_df.sort_values('DIRECTION').reset_index(drop=True)            
            #filtered_df = filtered_df.sort_values(['DIRECTION', 'FIRSTCANDLEPERC']).reset_index(drop=True)

            print("\nMomentum data collected")
            
            #df1 = Get_Two_Sisters_Candles(self, df, tsl)
            #print(df1)
        
        self.SetHistoricalRunIsOff()
        return filtered_df
        #put off the run switch
        


        # sorted_by_values = dict(sorted(body_dict.items(), key=lambda item: item[1]))
        # script_having_max_body = max(body_dict, key=body_dict.get)
        # script_having_min_body = min(body_dict, key=body_dict.get)
        # daily_data = tsl.get_historical_data(tradingsymbol = script_having_max_body, exchange = 'NSE',timeframe="DAY")
        # ldc = daily_data.iloc[-1]  #last_day_candle
        # tarde_info = {"Direction":"buy", "level":ldc['high']}


        # print(script_having_max_body)
        # print(tarde_info)

    def Get_All_LTP_Data(self, Symbols, Conn):
        #Symbols = df["SYMBOL"].astype(str).tolist()

        all_ltp_data = {}

        # Iterate in chunks of 20
        for i in range(0, len(Symbols), 10):
            chunk = Symbols[i:i+10]
            ltp_data = Conn.get_ltp_data(names=chunk)
            
            # Assuming ltp_data is a dictionary, merge it
            all_ltp_data.update(ltp_data)
            time.sleep(1)

        return all_ltp_data

    def SafeRound(self, value, RoundNumber=2):
        if pd.isna(value):
            return None
        return round(value, RoundNumber)

    def AddIndicatorColumns(self, chart, RSI=True, SMA=True, SK=True, MACD=True, BB=True):
        if not chart.empty and len(chart) >= 2:
            chart = chart.copy()  # Ensure safe modification

            if RSI:
                # RSI
                chart["RSI"] = round( talib.RSI(chart['close']),4)
            
            if SMA:
                # SMA
                chart['SM50'] = np.round(talib.SMA(chart['close'].to_numpy(), 50),4)
                chart['SM21'] = np.round(talib.SMA(chart['close'].to_numpy(), 21),4)

            if SK:
                # Stochastic K/D
                chart['SK'], chart['SD'] = np.round(talib.STOCH(
                    chart['high'].to_numpy(), chart['low'].to_numpy(), chart['close'].to_numpy(),
                    fastk_period=5, slowk_period=3, slowk_matype=0,
                    slowd_period=3, slowd_matype=0
                ),4)

            #MACD
            if MACD:
                # MACD
                #chart['MACD'], chart['MACDSIGNAL'], chart['MACDFAST'] = round(talib.MACD(chart['close']),4)
                
                macd, macdsignal, macdfast = talib.MACD(chart['close'])
                chart['MACD'] = np.round(macd, 4)
                chart['MACDSIGNAL'] = np.round(macdsignal, 4)
                chart['MACDFAST'] = np.round(macdfast, 4)
            
            # Calculate VWAP
            typical_price = (chart['high'] + chart['low'] + chart['close']) / 3
            vwap_numerator = (typical_price * chart['volume']).cumsum()
            vwap_denominator = chart['volume'].cumsum()
            chart['VWAP'] = round((vwap_numerator / vwap_denominator),4)

            #chart["UPPERBAND"], chart["MIDDLEBAND"], chart["LOWERBAND"] = round(talib.BBANDS(chart['close'],20),4)
            upper, middle, lower = talib.BBANDS(chart['close'], timeperiod=20)
            chart["UPPERBAND"] = np.round(upper, 4)
            chart["MIDDLEBAND"] = np.round(middle, 4)
            chart["LOWERBAND"] = np.round(lower, 4)

            return chart

            
    def Get_Indicators(self, chart, tsl, RSI=True, SMA=True, SK=True, MACD=True, LiveMode = TE.LiveMode.Live, Postfix = "", BB = False):    
        watchlist_921 = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC', 'BPCL', 'WIPRO', 'SHRIRAMFIN', 'ADANIPORTS', 'JSWSTEEL', 'COALINDIA', 'ULTRACEMCO', 'BAJAJ-AUTO', 'LT', 'POWERGRID', 'ADANIENT', 'SBIN', 'HCLTECH', 'TCS', 'EICHERMOT', 'BAJAJFINSV', 'TECHM', 'LTIM', 'HINDUNILVR', 'BHARTIARTL', 'AXISBANK', 'GRASIM', 'HEROMOTOCO', 'DRREDDY', 'ICICIBANK', 'HDFCBANK', 'BAJFINANCE', 'SBILIFE', 'RELIANCE', 'KOTAKBANK', 'ITC', 'TITAN', 'SUNPHARMA', 'INDUSINDBK', 'APOLLOHOSP', 'BRITANNIA', 'NESTLEIND', 'HDFCLIFE', 'DIVISLAB', 'CIPLA', 'ASIANPAINT', 'TATACONSUM']
        DI = {}

        if not chart.empty and len(chart) >= 2:
            

            if LiveMode!=TE.LiveMode.BackTest:
                chart = self.AddIndicatorColumns(chart, RSI, SMA, SK, MACD, False).copy()

            #chart = chart.copy()  # Ensure safe modification
            if RSI:
                # RSI
                #chart["RSI"] = talib.RSI(chart['close'])
                DI['RSID1' + Postfix] = self.SafeRound(chart["RSI"].iloc[-1])
                DI['RSID2' + Postfix] = self.SafeRound(chart["RSI"].iloc[-2])

            if SMA:
                # SMA
                #chart['SM50'] = talib.SMA(chart['close'].to_numpy(), 50)
                #chart['SM21'] = talib.SMA(chart['close'].to_numpy(), 21)

                DI['SM501' + Postfix] = self.SafeRound(chart['SM50'].iloc[-1])
                DI['SM502' + Postfix] = self.SafeRound(chart['SM50'].iloc[-2])
                DI['SM211' + Postfix] = self.SafeRound(chart['SM21'].iloc[-1])
                DI['SM212' + Postfix] = self.SafeRound(chart['SM21'].iloc[-2])

            if SK:
                # Stochastic K/D
                #chart['SK'], chart['SD'] = talib.STOCH(
                #    chart['high'].to_numpy(), chart['low'].to_numpy(), chart['close'].to_numpy(),
                #    fastk_period=5, slowk_period=3, slowk_matype=0,
                #    slowd_period=3, slowd_matype=0
                #)

                DI['SK1' + Postfix] = self.SafeRound(chart['SK'].iloc[-1])
                DI['SK2' + Postfix] = self.SafeRound(chart['SK'].iloc[-2])
                DI['SD1' + Postfix] = self.SafeRound(chart['SD'].iloc[-1])
                DI['SD2' + Postfix] = self.SafeRound(chart['SD'].iloc[-2])

            if MACD:
                # MACD
                #chart['MACD'], chart['MACDSIGNAL'], chart['MACDFAST'] = talib.MACD(chart['close'])
                DI['MACD1' + Postfix] = self.SafeRound(chart['MACD'].iloc[-1])
                DI['MACD2' + Postfix] = self.SafeRound(chart['MACD'].iloc[-2])
                DI['MACDSIGNAL1' + Postfix] = self.SafeRound(chart['MACDSIGNAL'].iloc[-1])
                DI['MACDSIGNAL2' + Postfix] = self.SafeRound(chart['MACDSIGNAL'].iloc[-2])
                DI['MACDFAST1' + Postfix] = self.SafeRound(chart['MACDFAST'].iloc[-1])
                DI['MACDFAST2' + Postfix] = self.SafeRound(chart['MACDFAST'].iloc[-2])

            if BB:
                DIBB = self.Get_Volume_Driven_Indicators(chart, TE.LiveMode.BackTest)

                DI['VWAP1' + Postfix] = DIBB['VWAP1']
                DI['VWAP2' + Postfix] = DIBB['VWAP2']
                
                #chart["UPPERBAND"], chart["MIDDLEBAND"], chart["LOWERBAND"] = talib.BBANDS(chart['close'],20)
                #BBU
                DI['BBU1' + Postfix] = DIBB['BBU1']
                DI['BBU2' + Postfix] = DIBB['BBU2']
                #BBM
                DI['BBM1' + Postfix] = DIBB['BBM1']
                DI['BBM2' + Postfix] = DIBB['BBM2']
                #BBB
                DI['BBB1' + Postfix] = DIBB['BBB1']
                DI['BBB2' + Postfix] = DIBB['BBB2']
                DI['LTP1' + Postfix] = DIBB['LTP1']
                DI['LTP2' + Postfix] = DIBB['LTP2']

            # Volume
            DI['VOL1' + Postfix] = chart['volume'].iloc[-1]
            DI['VOL2' + Postfix] = chart['volume'].iloc[-2]
            
            #VWAP
            #chart['VWAP'] = (((chart['high'] + chart['low'] + chart['close']) / 3) * chart['volume']).cumsum() / chart['volume'].cumsum()
            #DI['VWAP'] = chart['VWAP'].iloc[-1]


#chart['VWAP'] = VolumeWeightedAveragePrice(high=dataframe['high'], low=dataframe['low'], close=dataframe["close"], volume=dataframe['volume'], window=window, fillna=fillna).volume_weighted_average_price()

            # typical_price = (chart['high'] + chart['low'] + chart['close']) / 3
            # chart['Cumulative_TPV'] = (typical_price * chart['volume']).cumsum()
            # chart['Cumulative_Volume'] = chart['volume'].cumsum()
            # chart['VWAP'] = chart['Cumulative_TPV'] / chart['Cumulative_Volume']

            #BBU
            #chart["upper_band"], chart["middle_band"], chart["lower_band"] = talib.BBANDS(chart['close'],20)
            #DI['BBU'] = chart["upper_band"].iloc[-1]
            #BBM
            #DI['BBM'] = chart["middle_band"].iloc[-1]
            #BBB
            #DI['BBB'] = chart["lower_band"].iloc[-1]

        return DI

    def Get_Volume_Driven_Indicators(self, chart, LiveMode = TE.LiveMode.Live):
        DI = {}

        if not chart.empty:
            #VWAP
            #chart['VWAP'] = (((chart['high'] + chart['low'] + chart['close']) / 3) * chart['volume']).cumsum() / chart['volume'].cumsum()
            if LiveMode!=TE.LiveMode.BackTest:
                chart = self.AddIndicatorColumns(chart, False, False, False, False, True).copy()
            
            #chart = chart.copy()
            # Calculate VWAP
            typical_price = (chart['high'] + chart['low'] + chart['close']) / 3
            vwap_numerator = (typical_price * chart['volume']).cumsum()
            vwap_denominator = chart['volume'].cumsum()
            #chart['VWAP'] = vwap_numerator / vwap_denominator

            DI['VWAP1'] = self.SafeRound(chart['VWAP'].iloc[-1],4)
            DI['VWAP2'] = self.SafeRound(chart['VWAP'].iloc[-2],4)
            
            #chart["UPPERBAND"], chart["MIDDLEBAND"], chart["LOWERBAND"] = talib.BBANDS(chart['close'],20)
            #BBU
            DI['BBU1'] = self.SafeRound(chart["UPPERBAND"].iloc[-1],4)
            DI['BBU2'] = self.SafeRound(chart["UPPERBAND"].iloc[-2],4)
            #BBM
            DI['BBM1'] = self.SafeRound(chart["MIDDLEBAND"].iloc[-1],4)
            DI['BBM2'] = self.SafeRound(chart["MIDDLEBAND"].iloc[-2],4)
            #BBB
            DI['BBB1'] = self.SafeRound(chart["LOWERBAND"].iloc[-1],4)
            DI['BBB2'] = self.SafeRound(chart["LOWERBAND"].iloc[-2],4)
            DI['LTP1'] = self.SafeRound(chart["close"].iloc[-1],2)
            DI['LTP2'] = self.SafeRound(chart["close"].iloc[-2],2)

            return DI


    def Watch_BB_VWAP(self, Watchlist, tsl, Period, Actionable_Watchlist):
        print("a")

        for SYMBOL in Watchlist:
            
            #pass if symbol is already added to the actionable watchlist
            if Actionable_Watchlist["SYMBOL"].count(SYMBOL) > 0:
                continue

            chart = tsl.get_intraday_data(SYMBOL, 'NSE', Period)
            DI = self.Get_Volume_Driven_Indicators(self, chart)
            LTP = tsl.get_ltp_data[SYMBOL]
            VWAP    =   DI['VWAP1']
            BBU     =   DI['BBU1']
            BBM     =   DI['BBM1']
            BBB     =   DI['BBB1']
            Open    =   chart["open"].iloc[-1]
            High    =   chart["high"].iloc[-1]
            Low     =   chart["low"].iloc[-1]
            Close   =   chart["close"].iloc[-1]
            
            if (BBU <= Close and Close > Open) :
                print("BBU Close touched from bottom")
                #add to the actionable watchlist array
                #Add next action i.e. High and low either > BBU or < BBU and RSI, Stochastics status is accordingly then Buy or Sell
            elif BBU <= High:
                print("BBU High touched from bottom")
            elif BBU >= Close and Close < Open: 
                print("BBU Close touched from Top")
            elif BBU >= Low:
                print("BBU Low touched from Top")
    #Watchlist = Watchlist.reset_index()
    #for index, WatchlistRow in df.iterrows():
    
    def Get_LTP_BBVWAP_Position(self, LTP, Chart, LiveMode=TE.LiveMode.Live):
        DL = self.Get_Volume_Driven_Indicators(Chart, LiveMode)
        VWAP = DL["VWAP1"]
        BBU = DL["BBU1"]
        BBM = DL["BBM1"]
        BBB = DL["BBB1"]
        VVAPPosition = LTPPosition = TE.BB_VWAP_LTP_Position.NotSet
        DLBB = {}

        if BBU is not None:
            FirstDiff = BBU-BBM
            SecondDiff = BBM-BBB
            Center = BBM
            DLBB["CenterBase"] = "BBM"

            #VVAP position
            if VWAP > BBU:
                VVAPPosition = TE.BB_VWAP_LTP_Position.Above_BBU
            elif VWAP < BBB:
                VVAPPosition = TE.BB_VWAP_LTP_Position.Below_BBB

            #if VVAPPosition == TE.BB_VWAP_LTP_Position.NotSet:
                #FirstDiff = BBU-VWAP
                #SecondDiff = VWAP-BBB
                #Center = VWAP
                #DLBB["CenterBase"] = "VWAP"

            elif (BBU - (FirstDiff*Const.BBCenterDiffRatio)) <= VWAP <= (BBU + (FirstDiff*Const.BBCenterDiffRatio)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.On_BBU
            elif (BBB + (SecondDiff*Const.BBCenterDiffRatio)) >= VWAP >= (BBU - (FirstDiff*Const.BBCenterDiffRatio)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.On_BBB
            elif VWAP > (Center+(FirstDiff*.75)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.TH_75
            elif VWAP > (Center+(FirstDiff*.50)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.TH_50
            elif VWAP > (Center+(FirstDiff*.25)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.TH_25
            elif VWAP > Center:
                VVAPPosition = TE.BB_VWAP_LTP_Position.Above_Center
            elif (BBM + (BBM*Const.BBCenterDiffRatio)) >= VWAP >= (BBM - (BBM*Const.BBCenterDiffRatio)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.On_Center
            elif VWAP > (BBB+(SecondDiff*.75)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.BH_75
            elif VWAP > (BBB+(SecondDiff*.50)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.BH_50
            elif VWAP > (BBB+(SecondDiff*.25)):
                VVAPPosition = TE.BB_VWAP_LTP_Position.BH_25
            elif VWAP > BBB:
                VVAPPosition = TE.BB_VWAP_LTP_Position.Above_BBB
            #else:
            # FirstDiff = BBU-BBM
            # SecondDiff = BBM-BBB
            # Center = BBM
            # DLBB["CenterBase"] = "BBM"

                
            
            DLBB["FirstDiff"]   =   FirstDiff
            DLBB["SecondDiff"]  =   SecondDiff
            DLBB["Center"]      =   Center
            DLBB["VWAP"]        =   VWAP
            DLBB["BBU"]         =   BBU
            DLBB["BBB"]         =   BBB

            #VVAP Position
            
            
            #LTP Position
            if LTP > BBU:
                LTPPosition = TE.BB_VWAP_LTP_Position.Above_BBU
            elif LTP < BBB:
                LTPPosition = TE.BB_VWAP_LTP_Position.Below_BBB
            elif (BBU - (FirstDiff*Const.BBCenterDiffRatio)) <= LTP <= (BBU + (FirstDiff*Const.BBCenterDiffRatio)):
                LTPPosition = TE.BB_VWAP_LTP_Position.On_BBU
            elif (BBB + (SecondDiff*Const.BBCenterDiffRatio)) >= LTP >= (BBU - (FirstDiff*Const.BBCenterDiffRatio)):
                LTPPosition = TE.BB_VWAP_LTP_Position.On_BBB
            elif LTP > (Center+(FirstDiff*.75)):
                LTPPosition = TE.BB_VWAP_LTP_Position.TH_75
            elif LTP > (Center+(FirstDiff*.50)):
                LTPPosition = TE.BB_VWAP_LTP_Position.TH_50
            elif LTP > (Center+(FirstDiff*.25)):
                LTPPosition = TE.BB_VWAP_LTP_Position.TH_25
            elif LTP > Center:
                LTPPosition = TE.BB_VWAP_LTP_Position.Above_Center
            elif (Center + (Center*Const.BBCenterDiffRatio)) >= LTP >= (Center - (Center*Const.BBCenterDiffRatio)):
                LTPPosition = TE.BB_VWAP_LTP_Position.On_Center
            elif LTP > (BBB+(SecondDiff*.75)):
                LTPPosition = TE.BB_VWAP_LTP_Position.BH_75
            elif LTP > (BBB+(SecondDiff*.50)):
                LTPPosition = TE.BB_VWAP_LTP_Position.BH_50
            elif LTP > (BBB+(SecondDiff*.25)):
                LTPPosition = TE.BB_VWAP_LTP_Position.BH_25
            elif LTP > BBB:
                LTPPosition = TE.BB_VWAP_LTP_Position.Above_BBB

            DLBB["VWAPPosition"]    =   VVAPPosition
            DLBB["LTPPosition"]     =   LTPPosition
            DLBB["INDICATORS"]      =   DL

            #print("LTP position: " + LTPPosition.name)
        # also check if difference is > .4 else retrun pass
        return DLBB #VVAPPosition, LTPPosition, #difference is > .4
    

    def Get_BB_Call(self, LTP, Chart, DLIndicators, TradeType=TE.TradeType.SCALPING, LiveMode=TE.LiveMode.Live):
        DLBB            =   self.Get_LTP_BBVWAP_Position(LTP, Chart, LiveMode)

        TargetPrice     =   0
        SLPrice         =   0
        TargetBB        =   None
        SLBB            =   None
        TargetBBPrice   =   None
        SLBBPrice       =   None
        TargetLastPrice =   None
        SLLastPrice     =   None
        #We store Percentage of Target and SL
        TargetPricePerc =   None
        SLPricePerc     =   None
        BBCall          =   TE.OrderDirection.PASS
        Pass            =   False
        DLRes           =   {}

        if DLBB:
            LTPPosition     =   DLBB["LTPPosition"]
            VWAPPosition    =   DLBB["VWAPPosition"]
            BBU             =   DLBB["BBU"]
            BBB             =   DLBB["BBB"]
            VWAP            =   DLBB["VWAP"]
            FirstDiff       =   DLBB["FirstDiff"]
            SecondDiff       =   DLBB["SecondDiff"]
            Center          =   DLBB["Center"]
            
            FirstHalfRatio  =   round((FirstDiff/LTP),4)
            SecondHalfRatio =   round((SecondDiff/LTP),4)
            FirstDiffBuff   =   FirstDiff*.1
            SecondDiffBuff  =   SecondDiff*.1
            Close1          =   Chart.iloc[-1]["close"]
            Close2          =   Chart.iloc[-2]["close"]
            UPDirection     =   Close1 > Close2
            
            #Get BB Trend - Touched Top/VVAP and moving down, so candidate for lead
            #Also check whether its following VVAP or BBU/BBB

            BuyTargetPricePerc = 1.006
            SellTargetPricePerc = .994
            BuySLPricePerc      = .996
            SellSLPricePerc     = 1.004
            if FirstHalfRatio < Const.BBMinSpaceRatio and SecondHalfRatio < Const.BBMinSpaceRatio: 
                #return pass
                BBCall      =   TE.OrderDirection.PASS
            else:
                if ((LTPPosition == TE.BB_VWAP_LTP_Position.On_Center or
                    LTPPosition == TE.BB_VWAP_LTP_Position.Above_Center or
                    LTPPosition == TE.BB_VWAP_LTP_Position.TH_25)
                    and UPDirection and FirstHalfRatio >= Const.BBMinSpaceRatio) :

                    #Set prices
                    BBCall          =   TE.OrderDirection.BUY
                    #TargetPrice     =   BBU - FirstDiffBuff
                    TargetPrice     =   LTP * BuyTargetPricePerc
                    #SLPrice         =   Center - FirstDiffBuff
                    SLPrice         =   LTP * BuySLPricePerc
                    TargetBB        =   "BBU"
                    SLBB            =   DLBB["CenterBase"]
                    SLBBPrice       =   DLBB["Center"]
                    TargetBBPrice   =   DLBB["BBU"]
                    
                elif ((
                    LTPPosition == TE.BB_VWAP_LTP_Position.TH_50)
                    and UPDirection and FirstHalfRatio >= (Const.BBMinSpaceRatio*2)) :

                    #Set prices
                    BBCall          =   TE.OrderDirection.BUY
                    #TargetPrice     =   BBU - FirstDiffBuff
                    TargetPrice     =   LTP * BuyTargetPricePerc
                    #SLPrice         =   Center - FirstDiffBuff
                    SLPrice         =   LTP * BuySLPricePerc
                    TargetBB        =   "BBU"
                    SLBB            =   DLBB["CenterBase"]
                    SLBBPrice       =   DLBB["Center"]
                    TargetBBPrice   =   DLBB["BBU"]

                elif ((LTPPosition == TE.BB_VWAP_LTP_Position.On_BBB or
                       LTPPosition == TE.BB_VWAP_LTP_Position.Above_BBB or
                        LTPPosition == TE.BB_VWAP_LTP_Position.BH_25)
                        and UPDirection and SecondHalfRatio >= Const.BBMinSpaceRatio):
                    
                    BBCall          =   TE.OrderDirection.BUY
                    #SLPrice         =   BBB - SecondDiffBuff
                    SLPrice         =   LTP * BuySLPricePerc

                    if TradeType == TE.TradeType.SCALPING:
                        #TargetPrice     =   Center - SecondDiffBuff
                        TargetPrice     =   LTP * BuyTargetPricePerc
                        TargetBB        =   DLBB["CenterBase"]
                        TargetBBPrice   =   DLBB["Center"]
                    elif TradeType == TE.TradeType.MIS:
                        #TargetPrice     =   BBU - FirstDiffBuff
                        TargetPrice     =   LTP * BuyTargetPricePerc
                        TargetBB        =   "BBU"
                        TargetBBPrice   =   DLBB["BBU"]
                    
                    SLBB            =   "BBB"
                    SLBBPrice       =   DLBB["BBB"]
                    

                elif ((LTPPosition == TE.BB_VWAP_LTP_Position.On_BBU or
                    LTPPosition == TE.BB_VWAP_LTP_Position.TH_75)
                    and not UPDirection and FirstHalfRatio > Const.BBMinSpaceRatio) :
                    #Call
                    BBCall          =   TE.OrderDirection.SELL

                    #Stop Loss
                    #SLPrice         =   BBU + FirstDiffBuff
                    SLPrice         =   LTP * SellSLPricePerc
                    #Target
                    if TradeType == TE.TradeType.SCALPING:
                        #TargetPrice     =   Center + FirstDiffBuff
                        TargetPrice     =   LTP*SellTargetPricePerc
                        TargetBB        =   DLBB["CenterBase"]
                        TargetBBPrice   =   DLBB["Center"]
                    elif TradeType == TE.TradeType.MIS:
                        #TargetPrice     =   BBB + FirstDiffBuff
                        TargetPrice     =   LTP*SellTargetPricePerc
                        TargetBB        =   "BBB"
                        TargetBBPrice   =   DLBB["BBB"]

                    SLBB            =   "BBU"
                    SLBBPrice       =   DLBB["BBU"]

                elif ((LTPPosition == TE.BB_VWAP_LTP_Position.On_Center or
                    LTPPosition == TE.BB_VWAP_LTP_Position.BH_75)
                    and not UPDirection  and SecondHalfRatio >= Const.BBMinSpaceRatio):
                    BBCall          =   TE.OrderDirection.SELL
                    #TargetPrice     =   BBB + SecondDiffBuff
                    TargetPrice     =   LTP*SellTargetPricePerc
                    #SLPrice         =   Center + SecondDiffBuff
                    SLPrice         =   LTP * SellSLPricePerc

                    TargetBB        =   "BBB"
                    SLBB            =   DLBB["CenterBase"]
                    SLBBPrice       =   DLBB["Center"]
                    TargetBBPrice   =   DLBB["BBB"]

                elif ((LTPPosition == TE.BB_VWAP_LTP_Position.BH_50)
                    and not UPDirection  and SecondHalfRatio >= (Const.BBMinSpaceRatio*2)):
                    BBCall          =   TE.OrderDirection.SELL
                    #TargetPrice     =   BBB + SecondDiffBuff
                    TargetPrice     =   LTP*SellTargetPricePerc
                    #SLPrice         =   Center + SecondDiffBuff
                    SLPrice         =   LTP * SellSLPricePerc

                    TargetBB        =   "BBB"
                    SLBB            =   DLBB["CenterBase"]
                    SLBBPrice       =   DLBB["Center"]
                    TargetBBPrice   =   DLBB["BBB"]

            #We store Percentage of Target and SL
            if TargetPrice > 0 and SLPrice >0:
                TargetPricePerc     =   round(((abs(LTP-TargetPrice)/LTP)*100),2)
                SLPricePerc         =   round(((abs(LTP-SLPrice)/LTP)*100),2)
                if SLPricePerc>TargetPricePerc: 
                    BBCall      =   TE.OrderDirection.PASS
                #Add conditions for sticky trend (LTP sticks with BBU/BBB/VWAP)
                #Add conditions if VWAP is out of boundry or near the boundry and BBU-BBB diff is wide
                
        else:
            BBCall      =   TE.OrderDirection.PASS

        


        #Update Prices
        DLBB["INDICATORS"]["TargetBB"]              =   TargetBB
        DLBB["INDICATORS"]["SLBB"]                  =   SLBB
        DLBB["INDICATORS"]["SLBBLastPrice"]         =   SLBBPrice
        DLBB["INDICATORS"]["TargetBBLastPrice"]     =   TargetBBPrice
        DLBB["INDICATORS"]["TargetLastPrice"]       =   TargetPrice
        DLBB["INDICATORS"]["SLLastPrice"]           =   SLPrice
        DLBB["INDICATORS"]["LTPPosition"]           =   LTPPosition.value
        DLBB["INDICATORS"]["VWAPPosition"]          =   VWAPPosition.value
        
        #Return DL
        DLRes["BBCall"]     =   BBCall
        DLRes["TargetPricePerc"]=   TargetPricePerc
        DLRes["SLPricePerc"]    =   SLPricePerc
        DLRes["INDICATORS"]     =   DLBB["INDICATORS"]
        
        return DLRes

    def StoreOrderBBData(self, DL):
        DBO = DBOps()

        DBO.InsertOrderBBData(DL)
    
    def UpdateOrderBBData(self, DL):
        DBO = DBOps()

        DBO.UpdateOrderBBData(DL)

    def GetOrderBBData(self, OrderID):
        DBO = DBOps()

        return DBO.GetOrderBBData(OrderID)














        #If LTPPosition == BH25 and 
        #If LTPPosition == Above BBB or Above Center and Chart Last Close > Second last close Buy
        #Elif Chart Last Close < Second last close Sell
        #Elif other conditions
        #else Pass








        #Loop the watchlist
        #get the type of watch - Upperband touch from bottom, Upperband touch from top, upperband crossed downside, upperband crossed upside, upperband left dwonside, upperband left upside, 
        # vwap touched from bottom, vwap touched from top, vwap crossed downside, vwap crossed upside, vwap left upside,vwap left downside, 
        # Lowerband touch from bottom, Lowerband touch from top, Lowerband crossed downside, Lowerband crossed upside, Lowerband left upside, Lowerband left downside
                # last_row = data.iloc[-1]
                # second_last_row = data.iloc[-2]

                # if second_last_row['Close'] > second_last_row['VWAP'] and last_row['Close'] < last_row['VWAP']:
                #     print('Price Cross Below VWAP')
                # elif second_last_row['Close'] < second_last_row['VWAP'] and last_row['Close'] > last_row['VWAP']:
                #     print('Price Cross Above VWAP')
                # else:
                #     print('No Crossover')

    def Get_Two_Sisters_Candles(self, Watchlist, Exchange, CandleSize, tsl, TotalValueBasis, MaxPrice):  
        rows = []
        columns=('SYMBOL', 'BULLISH', 'TOTALVALUE', 'OrderID', 'OrderPrice', 'OrderQty', 'SLPrice', 'SLOrderID', 'TargetPrice', 'TargetOrderID', 'OrderExpenses', 'OrderClosingType', 'FinalExecutedPrice', 'PLStatus', 'TradeStatus', 'TradeClosingSource')

        #df = pd.DataFrame() #columns=('Symbol', 'ValueType', 'TotalValue'))
        ctr = 0
        curr_time = datetime.now().strftime(Const.Time_Format) 

        Watchlist = Watchlist.reset_index()

        #wait if another thread is running this function to avoid an exception of too many requests from Dhan
        self.HDAvailable()

        
        print("\n --Get Two Sisters-- script started at " + str(curr_time))

        for index, WatchlistRow in Watchlist.iterrows():
            try:
                #time.sleep(1)
                #Get 3 min Intraday data
                Chart = tsl.get_intraday_data(WatchlistRow['SYMBOL'], Exchange.name, CandleSize)
                #Get First Candle Perc
                Candle      =   Chart.iloc[-1]  #last_candle daily
                LTP         =   Candle['close']       
                Body_Perc1 = ((Candle['close'] - Candle['open'])/Candle['open'])*100
                Candle     =    Chart.iloc[-2]  #second last_candle daily
                Body_Perc2 = ((Candle['close'] - Candle['open'])/Candle['open'])*100
                Body1_Bullish   =   Body_Perc1 > 0
                Body2_Bullish   =   Body_Perc2 > 0
                VWAP            =   0
                BBU             =   0
                BBM             =   0
                BBB             =   0
                Body1_Position  =   0   #create a function to get the position - near and over VWAP   
                #Get Second Candle Pers
                #Total Pers

            #for name in Watchlist:   
                if ((Body_Perc1 > 0 and Body_Perc2 > 0) or (Body_Perc1 < 0 and Body_Perc2 < 0)) and abs(Body_Perc1 + Body_Perc2) > TotalValueBasis and LTP<=MaxPrice: 
                    row = [ WatchlistRow["SYMBOL"], Body_Perc1>0, round(abs(Body_Perc1 + Body_Perc2),2), 0, 0, 0, 0,0,0,0,0,TE.OrderDirection.NOTSET,0,0, TE.TradeStatus.Pending, TE.TradeClosingSource.NotPlaced.name]
                    print(WatchlistRow["SYMBOL"] + " - " + "Bullish - " + str( Body_Perc1>0) + " - " + " {:.2f}".format(abs(Body_Perc1 + Body_Perc2)) )
                    rows.append(row)
                
                print("\n"+ WatchlistRow["SYMBOL"])
                #elif WatchlistRow['FIRSTCANDLEPERC'] < 0 and WatchlistRow['SECONDCANDLEPERC'] < 0:
                    #row = [WatchlistRow["SYMBOL"], 0, abs(WatchlistRow['FIRSTCANDLEPERC'] + WatchlistRow['SECONDCANDLEPERC'])]
                    #rows.append(row)
            except:
                print("error with " + WatchlistRow['SYMBOL'])
        df = pd.DataFrame(rows, columns=columns)
        
        df = df.sort_values(by=['TOTALVALUE'], ascending=False)
        df = df.head(Const.Max_Trade_At_Once).reset_index(drop=True)

        print("\n'Get Two Sisters' script finished at " + str(curr_time))

        self.SetHistoricalRunIsOff()
        
        return df
    
    def Get_Indicator_Calls_for_Watchlist(self, Watchlist, Exchange, CandleSize, tsl, TotalValueBasis, MaxPrice):  
        rows = []
        #columns=('SYMBOL', 'BULLISH', 'TOTALVALUE', 'OrderID', 'OrderPrice', 'OrderQty', 'SLPrice', 'SLOrderID', 'TargetPrice', 'TargetOrderID', 'OrderExpenses', 'OrderClosingType', 'FinalExecutedPrice', 'PLStatus', 'TradeStatus', 'TradeClosingSource')
        columns=('SYMBOL', 'CallType', 'HighScore', 'BuyScore', 'SellScore', 'OrderID', 'OrderPrice', 'OrderQty', 'SLPrice', 'SLOrderID', 'TargetPrice', 'TargetOrderID', 'OrderExpenses', 'OrderClosingType', 'FinalExecutedPrice', 'PLStatus', 'TradeStatus', 'TradeClosingSource')

        #df = pd.DataFrame() #columns=('Symbol', 'ValueType', 'TotalValue'))
        ctr = 0
        curr_time = datetime.now().strftime(Const.Time_Format) 

        Watchlist = Watchlist.reset_index()

        #wait if another thread is running this function to avoid an exception of too many requests from Dhan
        self.HDAvailable()

        
        print("\n --Get Indicator Call-- script started at " + str(curr_time))

        for index, WatchlistRow in Watchlist.iterrows():
            try:
                #time.sleep(1)
                #Get 3 min Intraday data
                Chart = tsl.get_intraday_data(WatchlistRow['SYMBOL'], Exchange.name, CandleSize)
                DLIND = self.Get_Indicators(Chart, tsl)
                DLBB = self.Get_Volume_Driven_Indicators(Chart)

                INDCall, BuyScore, SellScore = self.GetIndicatorCall(DLIND, DLBB)

                LTP = Chart.iloc[-1]["close"]
                #Call BBAnalysis function
                DLBBCall = self.Get_BB_Call(LTP, Chart, DLIND, TE.TradeType.SCALPING)

                if INDCall != DLBBCall["BBCall"] or INDCall == TE.OrderDirection.PASS:
                    print(WatchlistRow['SYMBOL'] + ' - Pass')
                    continue

                if BuyScore>= SellScore: HighScore = BuyScore 
                else: HighScore = SellScore

                """ #Get First Candle Perc
                Candle      =   Chart.iloc[-1]  #last_candle daily
                LTP         =   Candle['close']       
                Body_Perc1 = ((Candle['close'] - Candle['open'])/Candle['open'])*100
                Candle     =    Chart.iloc[-2]  #second last_candle daily
                Body_Perc2 = ((Candle['close'] - Candle['open'])/Candle['open'])*100
                Body1_Bullish   =   Body_Perc1 > 0
                Body2_Bullish   =   Body_Perc2 > 0
                VWAP            =   0
                BBU             =   0
                BBM             =   0
                BBB             =   0
                Body1_Position  =   0   #create a function to get the position - near and over VWAP   
                #Get Second Candle Pers
                #Total Pers """

            #for name in Watchlist:   
                #if ((Body_Perc1 > 0 and Body_Perc2 > 0) or (Body_Perc1 < 0 and Body_Perc2 < 0)) and abs(Body_Perc1 + Body_Perc2) > TotalValueBasis and LTP<=MaxPrice: 
                if INDCall == TE.OrderDirection.BUY or INDCall == TE.OrderDirection.SELL:
                    row = [ WatchlistRow["SYMBOL"], INDCall , HighScore, BuyScore, SellScore, 0, 0, 0, 0,0,0,0,0,TE.OrderDirection.NOTSET,0,0, TE.TradeStatus.Pending, TE.TradeClosingSource.NotPlaced.name]
                    print("\n********")
                    print("\n" + WatchlistRow["SYMBOL"] + " - " + "Call - " + INDCall.name + " - " + " Buy Score: " + str(BuyScore) + " Sell Score: " + str(SellScore) )
                    print("\n********")
                    rows.append(row)
                else:
                    print("\n" + WatchlistRow["SYMBOL"] + " - " + " Buy Score: " + str(BuyScore) + " Sell Score: " + str(SellScore))
                #elif WatchlistRow['FIRSTCANDLEPERC'] < 0 and WatchlistRow['SECONDCANDLEPERC'] < 0:
                    #row = [WatchlistRow["SYMBOL"], 0, abs(WatchlistRow['FIRSTCANDLEPERC'] + WatchlistRow['SECONDCANDLEPERC'])]
                    #rows.append(row)
            except:
                print("error with " + WatchlistRow['SYMBOL'])
        df = pd.DataFrame(rows, columns=columns)
        
        df = df.sort_values(by=['HighScore'], ascending=False).reset_index(drop=True)
        #df = df.head(Const.Max_Trade_At_Once).reset_index(drop=True)

        print("\n'Get Indicators Call' script finished at " + str(curr_time))

        self.SetHistoricalRunIsOff()
        
        return df

    def Get_1_3_5M_Indicators(self, Conn, Symbol, ExchangeName, M1=True, M3=True, M5=True, M1Chart=None, M3Chart=None, M5Chart=None):
        if M1:
            if M1Chart is None:
                M1Chart = Conn.get_intraday_data(Symbol, ExchangeName, 1)
            DL1M =  self.Get_Indicators(M1Chart, Conn)
            if not M3 and not M5:
                return DL1M
        if M3:
            if M3Chart is None:
                M3Chart = Conn.get_intraday_data(Symbol, ExchangeName, 3)
            DL3M = self.Get_Indicators(M3Chart, Conn)
            if not M1 and not M5:
                return DL3M
        if M5:
            if M5Chart is None:
                M5Chart = Conn.get_intraday_data(Symbol, ExchangeName, 5)
            DL5M = self.Get_Indicators(M5Chart, Conn)
            if not M3 and not M1:
                return DL5M
        
        if M1 and M3 and M5:
            return DL1M, DL3M, DL5M
        elif M1 and M3:
            return DL1M, DL3M
        elif M1 and M5:
            return DL1M, DL5M
        elif M3 and M5:
            return DL3M, DL5M
        

    def GetHistoricalRunState(self):
        DBO = DBOps()

        return DBO.isHistoricalOnRun(datetime.now().strftime(Const.Time_Format))
    
    def SetHistoricalRunIsOn(self):
        DBO = DBOps()

        DBO.SetHistoricalRunState(1, datetime.now().strftime(Const.Time_Format))

    def SetHistoricalRunIsOff(self):
        DBO = DBOps()

        DBO.SetHistoricalRunState(0, datetime.now().strftime(Const.Time_Format))

    """ def GetTwoSistersRunState(self):
        DBO = DBOps()

        return DBO.isHistoricalOnRun()
    
    def SetTwoSistersRunIsOn(self):
        DBO = DBOps()

        DBO.SetHistoricalRunState(1)

    def SetTwoSistersRunIsOff(self):
        DBO = DBOps()

        DBO.SetHistoricalRunState(0)

    def TwoSistersAvailable(self):
        while True:
            if not self.GetTwoSistersRunState():
                print("Ready to fetch the Two Sisters Data: " + str(datetime.now().strftime(Const.Time_Format)))
                self.SetTwoSistersRunIsOn()
                break
            else:
                print("Waiting for a thread to fetch the Two Sisters Data: " + str(datetime.now().strftime(Const.Time_Format)))
                time.sleep(10)
 """
    def HDAvailable(self):
        
        while True:
            if not self.GetHistoricalRunState():
                self.SetHistoricalRunIsOn()
                print("Ready to fetch the Historical Data: " + str(datetime.now().strftime(Const.Time_Format)))
                break
            else:
                print("Waiting for a thread to fetch the Historical Data: " + str(datetime.now().strftime(Const.Time_Format)))
                time.sleep(10)

    def TakeACall(self, Chart, DL):
        DLB  =   self.Get_Volume_Driven_Indicators(Chart)

    def GetIndicatorCall(self, DL, DLBB):
        Score = 0
        CommonScore = 0
        BuyScore = 0
        SellScore = 0
        Counter = 0

        # Common indicators
        if DL["MACD1"] is not None and DL["MACD2"] is not None:
            if DL["MACD1"] > DL["MACD2"]: 
                CommonScore += 1
            

            if DL["MACD1"] > DL["MACDSIGNAL1"]: 
                CommonScore += 1

            Counter += 2

        if DL["SM211"] is not None and DL["SM501"] is not None:
            if DL["SM211"] > DL["SM501"]: 
                CommonScore += 1
            Counter += 1
        
        #if is_buy:
        if DL["RSID1"] is not None:
            if DL["RSID1"] > DL["RSID2"]: BuyScore += 1
            if DL["RSID1"] > 50: BuyScore += 1
            if DL["RSID1"] < DL["RSID2"]: SellScore += 1
            if DL["RSID1"] < 50: SellScore += 1
            Counter += 2

        if DL["SK1"] is not None:
            if DL["SK1"] > DL["SK2"]: BuyScore += 1
            if DL["SK1"] > DL["SD1"]: BuyScore += 1
            if DL["SD1"] > DL["SD2"]: BuyScore += 1
            if DL["SK1"] < DL["SK2"]: SellScore += 1
            if DL["SK1"] < DL["SD1"]: SellScore += 1
            if DL["SD1"] < DL["SD2"]: SellScore += 1
            Counter += 3
        #else:
        
        # === Bollinger Band logic ===
        if DLBB is not None:
            if DLBB["BBU1"] is not None:
                ltp, bbu, bbl, bbm = DLBB["LTP1"], DLBB["BBU1"], DLBB["BBB1"], DLBB["BBM1"]

                #if is_buy:
                if ltp <= bbl * 1.02: BuyScore += 1   # near lower band
                if ltp > bbm and ltp < (bbm *1.25): BuyScore += 1           # above mid-band
                #else:
                if ltp >= bbu * 0.98: SellScore += 1   # near upper band
                if ltp < bbm and ltp > (bbm*.75): SellScore += 1           # below mid-band

                # Band symmetry check
                if abs((bbu - bbm) - (bbm - bbl)) < 0.5:
                    CommonScore += 1
                Counter += 2

        BuyScore += CommonScore
        SellScore += CommonScore

        if ((Counter <= 15 and (BuyScore >= 9)) or (Counter <= 7 and (BuyScore >= 7))) and BuyScore > SellScore and DL["RSID1"] > 70 and DL["SK1"] > 70:
            Call = TE.OrderDirection.BUY
        elif (Counter <= 15 and (SellScore >= 9)) or (Counter <= 7 and (SellScore >= 7)) and DL["RSID1"] < 30 and DL["SK1"] <30:
            Call = TE.OrderDirection.SELL
        elif ((Counter <= 10 and (BuyScore >= 5)) or  (Counter <= 7 and ((BuyScore) >= 3))) or ((Counter <= 9 and (SellScore >= 5)) or  (Counter <= 7 and (SellScore >= 3))):
            Call = TE.OrderDirection.LEAD
        else:
            Call = TE.OrderDirection.PASS
        
        #print("\nBuy Score: " + str(BuyScore) + ", Sell Score: "+ str(SellScore))

        return Call, BuyScore, SellScore
    

    def Get_Intraday_Historical_Data(self, Conn, Symbol, DurationInMonths=12):
        DBO = DBOps()
        end_date = datetime.now() - timedelta(days=1)
        last_date = DBO.GetSymbolHistLastDate(Symbol)

        if last_date is None:
            start_date = end_date - timedelta(days=365)
        else:
            last_date_dt = datetime.strptime(last_date, "%Y-%m-%d")
            start_date = last_date_dt + timedelta(days=1)

        chunk_days = 3
        current = start_date
        DBB = DBBase()

        prevDF_1m = None
        prevDF_3m = None
        prevDF_5m = None
        prev_date = None
        start_time = datetime.now().strftime(Const.Time_Format)
        Days_Count = 0

        # Load holidays
        holiday_dates = self.load_holiday_dates()

        while current < end_date:
            # Get 3-day chunk
            chunk_dates = [
                current + timedelta(days=i)
                for i in range(chunk_days)
                if current + timedelta(days=i) <= end_date
            ]

            # Filter valid trading days
            valid_days = [
                d for d in chunk_dates
                if d.weekday() < 5 and d.date() not in holiday_dates
            ]

            # Decide fetch range
            if not valid_days:
                print(f"[INFO] Skipping non-trading chunk starting {current.date()} (weekends/holidays)")
                current += timedelta(days=chunk_days)
                continue
            elif len(valid_days) == 1:
                from_date = to_date = valid_days[0].strftime('%Y-%m-%d')
            else:
                from_date = valid_days[0].strftime('%Y-%m-%d')
                to_date = valid_days[-1].strftime('%Y-%m-%d')

            try:
                df = Conn.get_intraday_data(Symbol, 'NSE', 1, start_date=from_date, end_date=to_date)
            except Exception as e:
                print(f"[ERROR] Failed to fetch data from {from_date} to {to_date} for {Symbol}: {e}")
                current += timedelta(days=chunk_days)
                time.sleep(2)
                continue

            if df is None or df.empty:
                print(f"[INFO] No data returned for {Symbol} from {from_date} to {to_date}")
                current += timedelta(days=chunk_days)
                time.sleep(2)
                continue

            df['timestamp'] = pd.to_datetime(df['timestamp'])

            for date, df1m_day in df.groupby(df['timestamp'].dt.date):
                if prev_date is not None and date == prev_date:
                    continue

                df3m_day, df5m_day = self.convert_to_3min_5min(df1m_day)

                self.ProcessSymbolHistData(prevDF_1m, df1m_day.copy(), Symbol, '1', date)
                prevDF_1m = df1m_day.copy()

                self.ProcessSymbolHistData(prevDF_3m, df3m_day.copy(), Symbol, '3', date)
                prevDF_3m = df3m_day.copy()

                self.ProcessSymbolHistData(prevDF_5m, df5m_day.copy(), Symbol, '5', date)
                prevDF_5m = df5m_day.copy()

                print(f"[OK] Inserted {len(df1m_day)} rows for {Symbol} on {date}")
                prev_date = date
                Days_Count += 1

            current += timedelta(days=chunk_days)
            time.sleep(2)

        end_time = datetime.now().strftime(Const.Time_Format)
        start_dt = datetime.strptime(start_time, Const.Time_Format)
        end_dt = datetime.strptime(end_time, Const.Time_Format)
        time_taken = end_dt - start_dt

        print(f"Started: {start_time}, Finished: {end_time}, Time Taken: {time_taken}, Days: {Days_Count}")






    # def Get_Intraday_Historical_Data(self, Conn, Symbol, DurationInMonths=12):
    #     DBO             = DBOps()
    #     end_date        = datetime.now() - timedelta(days=1)
    #     last_date       = DBO.GetSymbolHistLastDate(Symbol)
    #     #holiday_dates   = self.load_holiday_dates()

    #     if last_date is None:
    #         start_date      = end_date - timedelta(days=365)
    #     else:
    #         #last_date = "2025-07-04"
    #         last_date_dt = datetime.strptime(last_date, "%Y-%m-%d")
    #         start_date = last_date_dt + timedelta(days=1)

    #     chunk_days      = 3
    #     current         = start_date
    #     DBB             = DBBase()
    #     #DBConn          = DBB.DBConnection

    #     prevDF_1m = None
    #     prevDF_3m = None
    #     prevDF_5m = None
    #     prev_date = None
    #     start_time       = datetime.now().strftime(Const.Time_Format)
    #     Days_Count       = 0
    #     while current < end_date:
    #         from_date = current.strftime('%Y-%m-%d')
    #         to_date = min(current + timedelta(days=chunk_days), end_date).strftime('%Y-%m-%d')

    #         try:
    #             df = Conn.get_intraday_data(Symbol, 'NSE', 1, start_date=from_date, end_date=to_date)
    #         except Exception as e:
    #             print(f"[ERROR] Failed to fetch data from {from_date} to {to_date} for {Symbol}: {e}")
    #             current += timedelta(days=chunk_days)
    #             time.sleep(2)
    #             continue
            
    #         if df is None:
    #                 print(f"[INFO] No data returned for {Symbol} from {from_date} to {to_date}")
    #                 current += timedelta(days=chunk_days)
    #                 time.sleep(2)
    #                 continue

    #         # Ensure timestamp is datetime
    #         df['timestamp'] = pd.to_datetime(df['timestamp'])

    #         # Group by date
    #         # for date, df1m_day in df.groupby(df['timestamp'].dt.date):
    #         #     df3m_day, df5m_day = self.convert_to_3min_5min(df1m_day)

    #         #     # 1 Minute Data
    #         #     self.ProcessSymbolHistData(prevDF_1m, df1m_day.copy(), Symbol, '1', date)
    #         #     prevDF_1m = df1m_day.copy()

    #         #     # 3 Minute Data
    #         #     self.ProcessSymbolHistData(prevDF_3m, df3m_day.copy(), Symbol, '3', date)
    #         #     prevDF_3m = df3m_day.copy()

    #         #     # 5 Minute Data
    #         #     self.ProcessSymbolHistData(prevDF_5m, df5m_day.copy(), Symbol, '5', date)
    #         #     prevDF_5m = df5m_day.copy()

    #         #     print(f"[OK] Inserted {len(df1m_day)} rows for {Symbol} on {date}")

    #         for date, df1m_day in df.groupby(df['timestamp'].dt.date):
    #             if prev_date is not None and date == prev_date:
    #                 # Already processed this date in previous chunk
    #                 continue

    #             # Convert to 3m and 5m
    #             df3m_day, df5m_day = self.convert_to_3min_5min(df1m_day)

    #             # 1 Minute Data
    #             self.ProcessSymbolHistData(prevDF_1m, df1m_day.copy(), Symbol, '1', date)
    #             prevDF_1m = df1m_day.copy()

    #             # 3 Minute Data
    #             self.ProcessSymbolHistData(prevDF_3m, df3m_day.copy(), Symbol, '3', date)
    #             prevDF_3m = df3m_day.copy()

    #             # 5 Minute Data
    #             self.ProcessSymbolHistData(prevDF_5m, df5m_day.copy(), Symbol, '5', date)
    #             prevDF_5m = df5m_day.copy()

    #             print(f"[OK] Inserted {len(df1m_day)} rows for {Symbol} on {date}")
    #             prev_date = date  # ✅ update last processed date
    #             Days_Count += 1

    #         current += timedelta(days=chunk_days)
    #         time.sleep(2)

    #     end_time       = datetime.now().strftime(Const.Time_Format)
    #     start_dt = datetime.strptime(start_time, Const.Time_Format)
    #     end_dt = datetime.strptime(end_time, Const.Time_Format)
    #     time_taken = end_dt - start_dt

    #     #print("Started: " + str(start_time) + ", Finished: " + str(end_time) + ", Time Taken:, " + str(time_taken) + ", Days: " + str(Days_Count))
    #     print(f"Started: {start_time}, Finished: {end_time}, Time Taken: {time_taken}, Days: {Days_Count}")    
        
    def ProcessSymbolHistData(self, dfPrev, dfCurr, Symbol, Candle, Date):
        #--Add 2 more tables and change 1M table name
        #--Modify Indicator functions, pass BackTest as optional param and do not calc indicators if BackTest=True
        #--Combine 2 days data to get the correct indicator data but store only one day's data
        DBO = DBOps()

        if dfPrev is not None and not dfPrev.empty:
        # Combine previous and current data for accurate indicator calculation
            dfCombined = pd.concat([dfPrev, dfCurr], ignore_index=True)
        else:
            # Use only current data if no previous data available
            dfCombined = dfCurr.copy()

        dfCombined["Date"] = Date
        dfCombined["Symbol"] = Symbol

        # Add indicators to the combined dataframe
        dfCombined = self.AddIndicatorColumns(dfCombined)

        # Extract only the current portion after indicators have been calculated
        dfCurrLen = len(dfCurr)
        dfCurrWithIndicators = dfCombined.iloc[-dfCurrLen:].copy()

        # Store only dfCurr with indicators
        DBO.InsertSymbolHistData(dfCurrWithIndicators, Candle) 
        
    
    def convert_to_3min_5min(self, df):
        """
        Convert 1-minute intraday data into 3-min and 5-min OHLCV format.

        Assumes:
        - Columns are lowercase: 'timestamp', 'open', 'high', 'low', 'close', 'volume'
        - 'timestamp' is already timezone-aware and correct
        - DataFrame is passed directly

        Returns:
        - df_3min: DataFrame resampled to 3-minute
        - df_5min: DataFrame resampled to 5-minute
        """

        # Set timestamp as index if not already
        if df.index.name != 'timestamp':
            df = df.set_index('timestamp')

        # Aggregation logic
        ohlc_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }

        # 3-minute resample
        df_3min = df.resample('3T').agg(ohlc_dict).dropna().reset_index()

        # 5-minute resample
        df_5min = df.resample('5T').agg(ohlc_dict).dropna().reset_index()

        return df_3min, df_5min

    
        #print(df)
        #df.sort_values(by=['col1', ascending=False, 'col2'])

        #Loop the watchlist
            #If both candles are positive or negative, add to the DF
            #Set NEGATIVE/POSITIVE
            #remove (-) sign
            #Add both candle values
        #sort by the total in decending order
        #pick top 5

        #Get Momentum indicators and VWap,BB values for 1 min candle.
        #If touching BBU and Stoch, RSI is reversing then sell 
        #If Total of both candles and diff between current price and upperband is almost similar then buy.
        # return the Dict having symbol and Buy/Sell

    def load_holiday_dates(self, filepath="holidays.txt") -> set:
        holiday_dates = set()
        try:
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        date_str = line.split("#")[0].strip()
                        try:
                            holiday_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                            holiday_dates.add(holiday_date)
                        except ValueError:
                            print(f"⚠️ Skipping invalid holiday format: {line}")
        except FileNotFoundError:
            print(f"⚠️ Holiday file '{filepath}' not found. Proceeding without holidays.")
        return holiday_dates

"""
        body_dict = {}
        tarde_info = {}
        bull_dict = {}
        Bear_dict = {}
        crossover_dict = {}
        #use dataframe instead of dict.
        #Name, Body_Percentage, RSI, Stoch, Volume, Open, high, low

        #Buy - Sensex is positive, Nifty50 is positive, Midcap is positive
        #sort by volume - desc
        #If Volume > SMA
        #IF RSI > 60
        #If Stoch > 70
        #If Stoch > signal
        #If Open > Prev day close
        #If LTP > Open

        #Sell - Else
        #sort by volume - desc
        #IF RSI < 40
        #If Stoch < 30
        #If Stoch < signal
        #If Open < Prev day close
        #If LTP < Open

        df = pd.DataFrame(columns=['SYMBOL','BULLISH','PRICEUP','RSIOVER60','RSIBELOW40','SKDOVERSDD','SKDOVER70', 'VOLOVERSM50', 'BULLISHCROSS', 'BEARISHCROSS', 'SM21OVERSM50'])


        #all_ltp_data   = tsl.get_ltp_data(names = ['NIFTY 17 APR 25400 CALL', 'NIFTY 17 APR 25400 PUT', "ACC", "CIPLA"])
        all_ltp_data   = tsl.get_ltp_data(watchlist_921)

        for name in watchlist_921:
            time.sleep(1)
            print(f"Pre market scanning {name}")
            
            #Chart3 = tsl.get_intraday_data(name, 'NSE', 3)
            #Chart1 = tsl.get_intraday_data(name, 'NSE', 1)
            ChartD = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")

            #RSI
            RSID1 = round(talib.RSI(ChartD['close']).iloc[-1],2)
            RSID2 = round(talib.RSI(ChartD['close']).iloc[-2],2)
            #RSI1 = round(talib.RSI(Chart1['close']).iloc[-1],2)
            #RSI3 = round(talib.RSI(chart1['close']).iloc[-1],2)

            #Stochastics
            #SK1, SD1 = talib.STOCH(Chart1['high'].to_numpy(), Chart1['low'].to_numpy(),Chart1['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
            #SK3, SD3 = talib.STOCH(Chart3['high'].to_numpy(), Chart3['low'].to_numpy(),Chart3['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
            SKD1, SDD1 = talib.STOCH(ChartD['high'].to_numpy(), ChartD['low'].to_numpy(),ChartD['close'].to_numpy(), 5, 3, 0, 3, 0)[-1]
            SKD2, SDD2 = talib.STOCH(ChartD['high'].to_numpy(), ChartD['low'].to_numpy(),ChartD['close'].to_numpy(), 5, 3, 0, 3, 0)[-2]
            #check iloc of daily data and other charts. verify the location data i.e. [-1] [0]
            #verify all data 

            #Daily analysis
            PDC_Price       = ChartD.iloc[-1]['close']  #Previous day close
            TO_Price        = all_ltp_data[name]     #Today open
            PDV             = ChartD.iloc[-1]['volume']  #Previous day volume
            PDSM50          = talib.SMA(ChartD['volume'].to_numpy(), 50) #Previous day SM50
            #PDSM21          = talib.SMA(ChartD['volume'].to_numpy(), 21) #Previous day SM21
            PD_LastCD          = ChartD.iloc[-1]  #last_candle daily
            PD_body_percentage = ((PD_LastCD['close'] - PD_LastCD['open'])/PD_LastCD['open'])*100
            price_change    = (TO_Price-PDC_Price)/PDC_Price
            #3M analysis



            #daily_thi = daily_data.iloc[0]['high']
            #now_sma = talib.SMA(Chart1['volume'].to_numpy())
            #now_vol = Chart1[-1]['volume']
            #now_ltp = Chart1[0]['close']
            ##ldc = chart3.iloc[-1]  #last_candle
            #body_percentage = ((ldc['close'] - ldc['open'])/ldc['open'])*100
            body_dict[name] = round(PD_body_percentage, 2)

            #if TO_Price > PDC_Price and RSID1 > RSID2 and RSID1 > 60 and SKD2 < SDD2 and SKD1 > SDD1 and SKD1 > 70 and PDV > PDSM50:
            #    print("crossover")
            #    crossover_dict[name] = price_change
            
            if TO_Price > PDC_Price and RSID1 > 60 and SKD1 > SDD1 and SKD1 > 70 and PDV > PDSM50:
                #bullish
                print("bullish")

                bull_dict[name] = price_change
            elif TO_Price < PDC_Price and RSID1 < 40 and SKD1 < SDD1 and SKD1 < 30 and PDV < PDSM50:
                #bearish
                print("bearish")
                Bear_dict[name] = price_change
            #daily_data = tsl.get_historical_data(tradingsymbol = name, exchange = 'NSE',timeframe="DAY")
            


        
        sorted_by_values = dict(sorted(body_dict.items(), key=lambda item: item[1]))
        script_having_max_body = max(body_dict, key=body_dict.get)
        script_having_min_body = min(body_dict, key=body_dict.get)
        daily_data = tsl.get_historical_data(tradingsymbol = script_having_max_body, exchange = 'NSE',timeframe="DAY")
        ldc = daily_data.iloc[-1]  #last_day_candle
        tarde_info = {"Direction":"buy", "level":ldc['high']}


        print(script_having_max_body)
        print(tarde_info)

    
    
    def Downward_Stoch_Crossover(self, chart):
        print("down")

    def Upward_Stoch_Crossover(self, chart):
        print("up")

    def Downward_MA21_Crossover_MA50 (self, chart):
        print("down")

    def Upard_MA21_Crossover_MA50 (self, chart):
        print("up")

    def Downward_BBand_Reversal (self, chart):
        print("down")

    def Upward_BBand_Reversal (self, chart):
        print("Up")

    def BBandShape (self, chart):
        print("Wide")

    def CPRShape (self, DailyChart):
        print("narrow")

    def Downward_MA14_Crossover_MA21 (self, chart):
        print("down")

    def Upard_MA14_Crossover_MA21 (self, chart):
        print("up")

    def RSI_Crossover (self, chart):
        print("up") 
    
    def RSIDivergence(self, chart):
        print("done")

        """