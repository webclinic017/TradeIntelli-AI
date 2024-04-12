import os
from dotenv import load_dotenv

load_dotenv()


class CapitalCom:
    base_url = "https://demo-api-capital.backend-capital.com/api/v1"
    api_key = os.getenv('CAPITAL_COM_API_KEY')
