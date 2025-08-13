"""  
Tasks for V1.1
--------
Must Have
---------
BackTest
---------
Should be a function of base class
Call Strategy() method of the strategy
Get the list of dates from the database for the available data
Run a loop for the day wise data
scan the data for row by row
Configurable Start row. RSI - 14, (BB, SMA-21, MACD) - 21, SMA50-50, Other options i.e. 3, 5 etc
Split the DF into 2 parts. First, upto the current row, Second, current row+1 to end
First part for the call decision. send it to the RSI and BB methods. Get the call and prices.
If its pass, Continue the loop, if its lead, send it to lead method and check if it was fruitful.
If its sell or buy, call the method to analyse result.

Analysis of Result
------------------
Second part for the result analysis. Check if (Low < SL < High) or (Low < Target < High), break. 
Calculate the expenses, Gross Profit, Net Profit, Distance from the order candle (number of candles), Start Time, End Time, Time Taken
Store the Success/Failure and calculated data against the DF row.

Scan next row and repeat the process till 3'o clock (configurable)

Reporting
---------
Once the process is done, color code the drives. First pick the first row where first order was placed.
    Set colorcode, say green=1. find the candle, where the order was closed. Add idle period, (default 5, configurable) and find the next order candle.
    Once reaches the end of the data, find the next order (after the first order) and scan till end, mark color code.
    Print path for the order sequences. Count the number of probable orders. Start Time, Number of orders, Success/Failure count.

Report 1: Can use Excel
    Daywise count of Orders, Failure, Success, Expected profit/Loss range as per the different execution paths. Show Green or Red

Report 2: Prediction of the best time for the trade.

Report 3: Compare the results for different SL, Target Percentages (First run manually with different SL/Targets, later automate it)
    It could be a percentage + time also.

Report 4: Volume comparison. As per the volume, judge when the whole lot will be traded.

Report 5: Comparison of Strategies against the stock symbol and suggest the best suitable strategy.

Report 6: Sector wise analysis. Testing the strategy on multiple stocks back to back. 
----------------------------------------------------------------------------------------
Stages:
----------------------------------------------------------------------------------------
Stage 1:
Write function to scan row by row, split the DF, Get the calls, Mark Results, show day wise count, result (as per the configured number of shares) 
Show the paths: start time, Number of orders, results. - 2 weeks

Stage 2:
Rearchitecture as per the architecture changes and incorporate BackTest functionality. - 4 weeks

Stage 3:
Reporting, combination of strategies, Comparison of strategies. - 8 weeks







----------------------------------------------------------------------------------------



----------------------
Architectural Changes
----------------------
Single Enter function in Base Class
Call Strategy's Strategy method in Enter
Strategy method should set/return 5 mendatory elements, Call, SL, Target, SLPerc, TargetPerc in DL, along with the StrategyData
There should be a StoreStrategyData function in Strategy. Should be called from Enter() after the order has been placed. Pass StrategyData to this function.
BBCall should be an optional part of Enter() function. Min time. 1 Min: 9:15+21=9:36, 3 min: 9:15+63=10:18, 5 Min: 9:15+105=11:00

-----------------------------------------------------------------------------------------




At the trading end time (should be 2-2:30 max), check if there is any open position. Close all positions.
Try using multiple api keys. See if it bypass '
New Field: Strategy_Order_End_Time In Enter function, Order will be placed between Strategy_Start_Time and Order_End_Time instead of Strategy_End_Time
           This way the active orders will not be closed pre-mature.
Install PandasAI and other tool to prompt queries
Check Indicators before creating an order


Get Chart also from DL1M/DL3M/DL5M, pass param to get the chart type
def DecideDirection(Chart, DL)
    Low, High of the day - get it from describe
    Low High of last 5 candles - get it from describe
    Call BB - get three points, VVAP
    Trend of the last 5 bars - Create a function, pass chart
    Other RSI Indicators 
    Pass if narrow gap between VVAP and BBT/BBB at least .5% Movement - .1 (Exp)+.1-.4
    return Buy/Sell/Pass

    OBBT, BBT, P90, P75, P50, P25, P10, BBM, M90, M75, M50, M25, M10, BBB, BBBB 
    OBBT - Over
    BBT - On BBT
    BBBB - Below 
    P90 - Plus (Above BBM)
    M90 - Minus (Below BBM)

    VVAP-BBM - Over, On(10% +-), Below
    VVAP-Close - 

    Check the sticky trend (sticking with VWAP/BBU/BBB/SM21/SM50)
    if sticked

    UpdatedTargetPrice = BBPrice + (LastTargetPrice - BBPice) #If target is below BBLine then -Diff will be added otherwise + Diff will be added

    Store BB records in DB 
        Add TargetBB, SLBB, TargetBBLastPrice, SLBBLastPrice, TargetLastPrice, SLLastPrice in GetACall function
    Update BB records on sticky  
    Get BB Records from DB

    Write Exit function for Sticky
        If Current BB is different from last BB:
            Get new Target and SL Price
            Modify Target and SL Orders
            Update BB data in DB
    -----------------------------------


    -----------------------------------



    -----------------------------------


def Monitor()
    if stock is moving towards desired direction, increase SL and Target as per the movement keeping within the BB limit
    Keep an eye on SK and RSI

def WhichLineIsBeingFollowed
    MA21/MA50/VVAP

import pandas as pd

def detect_5_candle_trend(df, price_col='Close', threshold=0.002):
    """
#    Detect 5-candle trend: 'Up', 'Down', or 'Sideways'
    
#    Args:
#        df: pandas DataFrame with OHLCV data
#        price_col: column to evaluate trend (default: 'Close')
#        threshold: min % change to ignore sideways noise (default: 0.2%)
        
