from fastapi import Query, APIRouter, HTTPException

from application.data_formatter import DataFormatter
from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
import traceback
import requests
from domain.performance_tester import PerformanceTester
from domain.trades_opportunity_scanner import TradesOpportunityScanner

router = APIRouter()


@router.get("/capital-market-search")
async def market_search(stock: str = Query('BTC')):
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.market_search(CapitalComDataRetriever.api_key, cst_token, x_security_token, stock)


@router.get("/marketnavigation")
async def market_navigation(category_id: str = Query('hierarchy_v1.commons.most_traded'),
                            limit: int = Query(20)):
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.market_navigation(cst_token, x_security_token, category_id, limit=limit)


@router.get("/capital-open-new-position")
async def open_position(stock: str = Query('BTC'),
                        stop_loss: int = Query(20),
                        profit_level: int = Query(20),
                        size: float = Query(0.5)):
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.open_position(cst_token,
                                                 x_security_token,
                                                 stock,
                                                 stop_loss,
                                                 profit_level,
                                                 size)


@router.delete("/positions/{dealId}")
def delete_position(deal_id: str):
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    success = CapitalComDataRetriever.delete_position_at_capital(cst_token,
                                                                 x_security_token,
                                                                 deal_id)
    if success:
        return {"message": "Position deleted successfully."}
    else:
        raise HTTPException(status_code=400, detail="Failed to delete position at Capital.com")


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
        historical_data = HistoricalDataRetriever.get_market_data_and_direction(stock, time_frame)
        PerformanceTester.calculate_profit_all(historical_data)

        return DataFormatter.formate_data(historical_data, stock)

    except Exception:
        traceback.print_exc()
        return []


@router.get("/calculate-success-rate")
async def calculate_success_rate(stock: str = Query('BTC'), period: int = Query(10)):
    return PerformanceTester.calculate_success_rate(stock, period)


@router.get("/scan-trades-opportunities")
async def scan_trades_opportunities():
    return TradesOpportunityScanner.scan_most_trades()

