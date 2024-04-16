from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
from infastructure.notification_manager import NotificationManager
from infastructure.redis_service import RedisService


class TradesOpportunityScanner:
    @classmethod
    def scan_most_trades(cls):
        cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
        most_traded = CapitalComDataRetriever.market_navigation(cst_token, x_security_token,
                                                                'hierarchy_v1.commons.most_traded', limit=20)
        res = {}
        for asset in most_traded["markets"]:
            res[asset["epic"]] = cls.check_market_direction(asset["epic"])
        return res

    @classmethod
    def check_market_direction(cls, symbol):
        market_direction = cls.combined_market_direction(symbol)

        redis_key_name = f'alert_sent_{symbol}_{market_direction}'
        alert_sent = RedisService.get(redis_key_name)

        if market_direction == "Bearish" and not alert_sent:
            subject = f"Trading alert: {symbol} is market is down {market_direction}"
            body = f"Trading alert: {symbol} is market is down {market_direction}"
            NotificationManager.send_email(symbol, subject, body)
            RedisService.set_value(redis_key_name, 600, True)

        elif market_direction == "Bullish" and not alert_sent:
            subject = f"Trading alert: {symbol} is market is up {market_direction}"
            body = f"Trading alert: {symbol} is market is up {market_direction}"
            NotificationManager.send_email(f"{symbol}", subject, body)
            RedisService.set_value(redis_key_name, 600, True)
        return market_direction

    @staticmethod
    def combined_market_direction(symbol):
        print(f"check_market_direction for: {symbol}")
        hd_5 = HistoricalDataRetriever.get_market_date_and_direction(symbol, "4H")
        last_pos = len(hd_5) - 1
        s_r_direction_5m, ema_direction_4h, macd_direction_4h = \
            hd_5["market_direction"].iloc[last_pos], hd_5["ema_market_direction"].iloc[last_pos], \
            hd_5["macd_market_direction"].iloc[last_pos]

        hd_30 = HistoricalDataRetriever.get_market_date_and_direction(symbol, "30M")
        last_pos = len(hd_30) - 1
        s_r_direction_30m, ema_direction_30m, macd_direction_30m = \
            hd_30["market_direction"].iloc[last_pos], hd_30["ema_market_direction"].iloc[last_pos], \
            hd_30["macd_market_direction"].iloc[last_pos]

        print(f"{symbol} S&R_5m: {s_r_direction_5m},"
              f" S&R_30m: {s_r_direction_30m},"
              f" ema_4H: {ema_direction_4h},"
              f" ema_30m: {ema_direction_30m}"
              f" macd_4H: {macd_direction_4h},"
              f" macd_30m: {macd_direction_30m}")

        s_r_bearish = s_r_direction_5m == s_r_direction_30m == "Bearish"
        s_r_bullish = s_r_direction_5m == s_r_direction_30m == "Bullish"

        ema_bearish = ema_direction_4h == ema_direction_30m == "Bearish"
        ema_bullish = ema_direction_4h == ema_direction_4h == "Bullish"

        macd_bearish = macd_direction_4h == macd_direction_30m == "Bearish"
        macd_bullish = macd_direction_4h == macd_direction_30m == "Bullish"

        if ema_bearish and (macd_bearish or s_r_bearish):
            return "Bearish"

        elif ema_bullish and (macd_bullish or s_r_bullish):
            return "Bullish"

        return "Uncertain"
