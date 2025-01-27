from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient


class Alpca:
    API_KEY = 'PKM1OG4ZMBZTQC75B5TF'
    API_SECRET = 'QaLbJYSuOfJ2Yj9dl88xceijOJXLOoa8Lj7SnrXe'
    BASE_URL = 'https://paper-api.alpaca.markets'

    @classmethod
    def get_crypto_client(cls):
        return CryptoHistoricalDataClient(cls.API_KEY, cls.API_SECRET)

    @classmethod
    def get_stocks_client(cls):
        return StockHistoricalDataClient(cls.API_KEY, cls.API_SECRET)


