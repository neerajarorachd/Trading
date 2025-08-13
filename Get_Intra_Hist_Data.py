from LibAnalysis import AnaLysisLib
from LibDhan import Dhan
import pandas as pd
from datetime import datetime

ALib = AnaLysisLib()
DH = Dhan()
Conn = DH.DhanConnection
Chart = pd.DataFrame()

#Symbol = 'NALCO'
Symbol = 'ASHOKLEY'
#Symbol = 'HINDCOPPER'
#Symbol = 'NALCO'
Chart = ALib.Get_Intraday_Historical_Data(Conn, Symbol, 12)
#Chart.to_csv("NALCO_intraday.csv", index=False)

#Chart['Symbol'] = Symbol

# Step 3: Add 'Date' column extracted from the 'timestamp' column
# Make sure 'timestamp' column is in datetime format
#Chart['Date'] = pd.to_datetime(Chart['timestamp']).dt.date

# Define the path and filename
# path = r"D:\AI Trading\Data"
# filename = f"NALCO_intraday_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
# full_path = f"{path}\\{filename}"

# Save the DataFrame to CSV
#Chart.to_csv(full_path, index=False)
