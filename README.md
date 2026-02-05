# upcdatabase

A Python library for accessing the [UPC Database API](https://upcdatabase.org/). Look up product information by UPC/EAN code, search for products, access currency and Bitcoin data, and more.

## Features

- **Product Lookup**: Find product information by UPC or EAN code
- **Search**: Search for products by name or query
- **Currency Data**: Get latest and historical currency exchange rates
- **Bitcoin Data**: Access Bitcoin exchange rate information
- **QR Code Generation**: Generate QR codes programmatically
- **Account Management**: Access your API account information

## Installation

Install from PyPI:

```bash
pip install upcdatabase
```

## Project Structure

```
upcdatabase/
├── src/upcdatabase/
│   ├── __init__.py          # Package initialization and exports
│   └── client.py            # Main UPCDatabase API client
├── tests/
│   ├── __init__.py
│   └── test_client.py       # Unit tests (17 tests, 100% coverage)
├── examples.py              # Usage examples for all endpoints
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── CONTRIBUTING.md          # Contribution guidelines
├── PUBLISHING.md            # PyPI publishing guide
├── pyproject.toml           # Project configuration and metadata
├── .pre-commit-config.yaml  # Pre-commit hooks (linting, formatting, tests)
└── requirements-dev.txt     # Development dependencies
```

## Quick Start

First, you'll need an API key from [UPC Database](https://upcdatabase.org/):

1. Create a free account at https://upcdatabase.org/signup
2. Register your application at https://upcdatabase.org/apikeys to get your API key

Then use the library:

```python
from upcdatabase import UPCDatabase

# Initialize the client
client = UPCDatabase(api_key="your_api_key_here")

# Look up a product by UPC
product = client.lookup("036000291204")
print(product["name"])
print(product["price"])
```

## Usage Examples

### Product Lookup

```python
from upcdatabase import UPCDatabase

client = UPCDatabase(api_key="your_api_key")

# Look up by UPC code
product = client.lookup("036000291204")
print(f"Product: {product['name']}")
print(f"Manufacturer: {product['manufacturer']}")
print(f"Price: ${product['price']}")
print(f"Image: {product['image']}")
```

### Search Products

```python
# Search for products
results = client.search("coca cola", limit=20)
for item in results.get("items", []):
    print(f"{item['name']} - {item['upc']}")
```

### Get Currency Data

```python
# Latest currency rates
rates = client.get_latest_currency()
print(rates)

# Historical rates
history = client.get_currency_history("2025-01-15")
print(history)

# Available symbols
symbols = client.get_currency_symbols()
print(symbols)
```

### Get Bitcoin Data

```python
# Latest Bitcoin rate
btc = client.get_latest_bitcoin()
print(f"BTC: ${btc['price']}")

# Historical Bitcoin rate
btc_history = client.get_bitcoin_history("2025-01-15")
print(btc_history)
```

### Generate QR Codes

```python
# Generate a QR code
qr = client.generate_qr("https://example.com")
print(qr)
```

### Get Account Information

```python
# Check account and API usage
account = client.get_account_info()
print(f"Requests remaining: {account['requests_remaining']}")
```

## Using as a Context Manager

```python
from upcdatabase import UPCDatabase

# The session will be automatically closed when exiting the block
with UPCDatabase(api_key="your_api_key") as client:
    product = client.lookup("036000291204")
    print(product["name"])
```

## Error Handling

```python
from upcdatabase import UPCDatabase, UPCDatabaseError

client = UPCDatabase(api_key="your_api_key")

try:
    product = client.lookup("invalid_code")
except UPCDatabaseError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## API Documentation

For detailed API documentation, visit:
- [API Reference](https://upcdatabase.org/api)
- [Authentication](https://upcdatabase.org/api-auth)
- [API Limits](https://upcdatabase.org/api-limits)
- [Pricing](https://upcdatabase.org/api-pricing)

## Documentation

### Client Methods

#### `lookup(upc: str) -> dict`
Look up a product by UPC or EAN code.

**Parameters:**
- `upc` (str): The UPC or EAN code to lookup

**Returns:** Product information dictionary

**Raises:** `UPCDatabaseError` if lookup fails

#### `search(query: str, limit: int = 10) -> dict`
Search for products by name or query.

**Parameters:**
- `query` (str): Search query string
- `limit` (int): Maximum number of results (default: 10)

**Returns:** Search results dictionary

#### `get_latest_currency() -> dict`
Get latest currency exchange rates.

#### `get_currency_history(date: str) -> dict`
Get historical currency rates for a specific date.

**Parameters:**
- `date` (str): Date in YYYY-MM-DD format

#### `get_currency_symbols() -> dict`
Get list of supported currency symbols.

#### `get_latest_bitcoin() -> dict`
Get latest Bitcoin exchange rate.

#### `get_bitcoin_history(date: str) -> dict`
Get historical Bitcoin rate for a specific date.

#### `generate_qr(text: str) -> dict`
Generate a QR code from text/data.

**Parameters:**
- `text` (str): Text to encode in the QR code

#### `get_account_info() -> dict`
Get account and API usage information.

## Requirements

- Python 3.7+
- `requests` library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This library is not affiliated with or endorsed by UPC Database. It is an independent client library for accessing the public UPC Database API.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
