import requests


class CapitalComDataRetriever:
    base_url = "https://demo-api-capital.backend-capital.com/api/v1"
    api_key = "zsOQe25jw8uT5mPj"

    @staticmethod
    def convert_to_pd(raw_historical_data):
        import pandas as pd
        import numpy as np
        prices = raw_historical_data['prices']
        # print("prices:", type(prices), prices)
        # Creating a list of dictionaries to convert to DataFrame
        df_data = [{
            'timestamp': price['snapshotTimeUTC'],
            'open': (price['openPrice']['bid'] + price['openPrice']['ask']) / 2,
            'high': (price['highPrice']['bid'] + price['highPrice']['ask']) / 2,
            'low': (price['lowPrice']['bid'] + price['lowPrice']['ask']) / 2,
            'close': (price['closePrice']['bid'] + price['closePrice']['ask']) / 2,
            'volume': price['lastTradedVolume'],
            # Adding placeholder values for 'trade_count' and 'vwap' as they are not available in the original data
            'trade_count': np.nan,
            'vwap': np.nan
        } for price in prices]

        # Converting to DataFrame
        historical_data = pd.DataFrame(df_data)

        # Setting the timestamp as the index
        historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])
        historical_data.set_index('timestamp', inplace=True)
        return historical_data

    @classmethod
    def create_capital_com_session(cls):
        # Replace these with your actual details

        import redis
        # Connect to Redis
        r = redis.Redis(host='redis', port=6379, db=0)

        # Store a value
        r.set('test_key', 'Hello, Redis!')

        # Retrieve the value
        cst_token = r.get('cst_token')
        x_security_token = r.get('x_security_token')
        if cst_token and x_security_token:
            print("Session restored successfully.", cst_token, x_security_token)
            return cst_token, x_security_token
        else:
            identifier = "omerahmed41@gmail.com"
            password = "E@ar7LUWh6ajcdj"

            headers = {
                "X-CAP-API-KEY": cls.api_key,
            }

            data = {
                "identifier": identifier,
                "password": password,
            }

            # Start session
            session_response = requests.post(f"{cls.base_url}/session", headers=headers, json=data)
            if session_response.ok:
                session_tokens = session_response.headers
                cst_token = session_tokens.get("CST")
                x_security_token = session_tokens.get("X-SECURITY-TOKEN")

                print("Session created successfully.", cst_token, x_security_token)

                r.setex('x_security_token', 600, x_security_token)
                r.setex('cst_token', 600, cst_token)

                return cst_token, x_security_token
            else:
                raise Exception("Failed to start session.")

    @staticmethod
    def get_capital_com_server_time():
        base_url = "https://demo-api-capital.backend-capital.com/api/v1"
        time_response = requests.get(f"{base_url}/time")
        if time_response.ok:
            server_time = time_response.json()
            print("Server Time:", server_time)
            return server_time
        else:
            print("Failed to fetch server time.")
            return None

    @classmethod
    def get_asset_last_bars(cls, cst_token, x_security_token, instrument_symbol="SILVER", timeframe="MINUTE_15",
                            number_of_bars=50):
        historical_data_url = f"{cls.base_url}/prices/{instrument_symbol}?resolution={timeframe}&max={number_of_bars}"
        # Set up the headers with your session tokens
        headers = {
            "X-CAP-API-KEY": cls.api_key,
            "CST": cst_token,
            "X-SECURITY-TOKEN": x_security_token,
        }

        # Make the request
        response = requests.get(historical_data_url, headers=headers)
        if response.ok:
            historical_data = response.json()
            return cls.convert_to_pd(historical_data)
        else:
            raise Exception(f"Failed to fetch historical data. Status Code: {response.status_code}",
                            response.text,
                            historical_data_url)

    @classmethod
    def market_search(cls, api_key, cst_token, x_security_token, symbol):
        auth_headers = {
            "X-CAP-API-KEY": api_key,
            "CST": cst_token,
            "X-SECURITY-TOKEN": x_security_token,
        }

        # Fetch the current price for gold
        market_data_url = f"{cls.base_url}/markets?searchTerm={symbol}"  # Adjust the endpoint as necessary
        response = requests.get(market_data_url, headers=auth_headers)
        if response.ok:
            gold_data = response.json()
            print("Gold Market Data:", gold_data)
            return gold_data
        else:
            raise Exception("Failed to fetch gold price. Status Code:", response.status_code, response.text)

    @staticmethod
    def map_string_to_time_frame(value: str):
        print("_map_string_to_time_frame", value)
        mapping = {
            '1M': "MINUTE",
            '5M': "MINUTE_5",
            '10M': "MINUTE_10",
            '15M': "MINUTE_15",
            '30M': "MINUTE_30",
            '1H': "HOUR",
            '2H': "HOUR_2",
            '4H': "HOUR_4",
            '1D': "DAY",
        }
        if value in mapping:
            return mapping[value]
        else:
            raise ValueError(f"Unknown TimeFrame value: {value}")