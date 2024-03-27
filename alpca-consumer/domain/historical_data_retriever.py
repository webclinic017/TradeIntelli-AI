from datetime import datetime, timedelta
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import yfinance as yf

import pandas as pd

from domain import enums
from infastructure.alpca import Alpca


class HistoricalDataRetriever:

    def __init__(self):
        self.time_frame = None
        self.crypto_client = Alpca.get_crypto_client()
        self.stock_client = Alpca.get_stocks_client()
        self.symbol_map = enums.symbol_map

    @staticmethod
    def _map_string_to_time_frame(value: str):
        mapping = {
            '1M': TimeFrame.Minute,
            '5M': TimeFrame(5, TimeFrameUnit.Minute),
            '15M': TimeFrame(15, TimeFrameUnit.Minute),
            '30M': TimeFrame(30, TimeFrameUnit.Minute),
            '1H': TimeFrame.Hour,
            '2H': TimeFrame(2, TimeFrameUnit.Hour),
            '1D': TimeFrame.Day,
        }
        if value in mapping:
            return mapping[value]
        else:
            raise ValueError(f"Unknown TimeFrame value: {value}")

    def __get_stock_historical_data(self, symbol: str, start_date: int):
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=start_date)
        # start_date = end_date - timedelta(hours=1)
        request_params = StockBarsRequest(
            start=start_date,
            # end=end_date,
            # limit=100,
            symbol_or_symbols=symbol,
            timeframe=self.time_frame,
        )
        return self.stock_client.get_stock_bars(request_params).df

    def __get_gold_historical_data(self, symbol: str, start_date: int, time_frame):
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=start_date)
        # start_date = end_date - timedelta(hours=1)
        request_params = StockBarsRequest(
            start=start_date,
            # end=end_date,
            # limit=100,
            symbol_or_symbols=symbol,
            timeframe=self.time_frame,
        )

        y = yf.download(symbol, start=start_date, interval=time_frame.lower())
        y["high"] = y["High"]
        y["close"] = y["Close"]
        y["volume"] = y["Volume"]
        y["open"] = y["Open"]
        y["low"] = y["Low"]
        return y

    def __get_crypto_historical_data(self, start_date: int):
        symbol = 'BTC/USD'
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=start_date)

        request_params = CryptoBarsRequest(
            adjustment='raw',
            symbol_or_symbols=symbol,
            timeframe=self.time_frame,
            start=start_date,
            end=end_date
        )

        # Fetch historical data
        return self.crypto_client.get_crypto_bars(request_params).df

    def get_historical_data(self, stock: str, time_frame, start_date: int):
        symbol = self.symbol_map.get(stock.lower())
        self.time_frame = self._map_string_to_time_frame(time_frame)

        if stock.lower() in ['gold', "ndx100", "spx500"]:
            historical_data = self.__get_gold_historical_data(symbol, start_date, time_frame)
        elif stock.lower() not in ['btc']:
            historical_data = self.__get_stock_historical_data(symbol, start_date)
        else:  # Crypto assets
            historical_data = self.__get_crypto_historical_data(start_date)

        if isinstance(historical_data.index, pd.MultiIndex):
            historical_data = historical_data.reset_index(level=0, drop=True)
            historical_data.index = pd.DatetimeIndex(historical_data.index)

        if historical_data.empty:
            raise Exception("No data found")
        return historical_data
