from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
from infastructure.notification_manager import NotificationManager
from infastructure.redis_service import RedisService
from prettytable import PrettyTable


class TradesOpportunityScanner:
    @classmethod
    def scan_most_trades(cls):
        cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
        most_traded = CapitalComDataRetriever.market_navigation(cst_token,
                                                                x_security_token,
                                                                'hierarchy_v1.commons.most_traded',
                                                                limit=20)
        res = {}
        for asset in most_traded["markets"]:
            info = {
                "epic": asset["epic"],
                "name": asset["instrumentName"],
                "instrumentType": asset["instrumentType"],
                "bid": asset["bid"],
            }
            cls.check_market_direction(asset["epic"], info)
            res[asset["epic"]] = info
        return res

    @classmethod
    def check_market_direction(cls, symbol, info):
        info = cls.combined_market_direction_strategy(symbol, info)
        combine_direction = info["combine_direction"]

        redis_key_name = f'alert_sent_{symbol}_{combine_direction}'
        alert_sent = RedisService.get(redis_key_name)

        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]  # Setting the column names
        for key, value in info.items():
            table.add_row([key, value])
        print(f"check_market_direction, symbol: {symbol}, \n {table}")

        direction = None
        if combine_direction == "Bearish" and not alert_sent:
            direction = "Down"
        elif combine_direction == "Bullish" and not alert_sent:
            direction = "Up"

        if direction:
            subject = f"Trading alert: {symbol} is market is {direction}, {combine_direction} Market"
            body = f"Trading Alert: {symbol} Market is {direction} - {combine_direction}. \n" \
                   f" Here are the details: \n\n {table}"
            NotificationManager.send_email(f"{symbol}", subject, body)
            RedisService.set_value(redis_key_name, 60 * 30, True)
        return combine_direction

    @staticmethod
    def combined_market_direction_strategy(symbol, info, tail=1, start_from_str=None, hd_4h=None, hd_30m=None):
        print(f"check_market_direction for: {symbol}")
        if hd_4h is None:
            hd_4h = HistoricalDataRetriever.get_market_data_and_direction(symbol, "4H", start_from_str)
        last_pos_4h = len(hd_4h) - tail
        s_r_direction_4h, ema_direction_4h, macd_direction_4h = \
            hd_4h["market_direction"].iloc[last_pos_4h], hd_4h["ema_market_direction"].iloc[last_pos_4h], \
            hd_4h["macd_market_direction"].iloc[last_pos_4h]

        if hd_30m is None:
            hd_30m = HistoricalDataRetriever.get_market_data_and_direction(symbol, "30M", start_from_str)
        last_pos = len(hd_30m) - tail
        s_r_direction_30m, ema_direction_30m, macd_direction_30m = \
            hd_30m["market_direction"].iloc[last_pos], hd_30m["ema_market_direction"].iloc[last_pos], \
            hd_30m["macd_market_direction"].iloc[last_pos]

        s_r_bearish = s_r_direction_4h == "Bearish"
        s_r_bullish = s_r_direction_4h == "Bullish"

        # ema_bearish = ema_direction_4h == "Bearish"
        ema_bearish = hd_30m["open"].iloc[last_pos] < hd_30m["EMA50"].iloc[last_pos]
        # ema_bullish = ema_direction_4h == "Bullish"
        ema_bullish = hd_30m["open"].iloc[last_pos] > hd_30m["EMA50"].iloc[last_pos]

        macd_bearish = macd_direction_30m == "Bearish"
        macd_bullish = macd_direction_30m == "Bullish"

        # if ema_bearish and (macd_bearish or s_r_bearish):
        if ema_bearish and s_r_bearish:
            info["combine_direction"] = "Bearish"
        # elif ema_bullish and (macd_bullish or s_r_bullish):
        elif ema_bullish and s_r_bullish:
            info["combine_direction"] = "Bullish"
        else:
            info["combine_direction"] = "Uncertain"

        info["30m_direction"] = {
            "index": hd_30m.index[last_pos],
            "S_R": s_r_direction_30m,
            "MACD": macd_direction_30m,
            "EMA": ema_direction_30m,
        }

        info["4h_direction"] = {
            "index": hd_4h.index[last_pos_4h],
            "S_R": s_r_direction_4h,
            "MACD": macd_direction_4h,
            "EMA": ema_direction_4h,
        }

        return info
