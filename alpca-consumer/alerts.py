from app.domain.historical_data_retriever import HistoricalDataRetriever
from app.domain.indicators import Indicators

from app.application.historical_data_controller import send_email


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        market_direction_5m = Alerts.get_market_direction("ndx100", "5M")
        market_direction_30m = Alerts.get_market_direction("ndx100", "30M")
        print(f"market_direction 5m: {market_direction_5m}")
        print(f"market_direction 30m: {market_direction_30m}")
        if market_direction_5m == "Bearish" and market_direction_30m == "Bearish":
            subject = f"Trading alert: ndx100 is {market_direction_5m}"
            send_email("ndx100", subject)

    @staticmethod
    def get_market_direction(stock, time_frame):
        print(f"get_market_direction: {stock}, {time_frame}")
        historical_data_retriever = HistoricalDataRetriever()
        historical_data = historical_data_retriever.get_historical_data(stock, time_frame)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)
        Indicators.decide_market_direction(historical_data)
        return historical_data["market_direction"][-1]


