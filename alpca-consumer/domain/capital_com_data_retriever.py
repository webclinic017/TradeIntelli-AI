import requests

from domain import enums
from infastructure.capital_com import CapitalCom
from infastructure.redis_service import RedisService


class CapitalComDataRetriever:
    base_url = CapitalCom.base_url
    api_key = CapitalCom.api_key

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
        cst_token = RedisService.get('cst_token')
        x_security_token = RedisService.get('x_security_token')
        if cst_token and x_security_token:
            print(f"Session restored successfully: {cst_token}, {x_security_token}")
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

                print(f"Session created successfully: {cst_token}, {x_security_token}")

                RedisService.set_value('x_security_token', 600, x_security_token)
                RedisService.set_value('cst_token', 600, cst_token)

                return cst_token, x_security_token
            else:
                raise Exception("Failed to start session.")

    @staticmethod
    def delete_position_at_capital(cst_token, x_security_token, deal_id):
        headers = {
            "X-SECURITY-TOKEN": x_security_token,
            "CST": cst_token,
            "Content-Type": "application/json"
        }

        # Make the DELETE request
        response = requests.delete(f"{CapitalComDataRetriever.base_url}/positions/{deal_id}", headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to delete position: {response.status_code} - {response.text}")
            return False

    @staticmethod
    def open_position(cst_token, x_security_token, symbol, stop_loss, profit_level, size, direction: str = "BUY"):
        epic = enums.capital_com_symbol_map.get(symbol.lower())

        url = f"{CapitalComDataRetriever.base_url}/positions"
        headers = {
            "X-SECURITY-TOKEN": x_security_token,
            "CST": cst_token,
            "Content-Type": "application/json"
        }
        payload = {
            'epic': epic,
            'direction': direction,
            'size': size,
            'guaranteedStop': False,
            # 'stopLevel': stop_loss,
            # 'profitLevel': profit_level
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print('Position opened successfully')
            return response.json()
        else:
            raise Exception(f"Failed to open position: {response.status_code} - {response.text}")

    @staticmethod
    def get_open_positions(cst_token, x_security_token):
        positions_url = f"{CapitalComDataRetriever.base_url}/positions"
        positions_headers = {
            "X-SECURITY-TOKEN": x_security_token,
            "CST": cst_token,
            "Content-Type": "application/json"
        }

        positions_response = requests.get(positions_url, headers=positions_headers)
        open_positions = positions_response.json()
        print(f"open_positions: {open_positions}")
        return open_positions
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
                            number_of_bars=50, start_from=None):
        historical_data_url = f"{cls.base_url}/prices/{instrument_symbol}?resolution={timeframe}&max={number_of_bars}"
        redis_per = 1
        if start_from:
            historical_data_url += f"&from={start_from}"
            redis_per = 60

        historical_data = RedisService.get(historical_data_url)
        if historical_data:
            print(f"user cached data for {historical_data_url}")
        else:
            headers = {
                "X-CAP-API-KEY": cls.api_key,
                "CST": cst_token,
                "X-SECURITY-TOKEN": x_security_token,
            }
            print(f"Requesting: {historical_data_url}")
            # Make the request
            response = requests.get(historical_data_url, headers=headers)
            if response.ok:
                historical_data = response.json()
                RedisService.set_value(historical_data_url, 60 * redis_per, historical_data)
            else:
                raise Exception(f"Failed to fetch historical data. Status Code: {response.status_code}",
                                response.text,
                                historical_data_url)
        return cls.convert_to_pd(historical_data)

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
            return gold_data
        else:
            raise Exception("Failed to fetch gold price. Status Code:", response.status_code, response.text)

    @classmethod
    def market_navigation(cls, cst_token, x_security_token, category_id, limit=20):
        market_data = RedisService.get(category_id)
        if market_data:
            print(f"Load cached {category_id}")
        else:
            auth_headers = {
                "X-CAP-API-KEY": cls.api_key,
                "CST": cst_token,
                "X-SECURITY-TOKEN": x_security_token,
            }
            # Fetch the current price for gold
            market_data_url = f"{cls.base_url}/marketnavigation/{category_id}?limit={limit}"  # Adjust the endpoint as necessary
            response = requests.get(market_data_url, headers=auth_headers)
            if response.ok:
                market_data = response.json()
                RedisService.set_value(category_id, 60 * 10, market_data)
            else:
                raise Exception(f"Failed to fetch{category_id}. Status Code:", response.status_code, response.text)
        return market_data

    @staticmethod
    def map_string_to_time_frame(value: str):
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