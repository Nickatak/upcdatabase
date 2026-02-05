"""Examples of using the upcdatabase library"""

from upcdatabase import UPCDatabase, UPCDatabaseError


def example_lookup():
    """Example: Look up a product by UPC"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        # Look up a common product
        product = client.lookup("036000291204")
        print("=== Product Lookup ===")
        print(f"Name: {product.get('name')}")
        print(f"Manufacturer: {product.get('manufacturer')}")
        print(f"Price: {product.get('price')}")
        print(f"Image: {product.get('image')}")
        print()
    except UPCDatabaseError as e:
        print(f"Error during lookup: {e}")


def example_search():
    """Example: Search for products"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        results = client.search("coca cola", limit=5)
        print("=== Search Results ===")
        for item in results.get("items", []):
            print(f"- {item.get('name')} ({item.get('upc')})")
        print()
    except UPCDatabaseError as e:
        print(f"Error during search: {e}")


def example_currency():
    """Example: Get currency data"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        print("=== Latest Currency Rates ===")
        rates = client.get_latest_currency()
        print(rates)
        print()
    except UPCDatabaseError as e:
        print(f"Error getting currency data: {e}")


def example_bitcoin():
    """Example: Get Bitcoin data"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        print("=== Latest Bitcoin Rate ===")
        btc = client.get_latest_bitcoin()
        print(btc)
        print()
    except UPCDatabaseError as e:
        print(f"Error getting Bitcoin data: {e}")


def example_qr_code():
    """Example: Generate a QR code"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        print("=== QR Code Generation ===")
        qr = client.generate_qr("https://example.com")
        print(qr)
        print()
    except UPCDatabaseError as e:
        print(f"Error generating QR code: {e}")


def example_account():
    """Example: Get account information"""
    client = UPCDatabase(api_key="your_api_key_here")
    
    try:
        print("=== Account Information ===")
        account = client.get_account_info()
        print(account)
        print()
    except UPCDatabaseError as e:
        print(f"Error getting account info: {e}")


def example_context_manager():
    """Example: Using as a context manager"""
    try:
        print("=== Using Context Manager ===")
        with UPCDatabase(api_key="your_api_key_here") as client:
            product = client.lookup("036000291204")
            print(f"Product: {product.get('name')}")
        print("Session automatically closed")
        print()
    except UPCDatabaseError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("UPC Database Library Examples")
    print("=" * 50)
    print("Note: Replace 'your_api_key_here' with your actual API key")
    print("Get your key from: https://upcdatabase.org/apikeys")
    print("=" * 50)
    print()
    
    # Uncomment the examples you want to run:
    # example_lookup()
    # example_search()
    # example_currency()
    # example_bitcoin()
    # example_qr_code()
    # example_account()
    # example_context_manager()
