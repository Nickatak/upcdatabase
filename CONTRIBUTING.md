# Contributing to upcdatabase

Thank you for considering contributing to the upcdatabase library! Here's how you can help:

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/upcdatabase.git
   cd upcdatabase
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/upcdatabase

# Run specific test
pytest tests/test_client.py::TestUPCDatabase::test_lookup_success
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with pylint
pylint src/upcdatabase/

# Type check with mypy
mypy src/upcdatabase/
```

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - Tests pass: `pytest tests/`
   - Code is formatted: `black src/ tests/`
   - Type hints are correct: `mypy src/upcdatabase/`

3. **Commit your changes**:
   ```bash
   git commit -m "Description of your changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for public methods
- Keep functions focused and testable

## Testing

- All new features must include tests
- Maintain or improve code coverage
- Test both success and error cases

## Documentation

- Update README.md if adding features
- Add docstrings to new methods
- Include usage examples

## Issues and Discussions

- **Found a bug?** Open an issue with:
  - Clear description of the issue
  - Steps to reproduce
  - Expected vs actual behavior
  
- **Have a suggestion?** Open a discussion or feature request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue or start a discussion if you have questions!
