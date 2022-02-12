from BaseTrader import *
from SettingManager import *
from AuthManager import AuthManager
import requests
import pandas as pd

class UpbitTrader(BaseTrader, Singleton):
    def get_server_url(self):
        return 'https://api.upbit.com'

    def get_websocket_uri(self):
        return 'wss://api.upbit.com/websocket/v1'

    def request_account(self):
        headers = AuthManager.instance().get_auth_headers()
        res = requests.get(self.get_server_url() + '/v1/accounts', headers=headers)

        SettingManager.checkHttpCode(self.__class__.__name__, self.request_account.__name__, res.status_code)
        return res.json()

    # to_time foramt: yyyy-MM-dd HH:mm:ss
    def request_candles_min(self, min, to_time, count=200):
        url = self.get_server_url()
        url += '/v1/candles/minutes/{}?market=KRW-BTC&to={}&count={}'.format(min, to_time, count)
        headers = {"Accept": "application/json"}
        res = requests.request("GET", url, headers=headers)

        if not SettingManager.checkHttpCode(self.__class__.__name__, self.request_account.__name__, res.status_code):
            return pd.DataFrame()

        df = pd.DataFrame(res.json())

        # 불필요한 Column 제거, UTC time index로 추가
        df = df.drop(['market', 'unit'], axis=1)
        df['candle_date_time_utc_timestamp'] = pd.to_datetime(df['candle_date_time_utc'], format='%Y-%m-%dT%H:%M:%S')
        df['candle_date_time_utc_timestamp'] = df['candle_date_time_utc_timestamp'].apply(lambda x: x.timestamp())
        df.set_index('candle_date_time_utc_timestamp', inplace=True)
        return df

    def request_candles_day(self, to_time, count=200):
        url = self.get_server_url()
        url += '/v1/candles/days?market=KRW-BTC&to={}&count={}'.format(to_time, count)
        headers = {"Accept": "application/json"}
        res = requests.request("GET", url, headers=headers)

        if not SettingManager.checkHttpCode(self.__class__.__name__, self.request_account.__name__, res.status_code):
            return pd.DataFrame()
        
        df = pd.DataFrame(res.json())
        
        # 불필요한 Column 제거, UTC time index로 추가
        df = df.drop(['market', 'unit'], axis=1)
        df['candle_date_time_utc_timestamp'] = pd.to_datetime(df['candle_date_time_utc'], format='%Y-%m-%dT%H:%M:%S')
        df['candle_date_time_utc_timestamp'] = df['candle_date_time_utc_timestamp'].apply(lambda x: x.timestamp())
        df.set_index('candle_date_time_utc_timestamp', inplace=True)
        return df

    def generate_subscribe_format(self, subscribe_type):
        subscribe_format = [ 
            {'ticket':SettingManager.g_uuid},
            {
                'type':SubscribeType.toString(subscribe_type).lower(),
                'codes':['KRW-BTC'],
                'isOnlyRealtime': True
            },
            {'format':'SIMPLE'}
        ]
        return subscribe_format
