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
    def calculate_resistance_and_support(historical_data):
        resistances = []
        supports = []

        # Thresholds
        min_touches = 2
        volume_multiplier = 1

        for i in range(1, len(historical_data) - 2):
            prev_row_2,  prev_row, curr_row, next_row = historical_data.iloc[i - 2], historical_data.iloc[i - 1], historical_data.iloc[i], historical_data.iloc[
                i + 1]

            # Volume Check
            avg_volume = historical_data['volume'].iloc[i - min_touches:i + min_touches].mean()
            is_high_volume = curr_row['volume'] > (avg_volume * volume_multiplier)

            if Indicators.__is_resistance(curr_row, prev_row, prev_row_2, next_row, is_high_volume):
                resistances.append((curr_row['high'], i))  # Store value and index

            # Identify support
            if Indicators.__support(curr_row, prev_row, prev_row_2, next_row, is_high_volume):
                supports.append((curr_row['low'], i))  # Store value and index

        historical_data['resistance'] = resistances[-1][0] if resistances else None
        historical_data['support'] = supports[-1][0] if supports else None

    @staticmethod
    def __is_resistance(curr_row, prev_row, prev_row_2, next_row, is_high_volume):
        return prev_row_2['close'] < prev_row['close'] < curr_row['close'] > next_row['close'] and is_high_volume

    @staticmethod
    def __support(curr_row, prev_row, prev_row_2, next_row, is_high_volume):
        return prev_row_2['close'] > prev_row['close'] > curr_row['close'] < next_row['close'] and is_high_volume
