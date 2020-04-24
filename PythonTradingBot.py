import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import threading
import time
import datetime
import logging
import argparse
# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS
#region
API_KEY = "ALPACA API KEY HERE"
API_SECRET = "ALPACA API SECRET HERE"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
#endregion
#Buy a stock when a doji candle forms
class BuyDoji:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
  def run(self):
        #On Each Minute
        async def on_minute(conn, channel, bar):
            symbol = bar.symbol
            print("Close: ", bar.close)
            print("Open: ", bar.open)
            print("Low: ", bar.low)
            print(symbol)
            #Check for Doji
            if bar.close > bar.open and bar.open - bar.low > 0.1:
                print('Buying on Doji!')
                self.alpaca.submit_order(symbol,1,'buy','market','day')
            #TODO : Take profit

        #Connect to get streaming market data
        conn = StreamConn('Polygon Key Here', 'Polygon Key Here', 'wss://alpaca.socket.polygon.io/stocks')
        on_minute = conn.on(r'AM$')(on_minute)
        # Subscribe to Microsoft Stock
        conn.run(['AM.MSFT'])
# Run the BuyDoji class
ls = BuyDoji()
ls.run()
