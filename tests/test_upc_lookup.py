"""Test UPC lookup for testing code UPC"""

import unittest
from unittest.mock import Mock, patch

from upcdatabase import UPCDatabase


class TestUPCLookup(unittest.TestCase):
    """Test cases for UPC lookup functionality.

    This test suite validates the UPC lookup endpoint for the specific test UPC code
    0111222333446, which is a special testing code provided by the UPC Database API.

    The tests verify:
    - Successful product lookup by UPC code
    - Correct parsing of API response data
    - Bearer token authentication is properly sent
    - API endpoint is called with the correct URL format
    - Response data matches expected structure and values for the testing code

    Test UPC: 0111222333446
    Product: UPC Database Testing Code (used for testing API integration)
    MSRP: $123.45
    """

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = UPCDatabase(api_key=self.api_key)
        self.test_upc = "0111222333446"
        self.expected_response = {
            "added_time": "2011-06-03 19:45:37",
            "modified_time": "2020-03-17 14:59:12",
            "title": "UPC Database Testing Code",
            "alias": "Testing Code",
            "description": "http://upcdatabase.org/code/0111222333446",
            "brand": "",
            "manufacturer": "",
            "msrp": "123.45",
            "ASIN": "",
            "category": "",
            "categories": "",
            "stores": [],
            "barcode": "0111222333446",
            "success": True,
            "timestamp": 1770332489,
            "images": [],
            "metadata": {"msrp": "123.45", "unit": "1 code"},
            "metanutrition": None,
        }

    @patch("upcdatabase.client.requests.Session.get")
    def test_lookup_testing_upc(self, mock_get):
        """Test lookup of UPC 0111222333446 returns expected data"""
        mock_response = Mock()
        mock_response.json.return_value = self.expected_response
        mock_get.return_value = mock_response

        result = self.client.lookup(self.test_upc)

        # Verify the response matches expected
        self.assertEqual(result["barcode"], "0111222333446")
        self.assertEqual(result["title"], "UPC Database Testing Code")
        self.assertEqual(result["alias"], "Testing Code")
        self.assertEqual(result["msrp"], "123.45")
        self.assertTrue(result["success"])
        self.assertEqual(result, self.expected_response)

        # Verify API was called with correct endpoint
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn("/product/0111222333446", call_args[0][0])
        # Verify bearer token was used
        self.assertIn("Authorization", call_args[1]["headers"])
        self.assertEqual(call_args[1]["headers"]["Authorization"], f"Bearer {self.api_key}")

    @patch("upcdatabase.client.requests.Session.get")
    def test_bearer_token_in_request(self, mock_get):
        """Test that bearer token is sent in Authorization header.

        Validates that API requests include the bearer token authentication
        in the Authorization header with the format 'Bearer <api_key>'.
        """
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response

        self.client.lookup(self.test_upc)

        # Verify the request was made with Authorization header
        mock_get.assert_called_once()
        call_args = mock_get.call_args

        # Check that headers were passed
        self.assertIn("headers", call_args[1])
        headers = call_args[1]["headers"]

        # Check that Authorization header exists
        self.assertIn("Authorization", headers)

        # Check that bearer token format is correct
        auth_header = headers["Authorization"]
        self.assertTrue(
            auth_header.startswith("Bearer "),
            f"Authorization header should start with 'Bearer ', got: {auth_header}",
        )

        # Check that API key is included in bearer token
        self.assertEqual(
            auth_header,
            f"Bearer {self.api_key}",
            f"Bearer token should contain API key: {self.api_key}",
        )


if __name__ == "__main__":
    unittest.main()
