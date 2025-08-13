
from Dhan_Tradehull import Tradehull
import pandas as pd
from pprint import pprint
import talib
from LibFinance import FinLib
from LibAnalysis import AnaLysisLib


str_Client_Code =   "1106451789"
str_Token_ID    =   "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ2ODUyNjg2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.tyAOEhC8dQtoQUhCabZdPIfhOa72w-heAVXLld79myY5W97-ai-xeq2Y94tc_OIFMflv-F8k76Hu4tMH9OpZbQ"
tsl             =   Tradehull(str_Client_Code,str_Token_ID)
FLib = FinLib()
ALib = AnaLysisLib()

#print script start time



chart = tsl.get_intraday_data('INFY', 'NSE', 5)
ALib.Get_Momentum_Data(chart, tsl)
# strRSI = ALib.GetRSI(chart)
# print(str(strRSI))
# sDirection = ALib.GetRSI_5C_Direction(chart)
# print(str(sDirection))
# sStoch = ALib.GetStochastics_5C_Direction(chart)
# print(str(sStoch))


