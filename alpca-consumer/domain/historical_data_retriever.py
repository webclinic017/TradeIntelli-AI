from datetime import datetime, timedelta
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

import pandas as pd

from domain import enums
from infastructure.alpca import Alpca


class HistoricalDataRetriever:

    def __init__(self):
        self.time_frame = None
        self.crypto_client = Alpca.get_crypto_client()
        self.stock_client = Alpca.get_stocks_client()
        self.symbol_map = enums.symbol_map
        self.api = Alpca.get_api()

    @staticmethod
    def _map_string_to_time_frame(value: str):
        mapping = {
            '30M': TimeFrame(30, TimeFrame.Minute),
            '1H': TimeFrame.Hour,
            '2H': TimeFrame(2, TimeFrame.Hour),
            '1D': TimeFrame.Day,
        }
        if value in mapping:
            return mapping[value]
        else:
            raise ValueError(f"Unknown TimeFrame value: {value}")

    def __get_stock_historical_data(self, symbol: str):
        # start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        # end_date = (datetime.now() - timedelta(days=360)).strftime("%Y-%m-%d")

        return self.api.get_bars(
            symbol=symbol,
            timeframe=self.time_frame,
            limit=100
        ).df

    def __get_crypto_historical_data(self):
        symbol = 'BTC/USD'
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)

        request_params = CryptoBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=self.time_frame,
            start=start_date,
            end=end_date
        )

        # Fetch historical data
        return self.crypto_client.get_crypto_bars(request_params).df

    def get_historical_data(self, stock: str, time_frame):
        symbol = self.symbol_map.get(stock.lower())
        self.time_frame = self._map_string_to_time_frame(time_frame)
        print("self.time_frame", self.time_frame)
        if stock.lower() not in ['btc']:
            historical_data = self.__get_stock_historical_data(symbol)
        else:  # Crypto assets
            historical_data = self.__get_crypto_historical_data()

        if isinstance(historical_data.index, pd.MultiIndex):
            historical_data = historical_data.reset_index(level=0, drop=True)
            historical_data.index = pd.DatetimeIndex(historical_data.index)

        if historical_data.empty:
            raise Exception("No data found")
        return historical_data
