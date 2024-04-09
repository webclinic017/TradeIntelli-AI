from app.domain.historical_data_retriever import HistoricalDataRetriever
from app.domain.indicators import Indicators

from app.application.historical_data_controller import send_email

from app.infastructure.redis_service import RedisService

from app.domain.market_direction_detector import MarketDirectionDetector


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        Alerts.check_market_direction("ndx100")
        Alerts.check_market_direction("gold")
        Alerts.check_market_direction("nvidia")

    @staticmethod
    def check_market_direction(symbol):
        print(f"check_market_direction for: {symbol}")
        historical_data_5, market_direction_5m, ema_market_direction_5m = Alerts.get_market_direction(symbol, "5M")
        historical_data_30, market_direction_30m, ema_market_direction_30m = Alerts.get_market_direction(symbol, "30M")
        print(f"{symbol} market_direction 5m: {market_direction_5m}")
        print(f"{symbol} market_direction 30m: {market_direction_30m}")
        redis_key_name = f'bar_alert_sent_{symbol}_{market_direction_5m}'
        alert_sent = RedisService.get(redis_key_name)

        if market_direction_5m == "Bearish" and market_direction_30m == "Bearish" and \
                ema_market_direction_5m == "Bearish" and ema_market_direction_30m == "Bearish" and\
                not alert_sent:
            subject = f"Trading alert: {symbol} is market is down {market_direction_5m}"
            body = f"Trading alert: {symbol} is market is down {market_direction_5m}"
            send_email("ndx100", subject, body)
            RedisService.set_value(redis_key_name, 600, True)

        elif market_direction_5m == "Bullish" and market_direction_30m == "Bullish" and\
                ema_market_direction_5m == "Bullish" and ema_market_direction_30m == "Bullish" and\
                not alert_sent:
            subject = f"Trading alert: {symbol} is market is up {market_direction_5m}"
            body = f"Trading alert: {symbol} is market is up {market_direction_5m}"
            send_email(f"{symbol}", subject, body)
            RedisService.set_value(redis_key_name, 600, True)

    @staticmethod
    def get_market_direction(stock, time_frame):
        print(f"get_market_direction: {stock}, {time_frame}")
        historical_data_retriever = HistoricalDataRetriever()
        historical_data = historical_data_retriever.get_historical_data(stock, time_frame)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)
        
        MarketDirectionDetector.support_and_resistance(historical_data)
        MarketDirectionDetector.ema_direction(historical_data)

        return historical_data, historical_data["market_direction"][-1], historical_data["ema_market_direction"][-1]