#    Returns:
#        df with a new column 'Trend5'
"""
    trends = []

    for i in range(len(df)):
        if i < 4:
            trends.append(None)
            continue

        window = df[price_col].iloc[i-4:i+1]
        start = window.iloc[0]
        end = window.iloc[-1]
        pct_change = (end - start) / start

        if pct_change > threshold:
            trends.append("Up")
        elif pct_change < -threshold:
            trends.append("Down")
        else:
            trends.append("Sideways")

    df['Trend5'] = trends
    return df

    

    import pandas as pd

def detect_5_candle_trend_body(df, threshold=0.001):
    """
#    Detects trend based on candle body (Open vs Close) over last 5 candles.
    
#    Args:
#        df: DataFrame with 'Open' and 'Close' columns
#        threshold: minimum relative body size to consider a candle directional
    
#    Returns:
#        df with a new column 'Trend5'
"""
    trends = []

    for i in range(len(df)):
        if i < 4:
            trends.append(None)
            continue

        bullish = bearish = neutral = 0

        for j in range(i-4, i+1):
            o = df.at[j, 'Open']
            c = df.at[j, 'Close']
            if abs(c - o) / max(o, 1e-9) < threshold:
                neutral += 1
            elif c > o:
                bullish += 1
            else:
                bearish += 1

        if bullish >= 3:
            trends.append("Up")
        elif bearish >= 3:
            trends.append("Down")
        else:
            trends.append("Sideways")

    df['Trend5'] = trends
    return df


Implement Comment column: store the indicators we are using for the order decision


Should Have
------------

Good to have (May be for V1.1)
Create Test connections for MySQL and SQLServer
Write DDL scripts and Data transfer scripts



Steps to add a new strategy
---------------------------
Add new Strategies class, pass new strategy Enum to super constructor 
    super().__init__(TE.Strategy.Morning_930_1130_Rev)
Copy/Ceate ST_ file, Refer new class

Copy/Create Monitor file, Refer new class
Add Enum

Add new strategy record
Enter and Exit functions if not a timebound strategy



Phase 1
------------
Get 921 Direction
Get Best moving stock from list
Create SL Order at 9:21 as per the direction
Close the position at 9:24

Phase 2
-----------------------
Position Dictionary (Order Type (Buy/Sell), Exchange, Stock Type [Stock/Nifty Options/Crude Oil Options], [Call Type][CE/PE], Symbol, Order Start, Order Finish, Order ID, Order Price, SL order ID, SL Price, Target Order ID, Target Price, Order Strategy [921/Bolinger etc], Closing Type [Time Finished, SL Hit, Target Hit, Cancelled, Squared Off], Order Status, In Qty, Out Qty, Balance Qty)
Qty mgmt: 

9:30-9:45 call
Get Volume, Depth, RSI and other indicators
Get the direction for 9:30
choose the best moving stock
keep on trailing the SL until Stochastics reach at reversal
Check indexes. Which Indexes are in momentum. Get Historical data of relavant stocks.
first check current position, then where it can go up and what is support level.
Also find the way to get Asks and Offers - get it through WebSocket

Types of Orders:
1. Fresh Order - Order + SLOrder + TargetOrder
2. Opposite order in case of timeout (closing order) will be update order, not the create order

Implement multiple trade at a time 

DL["ENumType"]
DL["ENumTypeID"]
DL["ENumTypeName"]

Separate Script for continous trading. Morning921 should be restricticted to one time trade. another script for continous trade with reverse trading.
Continous trading until Max loss/MaxProfit/Endtime-15min doesn't hit
Oder mgmt in DB
Monitoring through DB
Monitoring from a different script
Monitor until Starategy Endtime doesn't hit
Add Reverse = True or False in DB for reversal orders. i.e. If Two Sisters is bullish create a sale order instead of buy order. Analyse it later against
 time, Index price, size of candles, symbol, and other indicators

Phase 3
------------
Bought [IN] 100, sold [OUT] 100, Balance 0 
Sold [IN] 100, Bought [OUT] 50, Balance 50

TradeStatusOnPnL - Success/Failure/NoLossNoProfit/ModerateSuccess/ModerateFailure
===========================
Order Dictionary
Create SL Target Order (Target=Buy price + buy sell expenses + profit margin)
Cancel Target order if position has been closed or SL has been hit
Get Volume 
If volume is still high, trail SL at 9:24 
keep a watch on volume but close the position max by 9:27

If we have an order near BB Bot and price have crossed VWAP there there are chances that price will remain between VWAP and upper band. 
Set the stop loss at VWAP-.0005% (10-12 p) because if it will come down below VWAP, it will touch the bottom band.
Similarly. keep on moving the target along with the BB Upper band. Upperband - .0005% (10-12 p).
Later when we implement reversal breakout technique, we will keep a watch for reversal. Still better to sell 50% of stocks at a profit.
Today what happened that, Stop loss and Exit time executed at the same time and a new order got created in opposite direction :).
So, after loop exits, we should check where there is any open position or pending order.

Phase 4
-----------------------
Implement Finance features

Phase 5
-----------------------
Implement Bolinger Band

Phase 6
-----------------------

Implement multiple trade back to back
(Keep on checking for the available funds. Once a position is closed, cancel target order. Add a new row for active trade.)
After First drive of automation, we will implement advanced DB structure for Order management
OrderMaster Table, Orders Table having Traded orders, SL Orders and Target Orders
Multiple SL and Target orders for Parent order.
Adding more stock, selling partial order

While ordering, Also store indicator positions for machine learning








"""