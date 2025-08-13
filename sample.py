from dhanhq import dhanhq
import pandas as pd

client_id = "1106451789"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ2ODUyNjg2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjQ1MTc4OSJ9.tyAOEhC8dQtoQUhCabZdPIfhOa72w-heAVXLld79myY5W97-ai-xeq2Y94tc_OIFMflv-F8k76Hu4tMH9OpZbQ"

dhan = dhanhq(client_id, access_token)

def getHoldings (dhan):
    data = dhan.get_positions()
    df = pd.DataFrame(data['data'])
    df.to_csv('holdings.csv')
    print(df)

def placeOrder(symbol):
    dhan.place_order(security_id='1333',            # HDFC Bank
    exchange_segment=dhan.NSE,
    transaction_type=dhan.BUY,
    quantity=10,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)

def getOrderList():
    data=dhan.get_order_list()
    df = pd.DataFrame(data['data'])
    print(data)

getHoldings(dhan)
#placeOrder("HDFCBANK")
#getOrderList()


