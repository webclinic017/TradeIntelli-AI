from scipy.stats import linregress
import numpy as np


class MarketDirectionDetector:

    @classmethod
    def macd_direction(cls, historical_data, lookback_period=30, multiplier=1):
        """Predict market direction based on the trend, position, and dynamic strength of the MACD histogram."""

        # Calculate the standard deviation of the MACD histogram over the lookback period
        historical_volatility = historical_data['macd_histogram'].tail(lookback_period).std()
        strong_signal_threshold = historical_volatility * multiplier

        # Linear regression on MACD histogram values to determine trend
        histogram_values = historical_data['macd_histogram'].tail(lookback_period)
        slope, intercept, r_value, p_value, std_err = linregress(range(len(histogram_values)), histogram_values)
        histogram_trending_up = slope > 0

        histogram_above_zero = historical_data.iloc[-1]['macd_histogram'] > 0

        # Calculate slope of the histogram changes (acceleration)
        histogram_changes = np.diff(histogram_values)
        change_slope, change_intercept, change_r_value, change_p_value, change_std_err = linregress(
            range(len(histogram_changes)), histogram_changes)

        # Determine increasing strength
        latest_histogram = historical_data.iloc[-1]['macd_histogram']
        histogram_change = latest_histogram - historical_data.iloc[-2]['macd_histogram']
        increasing_strength = change_slope > 0 and abs(histogram_change) > strong_signal_threshold

        if histogram_trending_up and histogram_above_zero:
            historical_data['macd_market_direction'] = "Bullish"
        elif not histogram_trending_up and not histogram_above_zero:
            historical_data['macd_market_direction'] = "Bearish"
        else:
            historical_data['macd_market_direction'] = "Uncertain"

        return historical_data

    @classmethod
    def ema_direction(cls, historical_data):
        i = len(historical_data) - 1
        # prev_row_2, prev_row = historical_data.iloc[i - 2], historical_data.iloc[i - 1]
        curr_row, next_row = historical_data.iloc[i - 1], historical_data.iloc[i]
        ema_up = cls._ema_going_up(historical_data, "EMA50") and cls._ema_going_up(historical_data, "EMA100") and \
                 cls._ema_going_up(historical_data, "EMA200")
        ema_down = cls._ema_going_down(historical_data, "EMA50") and cls._ema_going_down(historical_data, "EMA100") and \
                 cls._ema_going_down(historical_data, "EMA200")
        if curr_row["EMA50"] > curr_row["EMA100"] > curr_row["EMA200"] and ema_up:
            historical_data['ema_market_direction'] = "Bullish"
        elif curr_row["EMA50"] < curr_row["EMA100"] < curr_row["EMA200"] and ema_down:
            historical_data['ema_market_direction'] = "Bearish"
        else:
            historical_data['ema_market_direction'] = "Uncertain"

    @staticmethod
    def _ema_going_up(historical_data, span):
        i = len(historical_data) - 1
        return historical_data.iloc[i][span] > historical_data.iloc[i - 1][span] > historical_data.iloc[i - 2][span]

    @staticmethod
    def _ema_going_down(historical_data, span):
        i = len(historical_data) - 1
        return historical_data.iloc[i][span] < historical_data.iloc[i - 1][span] < historical_data.iloc[i - 2][span]

    @staticmethod
    def support_and_resistance(historical_data):
        print("decide_market_direction")

        latest_price = historical_data['close'].iloc[-1]  # Assuming latest_data is structured as described previously
        support = historical_data['support'].iloc[-1]
        resistance = historical_data['resistance'].iloc[-1]
        if resistance and support:
            q = (resistance - support) * 0.25
            quarter_range_above_support = support + q
            quarter_range_below_resistance = resistance - q
            # print("support and resistance:", resistance, latest_price, quarter_range_below_resistance, support,
            #       latest_price, quarter_range_above_support)
        else:
            historical_data['market_direction'] = "Uncertain"

            print("not support or resistance:", resistance, support)
            return

        if support <= latest_price <= quarter_range_above_support \
                and historical_data['close'].iloc[-1] > historical_data['close'].iloc[-2]:
            print("Bullish:", resistance, support)
            historical_data['market_direction'] = "Bullish"

        elif quarter_range_below_resistance <= latest_price <= resistance:
            # \
            #     and historical_data['close'].iloc[-1] < historical_data['close'].iloc[-2]:
            print("check Bearish:", resistance, support)
            historical_data['market_direction'] = "Bearish"
        else:
            historical_data['market_direction'] = "Uncertain"
