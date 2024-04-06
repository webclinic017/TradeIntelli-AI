from fastapi import Query, APIRouter

from app.data_formatter import DataFormatter
from domain import enums
from domain.historical_data_retriever import HistoricalDataRetriever
from domain.indicators import Indicators
import traceback
import requests

router = APIRouter()


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
                              start_date: int = Query(60*24)):
    try:
        historical_data_retriever = HistoricalDataRetriever()
        symbol = enums.symbol_map.get(stock.lower())

        historical_data = historical_data_retriever.get_historical_data(stock, time_frame, start_date)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)
        Indicators.decide_market_direction(historical_data)

        return DataFormatter.formate_data(historical_data, symbol)

    except Exception as e:
        traceback.print_exc()
        return []