import requests

# Replace with your actual access token
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

# Payload for Super Order (Bracket Order)
order_data = {
    "symbol": "RELIANCE",
    "exchangeSegment": "NSE_EQ",
    "transactionType": "BUY",
    "orderType": "LIMIT",
    "quantity": 1,
    "price": 2500.0,
    "productType": "INTRADAY",
    "afterMarketOrder": False,
    "validity": "DAY",
    "disclosedQuantity": 0,
    "orderTag": "MySuperOrder",

    # Bracket order-specific fields
    "stopLoss": 20.0,      # Stop loss in points
    "takeProfit": 40.0,    # Target in points
    "trailingStopLoss": 0.0
}

response = requests.post("https://api.dhan.co/super-order", json=order_data, headers=headers)

print("Status:", response.status_code)
print("Response:", response.json())


""" {
  "status": "success",
  "data": {
    "orderId": "1234567890",              // Entry order
    "bracketOrders": {
      "targetOrderId": "1234567890T",     // Target leg
      "stopLossOrderId": "1234567890S"    // Stop loss leg
    }
  }
} 

response_data = response.json()

entry_order_id = response_data["data"]["orderId"]
target_order_id = response_data["data"]["bracketOrders"]["targetOrderId"]
stop_loss_order_id = response_data["data"]["bracketOrders"]["stopLossOrderId"]

print("Entry Order ID:", entry_order_id)
print("Target Order ID:", target_order_id)
print("Stop Loss Order ID:", stop_loss_order_id)


order_id = "1234567890"
response = requests.get(f"https://api.dhan.co/orders/{order_id}", headers=headers)
print(response.json())

Success

{
    "status": "success",
    "message": "Order placed successfully",
    "data": {
        "orderId": "230501000123456",         # Entry order ID
        "bracketOrders": {
            "targetOrderId": "230501000123456T",   # Target order ID
            "stopLossOrderId": "230501000123456S"  # Stop loss order ID
        }
    }
}


Failure

{
    "status": "error",
    "message": "Invalid price or insufficient margin",
    "errors": [
        {
            "code": "ORDER_VALIDATION_FAILED",
            "description": "Stop loss is too close to market price"
        }
    ]
}



"""