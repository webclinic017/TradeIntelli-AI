from alpaca.data.timeframe import TimeFrame
from fastapi import Query

from app.data_formatter import DataFormatter
from domain import enums
from domain.indicators import Indicators
from infastructure.fast_api_app import FastAPIApp
from domain.historical_data_retriever import HistoricalDataRetriever
import traceback

app = FastAPIApp.init_app()
historical_data_retriever = HistoricalDataRetriever()


@app.get("/historical-data")
async def get_historical_data(stock: str = Query('BTC'), time_frame: str = Query("1D")):
    try:
        symbol = enums.symbol_map.get(stock.lower())

        historical_data = historical_data_retriever.get_historical_data(stock, time_frame)

        Indicators.add_ema(historical_data)
        Indicators.calculate_resistance_and_support(historical_data)

        return DataFormatter.formate_data(historical_data, symbol)

    except Exception as e:
        traceback.print_exc()
        return []


