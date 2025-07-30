import requests
from typing import Dict, List, Union, Optional, Any
from .exceptions import UnirateError, AuthenticationError, RateLimitError, InvalidCurrencyError, InvalidDateError, APIError

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
        json: Optional[Dict] = None,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Any:
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            json (dict, optional): JSON body for POST requests
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            dict or str: Response data (dict for JSON, str for other formats)

        Raises:
            UnirateError: If the API request fails
        """
        if params is None:
            params = {}
        
        # Add API key to all requests
        params['api_key'] = self.api_key
        
        # Add format parameter
        if format != "json":
            params['format'] = format
            
        # Add callback parameter for JSONP
        if callback and format == "json":
            params['callback'] = callback

        try:
            response = self.session.request(
                method=method,
                url=f"{self.BASE_URL}/{endpoint.lstrip('/')}",
                params=params,
                json=json,
                timeout=self.timeout
            )
            
            # Handle different response status codes
            if response.status_code == 400:
                raise InvalidDateError("Invalid request parameters")
            elif response.status_code == 401:
                raise AuthenticationError("Missing or invalid API key")
            elif response.status_code == 404:
                raise InvalidCurrencyError("Currency not found or no data available")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code == 503:
                raise APIError("Service unavailable", response.status_code)
            
            response.raise_for_status()
            
            # Return appropriate format
            if format == "json":
                return response.json()
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            if not isinstance(e, (AuthenticationError, RateLimitError, InvalidCurrencyError, InvalidDateError, APIError)):
                raise UnirateError(f"API request failed: {str(e)}")
            raise

    def get_rate(
        self,
        from_currency: str = "USD",
        to_currency: Optional[str] = None,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[float, Dict[str, float], str]:
        """
        Get exchange rates between currencies.

        Args:
            from_currency (str, optional): Source currency code. Defaults to "USD".
            to_currency (str, optional): Target currency code. If not specified, returns rates for all currencies.
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            float, dict, or str: Exchange rate(s) or formatted response

        Raises:
            UnirateError: If the request fails or currencies are invalid
        """
        params = {
            "from": from_currency.upper()
        }
        
        if to_currency:
            params["to"] = to_currency.upper()

        response = self._make_request("GET", "/api/rates", params=params, format=format, callback=callback)
        
        if format != "json":
            return response
            
        if to_currency:
            return float(response["rate"])
        else:
            return {currency: float(rate) for currency, rate in response["rates"].items()}

    def convert(
        self,
        to_currency: str,
        amount: Union[int, float] = 1,
        from_currency: str = "USD",
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[float, Dict[str, float], str]:
        """
        Convert an amount from one currency to another.

        Args:
            to_currency (str): Target currency code
            amount (int or float, optional): Amount to convert. Defaults to 1.
            from_currency (str, optional): Source currency code. Defaults to "USD".
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            float, dict, or str: Converted amount(s) or formatted response

        Raises:
            UnirateError: If the conversion fails
        """
        params = {
            "amount": amount,
            "from": from_currency.upper(),
            "to": to_currency.upper()
        }

        response = self._make_request("GET", "/api/convert", params=params, format=format, callback=callback)
        
        if format != "json":
            return response
            
        if "result" in response:
            return float(response["result"])
        else:
            return {currency: float(result) for currency, result in response["results"].items()}

    def get_supported_currencies(
        self,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[List[str], str]:
        """
        Get a list of supported currencies.

        Args:
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            list or str: List of currency codes or formatted response

        Raises:
            UnirateError: If the request fails
        """
        response = self._make_request("GET", "/api/currencies", format=format, callback=callback)
        
        if format != "json":
            return response
            
        return response["currencies"]

    def get_historical_rate(
        self,
        date: str,
        amount: Union[int, float] = 1,
        from_currency: str = "USD",
        to_currency: Optional[str] = None,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[float, Dict[str, float], str]:
        """
        Get historical exchange rate for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format
            amount (int or float, optional): Amount to convert. Defaults to 1.
            from_currency (str, optional): Source currency code. Defaults to "USD".
            to_currency (str, optional): Target currency code. If not specified, returns rates for all currencies.
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            float, dict, or str: Historical exchange rate(s) or formatted response

        Raises:
            UnirateError: If the request fails or date/currencies are invalid
        """
        params = {
            "date": date,
            "amount": amount,
            "from": from_currency.upper()
        }
        
        if to_currency:
            params["to"] = to_currency.upper()

        response = self._make_request("GET", "/api/historical/rates", params=params, format=format, callback=callback)
        
        if format != "json":
            return response
            
        if to_currency:
            if amount == 1:
                return float(response["rate"])
            else:
                return float(response["result"])
        else:
            if amount == 1:
                return {currency: float(rate) for currency, rate in response["rates"].items()}
            else:
                return {currency: float(result) for currency, result in response["results"].items()}

    def get_historical_rates(
        self,
        date: str,
        amount: Union[int, float] = 1,
        base_currency: str = "USD",
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[Dict[str, float], str]:
        """
        Get historical exchange rates for a specific date (all rates for a base currency).

        Args:
            date (str): Date in YYYY-MM-DD format
            amount (int or float, optional): Amount to convert. Defaults to 1.
            base_currency (str, optional): Base currency code. Defaults to "USD".
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            dict or str: Dictionary containing all exchange rates for the specified date or formatted response

        Raises:
            UnirateError: If the request fails or date/currency is invalid
        """
        return self.get_historical_rate(
            date=date, 
            amount=amount, 
            from_currency=base_currency, 
            format=format, 
            callback=callback
        )

    def convert_historical(
        self,
        amount: Union[int, float],
        from_currency: str,
        to_currency: str,
        date: str,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[float, str]:
        """
        Convert amount using historical exchange rate for a specific date.

        Args:
            amount (int or float): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            date (str): Date in YYYY-MM-DD format
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            float or str: Converted amount using historical rate or formatted response

        Raises:
            UnirateError: If the conversion fails
        """
        return self.get_historical_rate(
            date=date,
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            format=format,
            callback=callback
        )

    def get_time_series(
        self,
        start_date: str,
        end_date: str,
        amount: Union[int, float] = 1,
        base_currency: str = "USD",
        currencies: Optional[List[str]] = None,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[Dict[str, Dict[str, float]], str]:
        """
        Get time series data for a date range with optional amount conversion (max 5 years).

        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            amount (int or float, optional): Amount to convert. Defaults to 1.
            base_currency (str, optional): Base currency code. Defaults to "USD".
            currencies (list, optional): List of currency codes to retrieve. If not specified, returns all currencies.
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            dict or str: Dictionary containing time series data with dates as keys or formatted response

        Raises:
            UnirateError: If the request fails or dates/currencies are invalid
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "amount": amount,
            "base": base_currency.upper()
        }
        
        if currencies:
            params["currencies"] = ",".join([curr.upper() for curr in currencies])

        response = self._make_request("GET", "/api/historical/timeseries", params=params, format=format, callback=callback)
        
        if format != "json":
            return response
            
        return response["data"]

    def get_historical_limits(
        self,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[Dict[str, Any], str]:
        """
        Get information about available historical data limits per currency.

        Args:
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            dict or str: Dictionary containing historical data limits information or formatted response

        Raises:
            UnirateError: If the request fails
        """
        response = self._make_request("GET", "/api/historical/limits", format=format, callback=callback)
        
        if format != "json":
            return response
            
        return response

    def get_vat_rates(
        self,
        country: Optional[str] = None,
        format: str = "json",
        callback: Optional[str] = None
    ) -> Union[Dict[str, Any], str]:
        """
        Get VAT rates for all countries or a specific country.

        Args:
            country (str, optional): Two-letter country code (e.g., "DE", "FR") for specific country rates
            format (str, optional): Response format (json, xml, csv, tsv). Defaults to "json".
            callback (str, optional): JSONP callback function name

        Returns:
            dict or str: Dictionary containing VAT rates information or formatted response

        Raises:
            UnirateError: If the request fails
        """
        params = {}
        if country:
            params["country"] = country.upper()

        response = self._make_request("GET", "/api/vat/rates", params=params, format=format, callback=callback)
        
        if format != "json":
            return response
            
        return response 