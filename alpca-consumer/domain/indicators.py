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
        historical_data['is_peak'] = False
        historical_data['is_trough'] = False

        for i in range(1, len(historical_data) - 1):  # Start from second and end one before last
            prev_row, curr_row, next_row = historical_data.iloc[i-1], historical_data.iloc[i], historical_data.iloc[i+1]

            if curr_row['high'] > prev_row['high'] and curr_row['high'] > next_row['high']:
                historical_data.at[curr_row.name, 'is_peak'] = True

            if curr_row['low'] < prev_row['low'] and curr_row['low'] < next_row['low']:
                historical_data.at[curr_row.name, 'is_trough'] = True
