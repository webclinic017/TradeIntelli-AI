from fastapi import Query, APIRouter

from application.data_formatter import DataFormatter
from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
from domain.indicators import Indicators
import traceback
import requests
from domain.market_direction_detector import MarketDirectionDetector
from domain.performance_tester import PerformanceTester


router = APIRouter()


@router.get("/capital-market-search")
async def market_search(stock: str = Query('BTC')):
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.market_search(CapitalComDataRetriever.api_key, cst_token, x_security_token, stock)


@router.get("/capital-open-position")
async def get_open_positions():
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.get_open_positions(cst_token, x_security_token)


@router.get("/capital-account_info")
async def get_account_info():
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    account_info_url = f"{CapitalComDataRetriever.base_url}/accounts"
    headers = {
        "X-SECURITY-TOKEN": x_security_token,
        "CST": cst_token,
        "Content-Type": "application/json"
    }

    positions_response = requests.get(account_info_url, headers=headers)
    open_positions = positions_response.json()
    print(f"open_positions: {open_positions}")
    return open_positions

@router.get("/stocks-movers")
async def get_historical_data():
    url = "https://data.alpaca.markets/v1beta1/screener/stocks/movers?top=10"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "PKM1OG4ZMBZTQC75B5TF",
        "APCA-API-SECRET-KEY": "QaLbJYSuOfJ2Yj9dl88xceijOJXLOoa8Lj7SnrXe"
    }

    response = requests.get(url, headers=headers)

    return response.json()


@router.get("/historical-data")
async def get_historical_data(stock: str = Query('BTC'), time_frame: str = Query("1H"),
                              start_date: int = Query(60 * 24)):
    try:
        historical_data_retriever = HistoricalDataRetriever()
        historical_data = historical_data_retriever.get_historical_data(stock, time_frame, start_date)

        Indicators.add_ema(historical_data)
        Indicators.add_macd(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)
        MarketDirectionDetector.support_and_resistance(historical_data)
        MarketDirectionDetector.ema_direction(historical_data)
        MarketDirectionDetector.macd_direction(historical_data)

        historical_data["s_r_profit"] = PerformanceTester.calculate_profit(historical_data, indicator="market_direction")
        historical_data["ema_profit"] = PerformanceTester.calculate_profit(historical_data, indicator="ema_market_direction")
        historical_data["macd_profit"] = PerformanceTester.calculate_profit(historical_data, indicator="macd_market_direction")
        return DataFormatter.formate_data(historical_data, stock)

    except Exception:
        traceback.print_exc()
        return []
