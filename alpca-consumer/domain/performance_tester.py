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



