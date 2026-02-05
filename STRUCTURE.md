# Project Structure Guide

## Directory Layout

```
upcdatabase/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI/CD workflow
├── src/
│   └── upcdatabase/
│       ├── __init__.py         # Package initialization & exports
│       └── client.py           # Main API client implementation
├── tests/
│   ├── __init__.py
│   └── test_client.py          # Unit tests
├── .editorconfig               # Code formatting settings
├── .gitignore                  # Git ignore file
├── CHANGELOG.md                # Version history and changes
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── MANIFEST.in                 # Package manifest for distribution
├── PUBLISHING.md               # Guide for publishing to PyPI
├── QUICKSTART.md               # Quick start guide
├── README.md                   # Main documentation
├── examples.py                 # Usage examples
├── pyproject.toml              # Modern Python project config
├── pytest.ini                  # Pytest configuration
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Setup script (legacy)
└── tox.ini                     # Testing environments config
```

## Key Files

### Configuration Files

- **pyproject.toml**: Modern Python packaging configuration
  - Project metadata (name, version, description)
  - Dependencies and optional extras
  - Tool configurations (black, isort, mypy)

- **setup.py**: Legacy setup script (delegating to pyproject.toml)

- **pytest.ini**: Pytest testing configuration

- **tox.ini**: Testing configuration for multiple Python versions

### Source Code

- **src/upcdatabase/client.py**: Main API client class
  - `UPCDatabase` - Main client class
  - `UPCDatabaseError` - Custom exception class

- **src/upcdatabase/__init__.py**: Package exports

### Testing

- **tests/test_client.py**: Unit tests for the client

### Documentation

- **README.md**: Main documentation with examples
- **QUICKSTART.md**: Quick start guide
- **CONTRIBUTING.md**: How to contribute
- **PUBLISHING.md**: How to publish to PyPI
- **CHANGELOG.md**: Version history

### Build & CI/CD

- **.github/workflows/tests.yml**: GitHub Actions workflow for testing

## Development Workflow

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/upcdatabase.git
cd upcdatabase

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

### 2. Running Tests

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=src/upcdatabase

# Using tox (test across multiple Python versions)
tox
```

### 3. Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
pylint src/upcdatabase/

# Type checking
mypy src/upcdatabase/
```

### 4. Building Package

```bash
# Build distribution
python -m build

# Check distribution
twine check dist/*
```

## Package Features

### API Endpoints Supported

1. **Products**
   - `lookup(upc)` - Get product by UPC/EAN
   - `search(query, limit)` - Search for products

2. **Currency**
   - `get_latest_currency()` - Latest exchange rates
   - `get_currency_history(date)` - Historical rates
   - `get_currency_symbols()` - Available symbols

3. **Bitcoin**
   - `get_latest_bitcoin()` - Current Bitcoin rate
   - `get_bitcoin_history(date)` - Historical Bitcoin rates

4. **Miscellaneous**
   - `generate_qr(text)` - Generate QR codes
   - `get_account_info()` - Account details

## Dependencies

### Core
- `requests>=2.25.0` - HTTP library

### Development
- `pytest` - Testing framework
- `pytest-cov` - Coverage reports
- `black` - Code formatter
- `isort` - Import sorter
- `pylint` - Code linter
- `mypy` - Type checker

## Versioning

Uses [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 0.1.0)
- Current version: 0.1.0

## Publishing

See [PUBLISHING.md](PUBLISHING.md) for:
1. Building distribution
2. Testing on TestPyPI
3. Publishing to PyPI
4. Creating releases

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
1. Development setup
2. Code style guidelines
3. Testing requirements
4. Pull request process

## License

MIT License - See [LICENSE](LICENSE) file

## Resources

- [UPC Database API](https://upcdatabase.org/api)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/)
