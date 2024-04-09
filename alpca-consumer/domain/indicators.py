class Indicators:

    @staticmethod
    def __calculate_ema(historical_data, span: int = 200, price: str = "close"):
        return historical_data[price].ewm(span=span, adjust=False).mean()

    @staticmethod
    def __calculate_macd(historical_data, short_span: int = 12, long_span: int = 26, signal_span: int = 9,
                       price: str = "close"):
        """Calculate MACD and its signal line."""
        # Calculate short and long period EMAs
        ema_short = Indicators.__calculate_ema(historical_data, span=short_span, price=price)
        ema_long = Indicators.__calculate_ema(historical_data, span=long_span, price=price)

        # Calculate the MACD line (short EMA - long EMA)
        macd_line = ema_short - ema_long

        # Calculate the signal line as EMA of the MACD line
        signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()

        macd_histogram = macd_line - signal_line

        return macd_line, signal_line, macd_histogram

    @classmethod
    def add_macd(cls, historical_data):
        macd_line, signal_line, macd_histogram = Indicators.__calculate_macd(historical_data)
        historical_data['macd_histogram'] = macd_histogram
        historical_data['signal_line'] = signal_line
        historical_data['macd_line'] = macd_line

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
