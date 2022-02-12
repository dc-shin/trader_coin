from Singleton import Singleton
from DatabaseManager import *
from UpbitTrader import UpbitTrader
from datetime import timezone, datetime
import time

class Collector(Singleton):
    def collect_all_candle(self, min, end_time):
        print('[Collector] Start collect all candle. min: {}, end_time: {}'.format(min, end_time))
        
        table_name = 'candle'
        recent_df = DatabaseManager.instance().select(table_name, 1, 'candle_date_time_utc_timestamp', OrderType.DESC, 'candle_date_time_utc_timestamp')
        old_df = DatabaseManager.instance().select(table_name, 1, 'candle_date_time_utc_timestamp', OrderType.ASC, 'candle_date_time_utc_timestamp')
        start_time_queue = []
        end_time_queue = []
        current_time = datetime.utcnow().timestamp()
        recent_time = 0.0 if recent_df.empty else recent_df.index.values.astype(float)[0]
        old_time = 0.0 if old_df.empty else old_df.index.values.astype(float)[0]
        
        if recent_df.empty or old_df.empty or (recent_time == old_time):
            # 현재부터 end_time까지 저장
            start_time_queue.append(current_time)
            end_time_queue.append(end_time)
        elif old_time <= end_time: # 이전에 end_time까지 데이터를 저장함
            # 현재부터 최근 데이터까지 가져오기
            start_time_queue.append(current_time)
            end_time_queue.append(recent_time)
        else:
            # 현재부터 최근 데이터까지, 오래된 데이터부터 end_time까지 저장
            start_time_queue.append(current_time)
            end_time_queue.append(recent_time)
            start_time_queue.append(old_time)
            end_time_queue.append(end_time)
        
        if len(start_time_queue) != len(end_time_queue):
            print('[Collector] Invalid time queue')
            return

        while start_time_queue and end_time_queue:
            time_format = '%Y-%m-%d %H:%M:%S'
            req_start_time = start_time_queue.pop(0)
            str_req_start_time = datetime.fromtimestamp(req_start_time, timezone.utc).strftime(time_format)
            str_req_start_time_kts = datetime.fromtimestamp(req_start_time).strftime(time_format)

            req_end_time = end_time_queue.pop(0)
            str_req_end_time_kts = datetime.fromtimestamp(req_end_time).strftime(time_format)

            print('[Collector] Request all candle. req_start_time_kts: {}, req_end_time_kts: {}'.format(str_req_start_time_kts, str_req_end_time_kts))

            while True:
                candles = UpbitTrader.instance().request_candles_min(min, str_req_start_time, count=10)
                
                if candles.empty:
                    print('[Collector] Request all candle failed. Candle empty. req_uct_time:', str_req_start_time)
                    return

                DatabaseManager.instance().insert(table_name, candles)
                
                tail_time = candles.tail(1).index.values.astype(float)[0]

                if ( tail_time <= req_end_time ): # 모든 데이터 가져옴
                    print('[Collector] Request candle completed. req_start_time_kts: {}, req_end_time_kts: {}'.format(str_req_start_time_kts, str_req_end_time_kts))
                    break
                
                # 마지막 데이터에서 이어서 가져오기 위해 req_start_time 재설정
                req_start_time = tail_time
                str_req_start_time = datetime.fromtimestamp(req_start_time, timezone.utc).strftime(time_format)
                time.sleep(0.5) # 500ms sleep
                print('[Collector] Request all candle loop. req_start_time_kts:',datetime.fromtimestamp(req_start_time).strftime(time_format))

    def collect_now_candle(self, min, end_time):
        pass