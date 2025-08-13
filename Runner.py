import subprocess
import time
from datetime import datetime
from LibConstants import Const

ST_921_927      =   subprocess.Popen(["python", "ST_921_927.py"])
ST_930_1130     =   subprocess.Popen(["python", "ST_930_1130.py"])
#ST_930_1130_Rev =   subprocess.Popen(["python", "ST_930_1130_Rev.py"])
Trade_Monitor   =   subprocess.Popen(["python", "Monitor_Trades_Master.py"])

# Optionally wait for finish
ST_921_927.wait()
print("ST_921_927 finished at: " + str(datetime.now().strftime(Const.Time_Format)))
#ST_930_1130_Rev.wait()
#print("ST_930_1130_Rev finished at: " + str(datetime.now().strftime(Const.Time_Format)))
ST_930_1130.wait()
print("ST_930_1130 finished at: " + str(datetime.now().strftime(Const.Time_Format)))
Trade_Monitor.wait()
print("Trade_Monitor finished at: " + str(datetime.now().strftime(Const.Time_Format)))