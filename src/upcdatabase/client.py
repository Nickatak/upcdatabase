"""Main UPC Database API client"""

from typing import Any, Dict, Optional
from urllib.parse import quote

import requests


class UPCDatabaseError(Exception):
    """Base exception for UPC Database errors"""

    pass


class UPCDatabase:
    """Client for the UPC Database API

    Provides access to product lookups, search, currency data, and more.

    Args:
        api_key: Your UPC Database API key from https://upcdatabase.org/apikeys

    Example:
        >>> client = UPCDatabase(api_key="your_api_key")
        >>> product = client.lookup("036000291204")
        >>> print(product["name"])
    """

    BASE_URL = "https://api.upcdatabase.org"

    def __init__(self, api_key: str):
        """Initialize the API client

        Args:
            api_key: Your UPC Database API key

        Raises:
            ValueError: If api_key is empty
        """
        if not api_key:
            raise ValueError("api_key cannot be empty")

        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "upcdatabase-python/0.1.0"})

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an API request

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Response JSON as dictionary

        Raises:
            UPCDatabaseError: If API returns an error
            requests.RequestException: If network request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        # Add bearer token to headers
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if params is None:
            params = {}

        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise UPCDatabaseError(
                f"API request failed: {e.response.status_code} - {e.response.text}"
            )
        except requests.exceptions.RequestException as e:
            raise UPCDatabaseError(f"Request failed: {str(e)}")

    def lookup(self, upc: str) -> Dict[str, Any]:
        """Look up a product by UPC/EAN code

        Args:
            upc: The UPC or EAN code to lookup

        Returns:
            Dict containing product information with keys:
                - success (bool): Request success status
                - barcode (str): Product barcode/UPC
                - title (str): Product name
                - alias (str): Product short name
                - description (str): Product description
                - brand (str): Brand name
                - manufacturer (str): Manufacturer name
                - mpn (str): Manufacturer part number
                - msrp (str): Suggested retail price
                - ASIN (str): Amazon identifier
                - category (str): Product category
                - metadata (dict): Additional product metadata
                - stores (list): Retail store information
                - images (list): Product images
                - reviews (dict): Review ratings

        Example:
            >>> product = client.lookup("036000291204")
            >>> print(product["title"])
            >>> print(product["manufacturer"])
            >>> print(product["msrp"])

        Raises:
            UPCDatabaseError: If lookup fails or product not found
        """
        return self._make_request(f"/product/{quote(upc)}")

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search for products

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)

        Returns:
            Dict containing search results with keys:
                - success (bool): Request success status
                - timestamp (int): Unix timestamp
                - results (int): Number of results found
                - items (list): List of product dicts (barcode, title, alias, description)

        Example:
            >>> results = client.search("coca cola")
            >>> print(f"Found {results['results']} results")
            >>> for item in results.get("items", []):
            ...     print(f"{item['title']} - {item['barcode']}")

        Raises:
            UPCDatabaseError: If search fails
        """
        params = {"s": query, "limit": limit}
        return self._make_request("/search", params=params)

    def get_latest_currency(self) -> Dict[str, Any]:
        """Get latest currency exchange rates

        Returns:
            Dict containing currency rates with keys:
                - success (bool): Request success status
                - date (str): Date of rates
                - timestamp (int): Unix timestamp
                - base (str): Base currency code
                - rates (dict): Currency codes mapped to exchange rates (float)

        Example:
            >>> rates = client.get_latest_currency()
            >>> print(f"USD/EUR: {rates['rates']['EUR']}")

        Raises:
            UPCDatabaseError: If request fails
        """
        return self._make_request("/currency/latest")

    def get_currency_history(self, date: str) -> Dict[str, Any]:
        """Get historical currency exchange rates

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            Dict containing historical currency rates with keys:
                - success (bool): Request success status
                - date (str): Date of rates
                - timestamp (int): Unix timestamp
                - base (str): Base currency code
                - rates (dict): Currency codes mapped to exchange rates (float)

        Example:
            >>> history = client.get_currency_history("2025-01-15")
            >>> print(f"On 2025-01-15, USD/EUR was {history['rates']['EUR']}")

        Raises:
            UPCDatabaseError: If request fails
        """
        params = {"date": date}
        return self._make_request("/currency/history", params=params)

    def get_currency_symbols(self) -> Dict[str, Any]:
        """Get list of supported currency symbols

        Returns:
            Dict containing currency symbols with keys:
                - success (bool): Request success status
                - timestamp (int): Unix timestamp
                - symbols (dict): Currency codes mapped to full names

        Example:
            >>> symbols = client.get_currency_symbols()
            >>> print(symbols["symbols"]["USD"])

        Raises:
            UPCDatabaseError: If request fails
        """
        return self._make_request("/currency/symbols")

    def get_latest_bitcoin(self) -> Dict[str, Any]:
        """Get latest Bitcoin exchange rate

        Returns:
            Dict containing Bitcoin rates with keys:
                - success (bool): Request success status
                - timestamp (int): Unix timestamp
                - date (str): Current date
                - base (str): Base currency (USD)
                - rates (dict): Bitcoin rates with high, low, latest (string values)

        Example:
            >>> btc = client.get_latest_bitcoin()
            >>> print(f"BTC latest: ${btc['rates']['latest']}")

        Raises:
            UPCDatabaseError: If request fails
        """
        return self._make_request("/bitcoin/latest")

    def get_bitcoin_history(self, date: str) -> Dict[str, Any]:
        """Get historical Bitcoin exchange rate

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            Dict containing historical Bitcoin rates with keys:
                - success (bool): Request success status
                - timestamp (int): Unix timestamp
                - date (str): Date of rates
                - base (str): Base currency (USD)
                - rates (dict): Bitcoin rates with high, low, close (string values)

        Example:
            >>> btc_history = client.get_bitcoin_history("2025-01-15")
            >>> print(f"BTC high: ${btc_history['rates']['high']}")

        Raises:
            UPCDatabaseError: If request fails
        """
        params = {"date": date}
        return self._make_request("/bitcoin/history", params=params)

    def generate_qr(self, text: str) -> Dict[str, Any]:
        """Generate a QR code

        Args:
            text: Text/data to encode in the QR code

        Returns:
            PNG image binary data as response (Content-Type: image/png)

        Example:
            >>> qr = client.generate_qr("https://example.com")
            >>> # Returns PNG image data

        Raises:
            UPCDatabaseError: If QR generation fails
        """
        import base64

        encoded_text = base64.b64encode(text.encode()).decode()
        return self._make_request(f"/qr/{encoded_text}")

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information

        Returns:
            Dict containing account information with keys:
                - success (bool): Request success status
                - email (str): Account email
                - registered (int): Registration timestamp
                - active (int): Active timestamp
                - score (str): Account score
                - banned (bool): Account ban status
                - apikey_count (str): Number of API keys
                - products (dict): Added and modified product counts
                - api_subscription (dict): Subscription details
                - api_limits (dict): API rate limits
                - api_remain (dict): Remaining API requests
                - api_requests (str): Total API requests made
                - timestamp (int): Current timestamp

        Example:
            >>> account = client.get_account_info()
            >>> print(f"Lookups remaining: {account['api_remain']['lookups']}")

        Raises:
            UPCDatabaseError: If request fails
        """
        return self._make_request("/account")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.session.close()
