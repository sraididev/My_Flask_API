from flask import Flask, jsonify
import requests
import time
from coins import coins

app = Flask(__name__)

# Predefined parameters
SYMBOLS = coins #["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # Add more symbols as needed
INTERVAL = "15m"  # Kline interval (e.g., 3 minutes)
FACTOR_THRESHOLD = 1.5  # Factor threshold to determine significant change
LIMIT = 2  # Fixed limit to get the last 2 data points

# Binance API endpoint for Klines
BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

@app.route('/coins')
def home():
    return jsonify({"message": "Hello, World!","Coins":coins})

# API route to check predefined candle factors
@app.route('/start', methods=['GET'])
def check_candle_factors():
    coins_list = []

    for symbol in SYMBOLS[:50]:  # Limit to the first 50 symbols if needed
        params = {
            "symbol": symbol,
            "interval": INTERVAL,
            "limit": LIMIT
        }
        
        try:
            # Make a request to the Binance API
            response = requests.get(BINANCE_API_URL, params=params)
            data = response.json()
            
            # Volume candles
            candle1_volume = float(data[0][5])
            candle2_volume = float(data[1][5])
            
            # Calculate Factor and check threshold
            if candle1_volume != 0:
                factor = candle2_volume / candle1_volume
                if factor >= FACTOR_THRESHOLD:
                    coins_list.append({
                                    "pair": f"{symbol}",
                                    "pump_by": f"Pump By: {round(factor,2)}",
                                    "trade_count1": f"Trade Count: {int(candle1_volume)}",
                                    "trade_count2": f"Trade Count: {int(candle2_volume)}"
                    })
        except Exception as e:
            print(f"Error with symbol {symbol}: {e}")
            continue

        time.sleep(0.02)  # To avoid hitting rate limits
    
    return jsonify(coins_list)

if __name__ == '__main__':
    app.run(debug=True)
