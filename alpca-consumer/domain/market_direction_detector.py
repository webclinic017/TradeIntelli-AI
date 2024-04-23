class MarketDirectionDetector:

    @classmethod
    def macd_direction(cls, historical_data, lookback_period=5, multiplier=1):
        """Predict market direction based on the trend, position, and dynamic strength of the MACD histogram."""
        historical_data['macd_market_direction'] = "Uncertain"

        for i in range(2 + lookback_period, len(historical_data)):

            latest_histogram = historical_data.iloc[i]['macd_histogram']
            prev_histogram = historical_data.iloc[i-1]['macd_histogram']
            h_change = latest_histogram - prev_histogram
            heading_up = h_change > 0
            heading_down = h_change < 0
            historical_volatility = historical_data['macd_histogram'][i-lookback_period:i].std()
            strong_signal_threshold = historical_volatility * multiplier
            strong_signal = abs(latest_histogram) > abs(strong_signal_threshold)

            histogram_above_zero = historical_data.iloc[i]['macd_histogram'] > 0
            histogram_below_zero = not histogram_above_zero

            if histogram_above_zero and strong_signal and heading_up:
                historical_data.iloc[i, historical_data.columns.get_loc('macd_market_direction')] = "Bullish"
            elif histogram_below_zero and strong_signal and heading_down:
                historical_data.iloc[i, historical_data.columns.get_loc('macd_market_direction')] = "Bearish"
        return historical_data

    @classmethod
    def ema_direction(cls, historical_data):
        historical_data['ema_market_direction'] = "Uncertain"

        for i in range(2, len(historical_data)):
            # prev_row_2, prev_row = historical_data.iloc[i - 2], historical_data.iloc[i - 1]
            curr_row, next_row = historical_data.iloc[i - 1], historical_data.iloc[i]
            ema_up = cls._ema_going_up(historical_data, i, "EMA50") and cls._ema_going_up(historical_data, i, "EMA100") and \
                     cls._ema_going_up(historical_data, i, "EMA200")
            ema_down = cls._ema_going_down(historical_data, "EMA50") and cls._ema_going_down(historical_data, "EMA100") and \
                     cls._ema_going_down(historical_data, "EMA200")
            if curr_row["EMA50"] > curr_row["EMA100"] > curr_row["EMA200"] and ema_up:
                historical_data.iloc[i, historical_data.columns.get_loc('ema_market_direction')] = "Bullish"

            elif curr_row["EMA50"] < curr_row["EMA100"] < curr_row["EMA200"] and ema_down:
                historical_data.iloc[i, historical_data.columns.get_loc('ema_market_direction')] = "Bearish"

    @staticmethod
    def _ema_going_up(historical_data, i, span):
        return historical_data.iloc[i][span] > historical_data.iloc[i - 1][span] > historical_data.iloc[i - 2][span]

    @staticmethod
    def _ema_going_down(historical_data, span):
        i = len(historical_data) - 1
        return historical_data.iloc[i][span] < historical_data.iloc[i - 1][span] < historical_data.iloc[i - 2][span]

    @staticmethod
    def support_and_resistance(historical_data):
        # print("deciding market direction")
        historical_data['market_direction'] = "Uncertain"

        for i in range(1, len(historical_data)):
            support = historical_data['support'].iloc[i]
            resistance = historical_data['resistance'].iloc[i]
            if resistance and support:
                q = (resistance - support) * 0.25
                quarter_range_above_support = support + (2 * q)
                # half_range = support + (q * 2)
                quarter_range_below_resistance = resistance - (2 * q)
                current_price = historical_data['close'].iloc[i]
                previous_price = historical_data['close'].iloc[i - 1]
                going_up = current_price > previous_price
                going_down = current_price < previous_price

                if support <= current_price <= quarter_range_above_support and going_up:
                    historical_data.iloc[i, historical_data.columns.get_loc('market_direction')] = "Bullish"

                elif quarter_range_below_resistance <= current_price <= resistance and going_down:
                    historical_data.iloc[i, historical_data.columns.get_loc('market_direction')] = "Bearish"

        return historical_data

