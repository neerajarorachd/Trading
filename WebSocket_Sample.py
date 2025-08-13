import websockets
import json

# Replace with your credentials and instrument
TOKEN = "YOUR_ACCESS_TOKEN"
CLIENT_ID = "YOUR_CLIENT_ID"
INSTRUMENT_ID = "NSE_EQ|INE848E01016"  # Example: TCS NSE instrument ID

def on_message(ws, message):
    data = json.loads(message)

    if 'data' in data:
        instrument_data = data['data']

        print("\n--- Market Depth Update ---")
        print(f"Instrument: {instrument_data.get('instrument', 'N/A')}")

        # Parse and print bid (buy) levels
        bids = instrument_data.get('bids', [])
        print("\nTop 5 Bids:")
        for level, bid in enumerate(bids[:5], start=1):
            print(f"  Level {level}: Price = {bid['price']}, Quantity = {bid['quantity']}")

        # Parse and print ask (sell) levels
        asks = instrument_data.get('asks', [])
        print("\nTop 5 Asks:")
        for level, ask in enumerate(asks[:5], start=1):
            print(f"  Level {level}: Price = {ask['price']}, Quantity = {ask['quantity']}")

        
        # Calculate total bid and ask quantities
        total_bid_qty = sum(bid['quantity'] for bid in bids)
        total_ask_qty = sum(ask['quantity'] for ask in asks)

        if total_bid_qty + total_ask_qty > 0:
            bid_percentage = (total_bid_qty / (total_bid_qty + total_ask_qty)) * 100
            ask_percentage = (total_ask_qty / (total_bid_qty + total_ask_qty)) * 100

            print(f"\nBid Volume: {total_bid_qty} | Ask Volume: {total_ask_qty}")
            print(f"Bid %: {bid_percentage:.2f}% | Ask %: {ask_percentage:.2f}%")
    else:
        print("Received non-depth message:", data)

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")

    # Subscribe to depth data for the instrument
    subscribe_payload = {
        "action": "subscribe",
        "params": {
            "mode": "depth",
            "instruments": [INSTRUMENT_ID]
        }
    }
    ws.send(json.dumps(subscribe_payload))

# Construct WebSocket URL
url = f"wss://streamapi.dhan.co/marketdata?client_id={CLIENT_ID}&token={TOKEN}"

# Create and run WebSocket app
ws = websockets.WebSocketApp(
    url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()

