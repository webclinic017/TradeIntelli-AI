from fastapi import Query, APIRouter

from app.data_formatter import DataFormatter
from domain import enums
from domain.historical_data_retriever import HistoricalDataRetriever
from domain.indicators import Indicators
import traceback


router = APIRouter()


@router.get("/historical-data")
async def get_historical_data(stock: str = Query('BTC'), time_frame: str = Query("1D"),
                              start_date: int = Query(30)):
    try:
        historical_data_retriever = HistoricalDataRetriever()
        symbol = enums.symbol_map.get(stock.lower())

        historical_data = historical_data_retriever.get_historical_data(stock, time_frame, start_date)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)

        return DataFormatter.formate_data(historical_data, symbol)

    except Exception as e:
        traceback.print_exc()
        return []