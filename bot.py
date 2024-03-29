import ccxt
import pandas as pd
pd.set_option('display.max_rows', None)
import warnings
warnings.filterwarnings('ignore')
import datetime

import secret
import supertrend as indicators

ASSET_NAME = 'BTC-PERP'
TIMEFRAME = '5m'
FETCHING_LIMIT = 1500
TRADE_SIZE = 0.0004 

exchange = ccxt.ftx({
    "apiKey": secret.PUBLIC_KEY,
    "secret": secret.SECRET_KEY
})

def in_position():
    for position in exchange.fetchPositions():
        if float(position['info']['size']) > 0:
            return True
    return False

def execute(df):
    in_uptrend = df['in_uptrend'][len(df['in_uptrend']) - 1]
    curr_datetime = str(df['timestamp'][len(df['timestamp']) - 1])
    curr_close = df['close'][len(df['close']) - 1]

    if not in_position() and in_uptrend:
        exchange.createOrder(ASSET_NAME, 'market', 'buy', TRADE_SIZE)
        print(curr_datetime + ', ' + ASSET_NAME + ' bought at price ' + str(curr_close) + '\n')
    elif in_position() and not in_uptrend:
        exchange.createOrder(ASSET_NAME, 'market', 'sell', TRADE_SIZE)
        print(curr_datetime + ', ' + ASSET_NAME + ' sold at price ' + str(curr_close) + '\n' + '\n')

def run():
    bars = exchange.fetch_ohlcv(ASSET_NAME, timeframe=TIMEFRAME, limit=FETCHING_LIMIT)
    
    df = pd.DataFrame(bars[:], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df = indicators.supertrend(df)

    execute(df)

run()
