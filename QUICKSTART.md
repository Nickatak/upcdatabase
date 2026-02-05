# Quick Start Guide

## Installation

```bash
pip install upcdatabase
```

## Get Your API Key

1. Visit https://upcdatabase.org/
2. Sign up for a free account
3. Go to https://upcdatabase.org/apikeys
4. Create an application to get your API key

## Basic Usage

```python
from upcdatabase import UPCDatabase

# Create client
client = UPCDatabase(api_key="your_api_key_here")

# Look up a product
product = client.lookup("036000291204")
print(product["name"])
print(product["price"])
```

## Common Operations

### Search for Products

```python
results = client.search("coca cola", limit=10)
for item in results["items"]:
    print(f"{item['name']} - UPC: {item['upc']}")
```

### Get Currency Exchange Rates

```python
# Latest rates
rates = client.get_latest_currency()

# Historical rates
history = client.get_currency_history("2025-01-15")
```

### Get Bitcoin Information

```python
# Latest BTC rate
btc = client.get_latest_bitcoin()
print(f"BTC/USD: {btc['price']}")
```

### Check Account Status

```python
account = client.get_account_info()
print(f"Requests remaining: {account['requests_remaining']}")
```

## Error Handling

```python
from upcdatabase import UPCDatabase, UPCDatabaseError

client = UPCDatabase(api_key="your_api_key")

try:
    product = client.lookup("invalid_code")
except UPCDatabaseError as e:
    print(f"API Error: {e}")
```

## Complete Example

```python
from upcdatabase import UPCDatabase, UPCDatabaseError

def main():
    api_key = "your_api_key_here"
    client = UPCDatabase(api_key=api_key)

    # Look up a specific product
    try:
        upc = "036000291204"
        product = client.lookup(upc)
        print(f"Found: {product['name']}")
        print(f"Price: ${product['price']}")
        print(f"Manufacturer: {product['manufacturer']}")
    except UPCDatabaseError as e:
        print(f"Error: {e}")

    # Search for products
    try:
        results = client.search("pepsi", limit=5)
        print(f"\nFound {len(results['items'])} results for 'pepsi'")
    except UPCDatabaseError as e:
        print(f"Search error: {e}")

if __name__ == "__main__":
    main()
```

## Next Steps

- Read the [README](README.md) for detailed documentation
- Check [examples.py](examples.py) for more examples
- Review [API Documentation](https://upcdatabase.org/api) for all endpoints

## Support

For issues or questions:
- Check [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
- Review the API documentation

## API Limits

Check your account at https://upcdatabase.org/apikeys for:
- API rate limits
- Request quota
- Remaining requests

Happy coding!
