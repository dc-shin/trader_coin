from Singleton import Singleton
from enum import Enum
import websockets
import json
import asyncio

class SubscribeType(Enum):
    Ticker = 0 # 현재가
    Trade = 1 # 체결
    Orderbook = 2 # 호가

    def toString(enumType):
        if enumType == SubscribeType.Ticker:
            return 'Ticker'
        elif enumType == SubscribeType.Trade:
            return 'Trade'
        elif enumType == SubscribeType.Orderbook:
            return 'Orderbook'
        return ''

class BaseTrader():
    def get_server_url(self):
        return ''

    def get_websocket_uri(self):
        return ''
    
    def get_ping_interval(self):
        return 60

    def request_account(self):
        pass

    def request_candles_min(self, min, to_time, count=200):
        pass

    def request_candles_day(self, to_time, count=200):
        pass

    def generate_subscribe_format(self, subscribe_type):
        return []

    async def subscribe_run(self, subscribe_format, subscribe_type):
        async with websockets.connect(uri=self.get_websocket_uri(), ping_interval=self.get_ping_interval()) as websocket:
            print('[BaseTrader] subscribe start. type: ', SubscribeType.toString(subscribe_type))

            subscribe_data = json.dumps(subscribe_format)
            await websocket.send(subscribe_data)

            # Receive data from server
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                print(data)

    # mp.Queue()
    # p = mp.Process(name="Producer", target=producer, args=(q,), daemon=True)
    # p.start()
    async def subscribe(self, subscribe_type):
        subscribe_format = self.generate_subscribe_format(subscribe_type)
        
        if not subscribe_format:
            print('[BaseTrader][subscribe] invalid type: {}'.format(subscribe_type))
            return

        asyncio.run(self.subscribe_run(subscribe_format, subscribe_type))