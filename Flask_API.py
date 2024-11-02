from flask import Flask, jsonify
import pandas as pd
from binance.spot import Spot as spot_Client

# url to access binance api
base_url = "https://api.binance.us"

app = Flask(__name__)


def data(coin,frame,limit):
  # create Client to access API
  spot_client = spot_Client(base_url=base_url)
  # Access historical prices
  data = spot_client.klines(coin, frame, limit=limit)
  #display(btcusd_history[:2])

  # show as DataFrame
  columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time', 'Quote_V', 'Trades_Count',
          'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

  dff = pd.DataFrame(data, columns=columns)
  dff['time_ms'] = dff['Date']
  dff['Date'] = pd.to_datetime(dff['Date'], unit='ms')
  df = dff.loc[:, ['time_ms','Open','High','Low','Close','Trades_Count','Quote_V','Volume']].copy()
  df = df.set_index(dff['Date'])

  df = df.loc[:,['Open','High','Low','Close','Quote_V','Trades_Count']]
  df["Open"] = pd.to_numeric(df["Open"])
  df['Close'] = pd.to_numeric(df["Close"])
  df ["High"] = pd.to_numeric(df["High"])
  df["Low"] = pd.to_numeric(df["Low"])
  df["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
  df["Quote_V"] = pd.to_numeric(df["Quote_V"])

  df = df.loc[:,['Open','High','Low','Close','Quote_V','Trades_Count']]

  return df



# Retrieve all entries
@app.route('/', methods=['GET'])
def get_entries():
    #df = data('BTCUSDT','1m',limit=4)
    #df['V1'] = df['Quote_V'].shift(2)
    #df['V2'] = df['Quote_V'].shift(1)
    #df['V_acc'] = df['V2'].div(df['V1'])

    # Sample data
    entries =[
    {
        "pair": "BTCUSDT",
        "pump_by": "Pump By: 2",
        "trade_count1": "Trade Count: 10",
        "trade_count2": "Trade Count: 20"
    },
    {
        "pair": "ETHUSDT",
        "pump_by": "Pump By: 1.5",
        "trade_count1": "Trade Count: 15",
        "trade_count2": "Trade Count: 25"
    },
    {
        "pair": "SOLUSDT",
        "pump_by": "Pump By: 3",
        "trade_count1": "Trade Count: 30",
        "trade_count2": "Trade Count: 90"
    }
]

    return jsonify(entries)

if __name__ == '__main__':
    app.run(debug=True)


