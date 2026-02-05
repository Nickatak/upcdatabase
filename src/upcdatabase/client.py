"""Main UPC Database API client"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import quote


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
        self.session.headers.update({
            "User-Agent": "upcdatabase-python/0.1.0"
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
        
        # Add API key to params
        if params is None:
            params = {}
        params["key"] = self.api_key
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise UPCDatabaseError(f"API request failed: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise UPCDatabaseError(f"Request failed: {str(e)}")
    
    def lookup(self, upc: str) -> Dict[str, Any]:
        """Look up a product by UPC/EAN code
        
        Args:
            upc: The UPC or EAN code to lookup
            
        Returns:
            Product information dict with keys: success (bool), barcode (str), title (str),
            alias (str), description (str), brand (str), manufacturer (str), mpn (str),
            msrp (str), ASIN (str), category (str), metadata (dict), stores (list),
            images (list), reviews (dict)
            
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
            Dict with keys: success (bool), timestamp (int), results (int),
            items (list of dicts with barcode, title, alias, description)
            
        Example:
            >>> results = client.search("coca cola")
            >>> print(f"Found {results['results']} results")
            >>> for item in results.get("items", []):
            ...     print(f"{item['title']} - {item['barcode']}")
            
        Raises:
            UPCDatabaseError: If search fails
        """
        params = {
            "s": query,
            "limit": limit
        }
        return self._make_request("/search", params=params)
    
    def get_latest_currency(self) -> Dict[str, Any]:
        """Get latest currency exchange rates
        
        Returns:
            Dict with keys: success (bool), date (str), timestamp (int), base (str),
            rates (dict with currency codes as keys and exchange rates as float values)
            
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
            Dict with keys: success (bool), date (str), timestamp (int), base (str),
            rates (dict with currency codes as keys and exchange rates as float values)
            
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
            Dict with keys: success (bool), timestamp (int),
            symbols (dict with currency codes as keys and full names as values)
            
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
            Dict with keys: success (bool), timestamp (int), date (str), base (str),
            rates (dict with high, low, latest as string values)
            
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
            Dict with keys: success (bool), timestamp (int), date (str), base (str),
            rates (dict with high, low, close as string values)
            
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
            Dict with keys: success (bool), email (str), registered (int), active (int),
            score (str), banned (bool), apikey_count (str), products (dict),
            api_subscription (dict), api_limits (dict), api_remain (dict),
            api_requests (str), timestamp (int)
            
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
