# Login (return Dhan object)
# Order dictionary
# Bolinger status dictionary
# 

import pandas as pd
from LibEnum import TradingEnums as TE
from enum import Enum
from datetime import datetime
# import psutil
# import subprocess
# import os

class GeneicLib:
    #Watchlist_copy = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC', 'BPCL', 'WIPRO', 'SHRIRAMFIN', 'ADANIPORTS', 'JSWSTEEL', 'COALINDIA', 'ULTRACEMCO', 'BAJAJ-AUTO', 'LT', 'POWERGRID', 'ADANIENT', 'SBIN', 'HCLTECH', 'TCS', 'EICHERMOT', 'BAJAJFINSV', 'TECHM', 'LTIM', 'HINDUNILVR', 'BHARTIARTL', 'AXISBANK', 'GRASIM', 'HEROMOTOCO', 'DRREDDY', 'ICICIBANK', 'HDFCBANK', 'BAJFINANCE', 'SBILIFE', 'RELIANCE', 'KOTAKBANK', 'ITC', 'TITAN', 'SUNPHARMA', 'INDUSINDBK', 'APOLLOHOSP', 'BRITANNIA', 'NESTLEIND', 'HDFCLIFE', 'DIVISLAB', 'CIPLA', 'ASIANPAINT', 'TATACONSUM']
    Watchlist_copy = ['INFY', 'M&M', 'HINDALCO', 'TATASTEEL', 'NTPC', 'MARUTI', 'TATAMOTORS', 'ONGC']
    Watchlist_921 = ['IGL', 'HINDCOPPER', 'PARACABLES', 'STLTECH', 'NATIONALUM', 'BHEL', 'BANKBARODA', 'ONGC', 'MANAPPURAM', 'JIOFIN', 'IOC', 'NETWORK18', 'WELSPUNLIV', 'GMRAIRPORT','TVSSCS', 'DEN', 'IDFCFIRSTB', 'IDBI', 'UJJIVANSFB', 'SHRIRAMPPS', 'DELTACORP', 'RTNINDIA', 'PATELENG', 'JTLIND', 'SAMMAANCAP', 'DHANI', 'EDELWEISS', 'DCBBANK', 'RBA', 'SDBL']


    def GetWatchlist(self,WLType):
        if WLType == TE.Watchlist_Type.P50TO250:
            return GeneicLib.Watchlist_921
        elif WLType == TE.Watchlist_Type.SENSEX:
            return GeneicLib.Watchlist_copy
        
    def GetTimeDiff(StringStartTime, StringEndTime, ReturnSeconds=False):
        start_time  = datetime.strptime(StringStartTime, "%H:%M:%S")
        end_time    = datetime.strptime(StringEndTime, "%H:%M:%S")

        # Calculate the difference
        time_diff = end_time - start_time  # This is a timedelta object

        # Convert timedelta to total seconds
        total_seconds = int(time_diff.total_seconds())

        # Convert total seconds to HH:MM:SS format
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Format the result
        if ReturnSeconds:
            return total_seconds
        else:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
    



    # def is_script_running(script_name):
    #     """Check if a script with the given name is already running."""
    #     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    #         try:
    #             if not proc.info['cmdline'] == None:
    #                 if script_name in proc.info['cmdline']:
    #                     return True
    #         except (psutil.NoSuchProcess, psutil.AccessDenied):
    #             continue
    #     return False

    # def run_script_if_not_running(script_path):
    #     script_name = os.path.basename(script_path)
        
    #     if not GeneicLib.is_script_running(script_name):
    #         print(f"Starting script: {script_name}")
    #         subprocess.Popen(['python', script_path])
    #     else:
    #         print(f"Script already running: {script_name}")


    def GetFilePath(file_name):
        from pathlib import Path

        # Absolute path of the current script
        file_path = Path(file_name).resolve()
        #file_path = Path(file_name).resolve().parent #for directory path
        #script_path = Path(__file__).resolve()
        return file_path




            