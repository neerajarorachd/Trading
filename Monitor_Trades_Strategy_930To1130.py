from LibDBBase import DBBase
import sys
import json
import pandas as pd
from ClassStrategies import Strategy930To1130
from LibDhan import Dhan

DH              = Dhan()
tsl             =   DH.DhanConnection
ST930To1130           =   Strategy930To1130()

def main():
    # Get the dictionary from the first argument
    input_json = sys.argv[1]
    Watchlist = pd.read_json(input_json)  #pd.DataFrame(input_json) #json.loads(input_json)
    
    #ST921.exit_921_927(Watchlist)
    ST930To1130.Exit(Watchlist, tsl)
    

if __name__ == "__main__":
    print("Entered into 921 monitor")
    main()
    print("exit from 921 monitor")



