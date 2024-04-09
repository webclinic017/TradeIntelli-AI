class DataFormatter:

    @staticmethod
    def formate_data(historical_data, symbol: str):
        return [
            {
                "stock": symbol,
                "date": index.strftime("%Y-%m-%d %H:%M:%S"),
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "EMA200": row['EMA200'],
                "EMA100": row['EMA100'],
                "EMA50": row['EMA50'],
                "resistance": row['resistance'],
                "support": row['support'],
                "market_direction": row['market_direction'] if "market_direction" in row else "",
            } for index, row in historical_data.iterrows()
        ]