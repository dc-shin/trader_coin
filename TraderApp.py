from operator import index
from BaseTrader import SubscribeType
from DatabaseManager import DatabaseManager
from UpbitTrader import UpbitTrader
from datetime import datetime
import pandas as pd

def main():
    print('######## Trader app started ########')

    # UpbitTrader.instance().subscribe(SubscribeType.Ticker)
    # UpbitTrader.instance().subscribe(SubscribeType.Trade)
    # UpbitTrader.instance().subscribe(SubscribeType.Orderbook)

    # account = UpbitTrader.instance().request_account()

    # print(type(account))
    # print(account)

    # yyyy-MM-dd HH:mm:ss
    # to_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(to_time)
    # candles = UpbitTrader.instance().request_candles_min(1, to_time, count=2)

    # DatabaseManager.instance().insert('candle', candles)

    temp = DatabaseManager.instance().select('candle', index_col_name='candle_date_time_utc_timestamp')
    print(temp)

if __name__ == '__main__':
	main()
