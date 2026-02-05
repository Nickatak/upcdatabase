"""Tests for the upcdatabase library"""

import unittest
from unittest.mock import Mock, patch

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


if __name__ == "__main__":
    unittest.main()
