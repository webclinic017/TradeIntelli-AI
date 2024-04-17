from datetime import datetime, timedelta
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import yfinance as yf
from domain import enums
from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.indicators import Indicators
from domain.market_direction_detector import MarketDirectionDetector
from infastructure.alpca import Alpca


class HistoricalDataRetriever:

    def __init__(self):
        self.time_frame = None
        self.crypto_client = Alpca.get_crypto_client()
        self.stock_client = Alpca.get_stocks_client()
        self.symbol_map = enums.symbol_map
        self.capital_symbol_map = enums.capital_com_symbol_map

    @staticmethod
    def _map_string_to_time_frame(value: str):
        print(f"_map_string_to_time_frame {value}")
        mapping = {
            '1M': TimeFrame.Minute,
            '5M': TimeFrame(5, TimeFrameUnit.Minute),
            '10M': TimeFrame(10, TimeFrameUnit.Minute),
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

    @staticmethod
    def _map_start_time(value: str):
        x = 50
        mapping = {
            '1M': 1 * x,
            '5M': 5 * x,
            '10M': 10 * x,
            '15M': 15 * x,
            '30M': 30 * x,
            '1H': 60 * x,
            '2H': 60 * 2 * x,
            '1D': 60 * 24 * x,
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
            limit=100,
            symbol_or_symbols=symbol,
            timeframe=self.time_frame,
        )
        return self.stock_client.get_stock_bars(request_params).df

    def __get_gold_historical_data(self, symbol: str, start_date: int, time_frame):
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=start_date)

        gold_data = yf.download(symbol, start=start_date, interval=time_frame.lower())
        gold_data = gold_data.rename(
            columns={"High": "high", "Low": "low", "Open": "open", "Close": "close", "Volume": "volume"})

        return gold_data

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

    @staticmethod
    def get_minutes_since_last_market_open(symbol, time_frame):
        end_date = datetime.utcnow()  # Use UTC timezone to avoid offset-aware issues
        start_date = end_date - timedelta(days=7)

        # Download data from Yahoo Finance
        data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                           interval=time_frame.lower())

        if not data.empty:
            last_open_time = data.index.max().to_pydatetime().replace(tzinfo=None)

            # Calculate difference between now (in UTC) and the last open time
            diff = end_date - last_open_time
            minutes_since_last_open = diff.total_seconds() / 60

            return minutes_since_last_open
        else:
            return None

    def get_historical_data(self, stock: str, time_frame, start_from: int = None):
        symbol = self.capital_symbol_map.get(stock.lower(), stock)
        time_frame = CapitalComDataRetriever.map_string_to_time_frame(time_frame)
        cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
        historical_data = CapitalComDataRetriever.get_asset_last_bars(cst_token,
                                                                      x_security_token,
                                                                      symbol,
                                                                      time_frame,
                                                                      200,
                                                                      start_from)

        if historical_data.empty:
            raise Exception("No data found")
        return historical_data

    @staticmethod
    def get_market_data_and_direction(stock, time_frame, start_from=None, historical_data=None):
        # print(f"get_market_direction: {stock}, {time_frame}")
        historical_data_retriever = HistoricalDataRetriever()
        if historical_data is None:
            historical_data = historical_data_retriever.get_historical_data(stock, time_frame, start_from)

        Indicators.add_ema(historical_data)
        Indicators.add_macd(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)

        MarketDirectionDetector.support_and_resistance(historical_data)
        MarketDirectionDetector.ema_direction(historical_data)
        MarketDirectionDetector.macd_direction(historical_data)

        return historical_data
