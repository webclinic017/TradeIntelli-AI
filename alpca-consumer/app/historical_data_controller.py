import json

from fastapi import Query, APIRouter

from app.data_formatter import DataFormatter
from domain.capital_com_data_retriever import CapitalComDataRetriever
from domain.historical_data_retriever import HistoricalDataRetriever
from domain.indicators import Indicators
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

router = APIRouter()


def send_email(stock, subject: str = None, body: str = None):
    # Set up the email server and the message
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "omerahmed41@gmail.com"
    receiver_email = "omerahmed41@gmail.com"
    password = "yess nais wjfx gemg"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    if not subject:
        subject = f"Trading alert: {stock}"
    message["Subject"] = subject

    # Add body to email
    if not body:
        body = f"Buy {stock}"

    message.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP(smtp_server, port)

    try:
        # Connect to the server and send the email
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


@router.get("/capital-market-search")
async def market_search(stock: str = Query('BTC')):
    # symbol = "Bitcoin"
    cst_token, x_security_token = CapitalComDataRetriever.create_capital_com_session()
    return CapitalComDataRetriever.market_search(CapitalComDataRetriever.api_key, cst_token, x_security_token, stock)


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
        Indicators.calculate_resistance_and_support(historical_data)
        Indicators.decide_market_direction(historical_data)
        return DataFormatter.formate_data(historical_data, stock)

    except Exception:
        traceback.print_exc()
        return []
