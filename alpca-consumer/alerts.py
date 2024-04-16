from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
from domain.indicators import Indicators
from domain.market_direction_detector import MarketDirectionDetector
from infastructure.notification_manager import NotificationManager
from infastructure.redis_service import RedisService


class Alerts:

    @staticmethod
    def print_text(message):
        print(f"Alert: {message}")

    @staticmethod
    def run_alerts():
        print("running alerts:")
        # Alerts.check_market_direction("ndx100")
        # Alerts.check_market_direction("gold")
        # Alerts.check_market_direction("nvidia")
        cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
        most_traded = CapitalComDataRetriever.market_navigation(cst_token, x_security_token,
                                                                'hierarchy_v1.commons.most_traded', limit=20)
        for asset in most_traded["markets"]:
            Alerts.check_market_direction(asset["epic"])

    @staticmethod
    def check_market_direction(symbol):
        print(f"check_market_direction for: {symbol}")
        historical_data_5, s_r_direction_5m, ema_direction_5m, macd_direction_5m = \
            Alerts.get_market_direction(symbol, "5M")
        historical_data_30, s_r_direction_30m, ema_direction_30m, macd_direction_30m =\
            Alerts.get_market_direction(symbol, "30M")
        print(f"{symbol} S&R_5m: {s_r_direction_5m},"
              f" S&R_30m: {s_r_direction_30m},"
              f" ema_5m: {ema_direction_5m},"
              f" ema_30m: {ema_direction_30m}"
              f" macd_5m: {macd_direction_5m},"
              f" macd_30m: {macd_direction_30m}")

        s_r_bearish = s_r_direction_5m == s_r_direction_30m == "Bearish"
        s_r_bullish = s_r_direction_5m == s_r_direction_30m == "Bullish"

        ema_bearish = ema_direction_5m == ema_direction_30m == "Bearish"
        ema_bullish = ema_direction_5m == ema_direction_5m == "Bullish"

        macd_bearish = macd_direction_5m == macd_direction_30m == "Bearish"
        macd_bullish = macd_direction_5m == macd_direction_30m == "Bullish"

        redis_key_name = f'bar_alert_sent_{symbol}_{s_r_direction_5m}'
        alert_sent = RedisService.get(redis_key_name)

        if ema_bearish and (macd_bearish or s_r_bearish) and not alert_sent:
            subject = f"Trading alert: {symbol} is market is down {s_r_direction_5m}"
            body = f"Trading alert: {symbol} is market is down {s_r_direction_5m}"
            NotificationManager.send_email("ndx100", subject, body)
            RedisService.set_value(redis_key_name, 600, True)

        elif ema_bullish and (macd_bullish or s_r_bullish) and not alert_sent:
            subject = f"Trading alert: {symbol} is market is up {s_r_direction_5m}"
            body = f"Trading alert: {symbol} is market is up {s_r_direction_5m}"
            NotificationManager.send_email(f"{symbol}", subject, body)
            RedisService.set_value(redis_key_name, 600, True)

    @staticmethod
    def get_market_direction(stock, time_frame):
        # print(f"get_market_direction: {stock}, {time_frame}")
        historical_data_retriever = HistoricalDataRetriever()
        historical_data = historical_data_retriever.get_historical_data(stock, time_frame)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)

        MarketDirectionDetector.support_and_resistance(historical_data)
        MarketDirectionDetector.ema_direction(historical_data)

        return historical_data, historical_data["market_direction"].iloc[len(historical_data) - 1], \
               historical_data["ema_market_direction"].iloc[len(historical_data) - 1], \
               historical_data["macd_market_direction"].iloc[len(historical_data) - 1]
