.PHONY: help install clean test lint format typecheck publish

help:
	@echo "upcdatabase - Makefile commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install package in development mode with dependencies"
	@echo "  make clean      - Remove build artifacts and cache files"
	@echo "  make test       - Run test suite"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with black and isort"
	@echo "  make typecheck  - Run type checking with mypy"
	@echo "  make publish    - Clean, build, and upload to PyPI"
	@echo ""

install:
	pip install -e ".[dev]"

clean:
	rm -rf build/ dist/ *.egg-info *.dist-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage .pytest_cache htmlcov .mypy_cache

test:
	pytest tests/ -v

lint:
	pylint src/upcdatabase/ --disable=all --enable=E,F

format:
	black src/ tests/
	isort src/ tests/

typecheck:
	mypy src/upcdatabase/ --ignore-missing-imports --no-warn-return-any

publish: clean
	@echo "Building distribution..."
	python -m build
	@echo ""
	@echo "Uploading to PyPI..."
	@if [ -f .env ]; then \
		set -a; \
		. ./.env; \
		set +a; \
		python -m twine upload dist/* --username __token__ --password $$PYPI_TOKEN; \
	else \
		echo "Error: .env file not found. Copy .env.example to .env and add your PyPI token."; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ Successfully published to PyPI!"
