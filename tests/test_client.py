"""Unit tests for upcdatabase client"""

import unittest
from unittest.mock import Mock, patch

import requests

from upcdatabase import UPCDatabase, UPCDatabaseError


class TestUPCDatabase(unittest.TestCase):
    """Test cases for UPCDatabase client"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    def test_initialization(self):
        """Test client initialization"""
        client = UPCDatabase(api_key="test_key")
        self.assertEqual(client.api_key, "test_key")

    def test_initialization_empty_key(self):
        """Test that empty API key raises error"""
        with self.assertRaises(ValueError):
            UPCDatabase(api_key="")

    @patch("upcdatabase.client.requests.Session.get")
    def test_lookup_success(self, mock_get):
        """Test successful product lookup"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "name": "Test Product",
            "upc": "036000291204",
            "manufacturer": "Test Co",
            "price": "9.99",
        }
        mock_get.return_value = mock_response

        result = self.client.lookup("036000291204")

        self.assertEqual(result["name"], "Test Product")
        self.assertEqual(result["upc"], "036000291204")
        mock_get.assert_called_once()

    @patch("upcdatabase.client.requests.Session.get")
    def test_search_success(self, mock_get):
        """Test successful product search"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [{"name": "Product 1", "upc": "123"}, {"name": "Product 2", "upc": "456"}]
        }
        mock_get.return_value = mock_response

        result = self.client.search("cola")

        self.assertEqual(len(result["items"]), 2)
        mock_get.assert_called_once()

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_latest_currency(self, mock_get):
        """Test getting latest currency rates"""
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"USD": 1.0}}
        mock_get.return_value = mock_response

        result = self.client.get_latest_currency()

        self.assertIn("rates", result)
        mock_get.assert_called_once()

    def test_context_manager(self):
        """Test context manager functionality"""
        with UPCDatabase(api_key="test_key") as client:
            self.assertEqual(client.api_key, "test_key")

    def test_api_key_in_params(self):
        """Test that API key is added to request params"""
        with patch("upcdatabase.client.requests.Session.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            self.client.lookup("123")

            # Check that the get call includes the API key
            call_args = mock_get.call_args
            self.assertIn("key", call_args[1]["params"])
            self.assertEqual(call_args[1]["params"]["key"], self.api_key)


class TestUPCDatabaseError(unittest.TestCase):
    """Test error handling"""

    def test_error_inheritance(self):
        """Test that UPCDatabaseError is an Exception"""
        self.assertTrue(issubclass(UPCDatabaseError, Exception))

    def test_error_message(self):
        """Test error message"""
        error = UPCDatabaseError("Test error")
        self.assertEqual(str(error), "Test error")


class TestUPCDatabaseRequestErrors(unittest.TestCase):
    """Test request error handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    @patch("upcdatabase.client.requests.Session.get")
    def test_http_error_handling(self, mock_get):
        """Test HTTP error handling"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = Mock(
            raise_for_status=Mock(side_effect=requests.exceptions.HTTPError(response=mock_response))
        )

        with self.assertRaises(UPCDatabaseError):
            self.client.lookup("123")

    @patch("upcdatabase.client.requests.Session.get")
    def test_request_exception_handling(self, mock_get):
        """Test general request exception handling"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with self.assertRaises(UPCDatabaseError):
            self.client.lookup("123")


class TestCurrencyEndpoints(unittest.TestCase):
    """Test currency API endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_currency_history(self, mock_get):
        """Test getting historical currency rates"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "date": "2025-01-15",
            "rates": {"USD": 1.0, "EUR": 0.95},
        }
        mock_get.return_value = mock_response

        result = self.client.get_currency_history("2025-01-15")

        self.assertTrue(result["success"])
        self.assertEqual(result["date"], "2025-01-15")
        self.assertIn("rates", result)
        mock_get.assert_called_once()

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_currency_symbols(self, mock_get):
        """Test getting currency symbols"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "symbols": {"USD": "US dollar", "EUR": "Euro"},
        }
        mock_get.return_value = mock_response

        result = self.client.get_currency_symbols()

        self.assertTrue(result["success"])
        self.assertIn("symbols", result)
        mock_get.assert_called_once()


class TestBitcoinEndpoints(unittest.TestCase):
    """Test Bitcoin API endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_latest_bitcoin(self, mock_get):
        """Test getting latest Bitcoin rate"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "timestamp": 1000000,
            "date": "2025-02-05",
            "rates": {"high": "28000", "low": "27000", "latest": "27500"},
        }
        mock_get.return_value = mock_response

        result = self.client.get_latest_bitcoin()

        self.assertTrue(result["success"])
        self.assertIn("rates", result)
        mock_get.assert_called_once()

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_bitcoin_history(self, mock_get):
        """Test getting historical Bitcoin rate"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "timestamp": 1000000,
            "date": "2025-01-15",
            "rates": {"high": "26000", "low": "25000", "close": "25500"},
        }
        mock_get.return_value = mock_response

        result = self.client.get_bitcoin_history("2025-01-15")

        self.assertTrue(result["success"])
        self.assertEqual(result["date"], "2025-01-15")
        mock_get.assert_called_once()


class TestQRCodeEndpoint(unittest.TestCase):
    """Test QR code generation endpoint"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    @patch("upcdatabase.client.requests.Session.get")
    def test_generate_qr(self, mock_get):
        """Test QR code generation"""
        mock_response = Mock()
        mock_response.json.return_value = {"image": "base64_encoded_image_data"}
        mock_get.return_value = mock_response

        result = self.client.generate_qr("https://example.com")

        self.assertIsNotNone(result)
        mock_get.assert_called_once()

        # Verify the URL include base64 encoded text
        call_args = mock_get.call_args
        self.assertIn("/qr/", call_args[0][0])


class TestAccountEndpoint(unittest.TestCase):
    """Test account information endpoint"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)

    @patch("upcdatabase.client.requests.Session.get")
    def test_get_account_info(self, mock_get):
        """Test getting account information"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "email": "test@example.com",
            "score": "100",
            "api_remain": {"lookups": "500", "search": "100"},
            "api_limits": {"lookups": 1000, "searches": 200},
        }
        mock_get.return_value = mock_response

        result = self.client.get_account_info()

        self.assertTrue(result["success"])
        self.assertEqual(result["email"], "test@example.com")
        self.assertIn("api_remain", result)
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
