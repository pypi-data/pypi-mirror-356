import requests
import json
import pandas as pd
from typing import Optional
from ..config import BASE_REST_URL
from .authenticator import Authenticator

class HistoricalData:
    """
    This class provides historical data from OTC Market and CETIP Market.

    * Main use case:

    >>> from btgsolutions_otcmarkets import HistoricalData
    >>> historical_data = HistoricalData(
    >>>     api_key='YOUR_API_KEY',
    >>> )

    >>> historical_data.get_otc_trades(
    >>>     ticker='PLSB1A',
    >>>     start_date='2024-09-01',
    >>>     end_date='2024-10-01',
    >>> )

    >>> historical_data.get_cetip_grouped_trades(
    >>>     ticker='PLSB1A',
    >>>     granularity='monthly'
    >>> )

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.
    """
    def __init__(
        self,
        api_key: Optional[str]
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.headers = {"authorization": f"Bearer {self.token}"}


    def get_otc_tickers(
        self,
    ):
        """
        This method get the available tickers for getting OTC trades. Includes all ticker that has at least one trade in OTC.
        """

        url = f"{BASE_REST_URL}/api/v1/btg-otc-mkts/historical/trades/tickers_otc"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data

        response = json.loads(response.text)
        raise Exception(f'Error: {response.get("ApiClientError", "")}.\nSuggested action: {response.get("SuggestedAction", "")}.')

    def get_cetip_tickers(
        self,
    ):
        """
        This method get the available tickers for getting CETIP trades. Includes all ticker that has at least one trade in our CETIP database.
        """

        url = f"{BASE_REST_URL}/api/v1/btg-otc-mkts/historical/trades/tickers_cetip"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data

        response = json.loads(response.text)
        raise Exception(f'Error: {response.get("ApiClientError", "")}.\nSuggested action: {response.get("SuggestedAction", "")}.')

    def get_otc_trades(
        self,
        ticker: str,
        start_date: str = "1900-01-01",
        end_date: str = "2100-01-01",
    ):
        """
        This method get the historical trades of BTG OTC Market by ticker.

        Parameters
        ----------------
        ticker: string
            Asset ticker.
            Field is required. Example: 'PLSB1A'.
        start_date: str
            Start date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "1900-01-01".
        end_date: str
            Final date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "2100-01-01".
        """

        url = f"{BASE_REST_URL}/api/v1/btg-otc-mkts/historical/trades/otc_trades?ticker={ticker}"

        if start_date:
            url += f"&start={start_date}T00:00:00"
        if end_date:
            url += f"&end={end_date}T23:59:59"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data

        response = json.loads(response.text)
        raise Exception(f'Error: {response.get("ApiClientError", "")}.\nSuggested action: {response.get("SuggestedAction", "")}.')
    
    def get_otc_grouped_trades(
        self,
        ticker: str,
        start_date: str = "1900-01-01",
        end_date: str = "2100-01-01",
        granularity: str = "daily",
    ):
        """
        This method get the historical trades of BTG OTC Market by ticker and aggregated daily, weekly or monthly.

        Parameters
        ----------------
        ticker: string
            Asset ticker.
            Field is required. Example: 'PLSB1A'.
        start_date: str
            Start date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "1900-01-01".
        end_date: str
            Final date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "2100-01-01".
        granularity: str
            Granularity of the data (daily, weekly, monthly)
            Field is not required. Default: daily.
        """

        url = f"{BASE_REST_URL}/api/v1/btg-otc-mkts/historical/trades/otc_grouped_trades?ticker={ticker}"

        if start_date:
            url += f"&start={start_date}T00:00:00"
        if end_date:
            url += f"&end={end_date}T23:59:59"
        if granularity:
            url += f"&granularity={granularity}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data

        response = json.loads(response.text)
        raise Exception(f'Error: {response.get("ApiClientError", "")}.\nSuggested action: {response.get("SuggestedAction", "")}.')
    
    def get_cetip_grouped_trades(
        self,
        ticker: str,
        start_date: str = "1900-01-01",
        end_date: str = "2100-01-01",
        granularity: str = "daily",
    ):
        """
        This method get the historical trades of CETIP Market by ticker and aggregated daily, weekly or monthly.

        Parameters
        ----------------
        ticker: string
            Asset ticker.
            Field is required. Example: 'PLSB1A'.
        start_date: str
            Start date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "1900-01-01".
        end_date: str
            Final date-time in YYYY-MM-DD format (e.g., 2024-01-01).
            Field is not required. Default: "2100-01-01".
        granularity: str
            Granularity of the data (daily, weekly, monthly)
            Field is not required. Default: daily.
        """

        url = f"{BASE_REST_URL}/api/v1/btg-otc-mkts/historical/trades/cetip_grouped_trades?ticker={ticker}"

        if start_date:
            url += f"&start={start_date}T00:00:00"
        if end_date:
            url += f"&end={end_date}T23:59:59"
        if granularity:
            url += f"&granularity={granularity}"

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data

        response = json.loads(response.text)
        raise Exception(f'Error: {response.get("ApiClientError", "")}.\nSuggested action: {response.get("SuggestedAction", "")}.')