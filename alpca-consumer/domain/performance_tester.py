from domain.historical_data_retriever import HistoricalDataRetriever
from domain.trades_opportunity_scanner import TradesOpportunityScanner
from datetime import datetime, timedelta

class PerformanceTester:

    @staticmethod
    def calculate_profit(historical_data, indicator: str = "market_direction"):
        print(f"Starting calculate_profit, indicator: {indicator}")
        # historical_data = historical_data[-40:]
        trade_is_open = False
        start_price = 0
        max_price = 0
        trilling_loss = -20
        profit = 0
        num = len(historical_data)
        for index, curr in historical_data.iterrows():
            market_direction = curr[indicator]
            if not trade_is_open and market_direction == "Bullish":
                trade_is_open = True
                start_price = curr["close"]
                print(f"Trade started at: {index}, price:  {start_price}")
            if trade_is_open:
                max_price = max(curr["close"], max_price)
                if max_price - trilling_loss < curr["close"]:
                    trade_is_open = False
                    profit += curr["close"] - start_price
                    print(f"Trade closed at: {index}, price:  {start_price}, profit:  {profit}")
        if trade_is_open:
            last_bar = historical_data.iloc[num-1]
            profit += last_bar["close"] - start_price
            print(f"Trade closed at last bar, price:  {start_price}, profit:  {profit}")
        print(f"Finished calculate_profit, indicator: {indicator}, profit:  {profit}")
        return profit

    @staticmethod
    def calculate_profit_all(historical_data):
        historical_data["s_r_profit"] = PerformanceTester.calculate_profit(historical_data,
                                                                           indicator="market_direction")
        historical_data["ema_profit"] = PerformanceTester.calculate_profit(historical_data,
                                                                           indicator="ema_market_direction")
        historical_data["macd_profit"] = PerformanceTester.calculate_profit(historical_data,
                                                                            indicator="macd_market_direction")

    @staticmethod
    def calculate_success_rate(symbol, period=10):
        res = {"long_profit": 0,
               "long_trade_start_index": None,
               "short_profit": 0,
               "short_trade_start_index": None,
               }

        predications = {}
        historical_data_retriever = HistoricalDataRetriever()

        hd_4h = historical_data_retriever.get_historical_data(symbol, "4H")
        hd_30m = historical_data_retriever.get_historical_data(symbol, "30M")
        long_trade_start_price = 0
        long_trade_start_index = 0
        short_trade_start_price = 0
        short_trade_start_index = 0
        for i in range(1, period + 1):
            info = {}
            _hd_4h = hd_4h[:len(hd_4h) - period + i]
            _hd_30m = hd_30m[:len(hd_30m) - ((period - i)*8)]

            _hd_4h = HistoricalDataRetriever.get_market_data_and_direction(symbol, "4H", historical_data=_hd_4h)
            _hd_30m = HistoricalDataRetriever.get_market_data_and_direction(symbol, "30M", historical_data=_hd_30m)
            TradesOpportunityScanner.combined_market_direction_strategy(symbol, info, 1, hd_4h=_hd_4h, hd_30m=_hd_30m)

            close_30m = _hd_30m["close"].iloc[len(_hd_30m) - 1]
            close_4h = _hd_4h["close"].iloc[len(_hd_4h) - 1]
            info["close_30m"] = close_30m
            info["close_4h"] = close_4h
            print("calculate_success_rate", info)
            predications[_hd_30m.index.max()] = info
            if info["combine_direction"] == "Bullish" and not long_trade_start_price:
                long_trade_start_price = close_30m
                long_trade_start_index = _hd_30m.index.max()
            if info["combine_direction"] == "Bearish" and not short_trade_start_price:
                short_trade_start_price = close_30m
                short_trade_start_index = _hd_30m.index.max()

        last_close = hd_30m["close"].iloc[len(hd_30m)-1]
        if long_trade_start_price:
            res["long_profit"] = (last_close - long_trade_start_price)
            res["long_trade_start_index"] = long_trade_start_index

        if short_trade_start_price:
            res["short_profit"] = (short_trade_start_price - last_close)
            res["short_trade_start_index"] = short_trade_start_index

        res["predications"] = predications
        return res
