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
        # Initialize resistance and support with None or some default value
        historical_data['resistance'] = None
        historical_data['support'] = None

        # Variables to store the final peak and support values
        # Lists to store resistance and support values along with their indices
        resistances = [(0, 1)]
        supports = [(0, 1)]

        # Iterate to find resistances and supports
        for i in range(1, len(historical_data) - 1):
            prev_row, curr_row, next_row = historical_data.iloc[i - 1], historical_data.iloc[i], historical_data.iloc[
                i + 1]

            # Identify resistance
            if curr_row['high'] > prev_row['high'] and curr_row['high'] > next_row['high']:
                resistances.append((curr_row['high'], i))  # Store value and index

            # Identify support
            if curr_row['low'] < prev_row['low'] and curr_row['low'] < next_row['low']:
                supports.append((curr_row['low'], i))  # Store value and index

        historical_data['resistance'], _ = resistances[-1]
        historical_data['support'], _ = supports[-1]


