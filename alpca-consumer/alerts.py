from app.domain.historical_data_retriever import HistoricalDataRetriever
from app.domain.indicators import Indicators


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        market_direction_5m = Alerts.get_market_direction("btc", "5M")
        print(f"market_direction: {market_direction_5m}")

    @staticmethod
    def get_market_direction(stock, time_frame):
        print(f"get_market_direction: {stock}, {time_frame}")
        historical_data_retriever = HistoricalDataRetriever()
        historical_data = historical_data_retriever.get_historical_data(stock, time_frame)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)
        Indicators.decide_market_direction(historical_data)
        return historical_data["market_direction"][-1]
