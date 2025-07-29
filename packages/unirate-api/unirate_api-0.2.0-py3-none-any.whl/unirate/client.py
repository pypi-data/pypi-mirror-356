import requests
from typing import Dict, List, Union, Optional
from .exceptions import UnirateError

class UnirateClient:
    """
    Main client class for interacting with the Unirate API.
    """
    
    BASE_URL = "https://api.unirateapi.com"
    
    def __init__(
        self,
        api_key: str,
        timeout: int = 30
    ):
        """
        Initialize the Unirate client.

        Args:
            api_key (str): Your API key for authentication
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'unirate-python/{__import__("unirate").__version__}'
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict:
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            json (dict, optional): JSON body for POST requests

        Returns:
            dict: Response data

        Raises:
            UnirateError: If the API request fails
        """
        if params is None:
            params = {}
        
        # Add API key to all requests
        params['api_key'] = self.api_key

        try:
            response = self.session.request(
                method=method,
                url=f"{self.BASE_URL}/{endpoint.lstrip('/')}",
                params=params,
                json=json,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UnirateError(f"API request failed: {str(e)}")

    def get_rate(
        self,
        from_currency: str,
        to_currency: str
    ) -> float:
        """
        Get the exchange rate between two currencies.

        Args:
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")

        Returns:
            float: Exchange rate

        Raises:
            UnirateError: If the request fails or currencies are invalid
        """
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper()
        }

        response = self._make_request("GET", "/api/rates", params=params)
        return float(response["rate"])

    def convert(
        self,
        amount: Union[int, float],
        from_currency: str,
        to_currency: str
    ) -> float:
        """
        Convert an amount from one currency to another.

        Args:
            amount (int or float): Amount to convert
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")

        Returns:
            float: Converted amount

        Raises:
            UnirateError: If the conversion fails
        """
        params = {
            "amount": amount,
            "from": from_currency.upper(),
            "to": to_currency.upper()
        }

        response = self._make_request("GET", "/api/convert", params=params)
        return float(response["result"])

    def get_supported_currencies(self) -> List[str]:
        """
        Get a list of supported currencies.

        Returns:
            list: List of currency codes

        Raises:
            UnirateError: If the request fails
        """
        response = self._make_request("GET", "/api/currencies")
        return response["currencies"]

    def get_historical_rate(
        self,
        from_currency: str,
        to_currency: str,
        date: str
    ) -> float:
        """
        Get historical exchange rate for a specific date.

        Args:
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")
            date (str): Date in YYYY-MM-DD format

        Returns:
            float: Historical exchange rate

        Raises:
            UnirateError: If the request fails or date/currencies are invalid
        """
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "date": date
        }

        response = self._make_request("GET", "/api/historical/rates", params=params)
        return float(response["rate"])

    def get_historical_rates(
        self,
        base_currency: str,
        date: str
    ) -> Dict[str, float]:
        """
        Get historical exchange rates for a specific date (all rates for a base currency).

        Args:
            base_currency (str): Base currency code (e.g., "USD")
            date (str): Date in YYYY-MM-DD format

        Returns:
            dict: Dictionary containing all exchange rates for the specified date

        Raises:
            UnirateError: If the request fails or date/currency is invalid
        """
        params = {
            "from": base_currency.upper(),
            "date": date
        }

        response = self._make_request("GET", "/api/historical/rates", params=params)
        return {currency: float(rate) for currency, rate in response["rates"].items()}

    def convert_historical(
        self,
        amount: Union[int, float],
        from_currency: str,
        to_currency: str,
        date: str
    ) -> float:
        """
        Convert amount using historical exchange rate for a specific date.

        Args:
            amount (int or float): Amount to convert
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")
            date (str): Date in YYYY-MM-DD format

        Returns:
            float: Converted amount using historical rate

        Raises:
            UnirateError: If the conversion fails
        """
        # Get historical rate and multiply by amount since there's no direct convert endpoint
        rate = self.get_historical_rate(from_currency, to_currency, date)
        return amount * rate

    def get_time_series(
        self,
        from_currency: str,
        to_currency: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, float]:
        """
        Get time series data for a currency pair over a date range.

        Args:
            from_currency (str): Source currency code (e.g., "USD")
            to_currency (str): Target currency code (e.g., "EUR")
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format

        Returns:
            dict: Dictionary containing time series data with dates as keys

        Raises:
            UnirateError: If the request fails or dates/currencies are invalid
        """
        params = {
            "base": from_currency.upper(),
            "currencies": to_currency.upper(),
            "start_date": start_date,
            "end_date": end_date
        }

        response = self._make_request("GET", "/api/historical/timeseries", params=params)
        return {date: float(currency_rates[to_currency.upper()]) for date, currency_rates in response["data"].items()} 