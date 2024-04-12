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
                "s_r_profit": row['s_r_profit'],
                "ema_profit": row['ema_profit'],
                "macd_profit": row['macd_profit'],
                "market_direction": row['market_direction'] if "market_direction" in row else "",
                "ema_market_direction": row['ema_market_direction'] if "ema_market_direction" in row else "",
                "macd_market_direction": row['macd_market_direction'] if "macd_market_direction" in row else "",
                "macd_histogram": row['macd_histogram'] if "macd_histogram" in row else 0,
            } for index, row in historical_data.iterrows()
        ]