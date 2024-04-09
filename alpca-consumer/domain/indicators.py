from app.data_formatter import DataFormatter


class Indicators:

    @staticmethod
    def __calculate_ema(historical_data, span: int = 200, price: str = "close"):
        return historical_data[price].ewm(span=span, adjust=False).mean()

    @classmethod
    def add_ema(cls, historical_data):
        historical_data['EMA200'] = cls.__calculate_ema(historical_data, 200)
        historical_data['EMA100'] = cls.__calculate_ema(historical_data, 100)
        historical_data['EMA50'] = cls.__calculate_ema(historical_data, 50)

    @staticmethod
    def decide_market_direction(historical_data):
        print("decide_market_direction")

        latest_price = historical_data['close'].iloc[-1]  # Assuming latest_data is structured as described previously
        support = historical_data['support'].iloc[-1]
        resistance = historical_data['resistance'].iloc[-1]
        if resistance and support:
            q = (resistance - support) * 0.25
            quarter_range_above_support = support + q
            quarter_range_below_resistance = resistance - q
            print("support and resistance:", resistance, latest_price, quarter_range_below_resistance, support,
                  latest_price, quarter_range_above_support)
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

    @staticmethod
    def calculate_resistance_and_support(historical_data):
        resistances = []
        supports = []

        # Thresholds
        min_touches = 2
        volume_multiplier = 1.5

        for i in range(1, len(historical_data) - 1):
            prev_row, curr_row, next_row = historical_data.iloc[i - 1], historical_data.iloc[i], historical_data.iloc[
                i + 1]

            # Volume Check
            avg_volume = historical_data['volume'].iloc[i - min_touches:i + min_touches].mean()
            is_high_volume = curr_row['volume'] > (avg_volume * volume_multiplier)

            if Indicators.__is_resistance(curr_row, prev_row, next_row, is_high_volume):
                resistances.append((curr_row['high'], i))  # Store value and index

            # Identify support
            if Indicators.__support(curr_row, prev_row, next_row, is_high_volume):
                supports.append((curr_row['low'], i))  # Store value and index

        historical_data['resistance'] = resistances[-1][0] if resistances else None
        historical_data['support'] = supports[-1][0] if supports else None

    @staticmethod
    def __is_resistance(curr_row, prev_row, next_row, is_high_volume):
        return curr_row['close'] > prev_row['close'] and curr_row['close'] > next_row['close'] and is_high_volume

    @staticmethod
    def __support(curr_row, prev_row, next_row, is_high_volume):
        return curr_row['close'] < prev_row['close'] and curr_row['close'] < next_row['close'] and is_high_volume
