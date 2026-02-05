# Publishing to PyPI

This guide explains how to build and publish the upcdatabase library to PyPI.

## Prerequisites

1. **PyPI Account**: Create a free account at https://pypi.org/
2. **TestPyPI Account** (optional): Create an account at https://test.pypi.org/ for testing

## Setup

### Step 1: Install Build Tools

```bash
pip install --upgrade build twine
```

### Step 2: Configure PyPI Credentials

Create or update `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-...  # Your PyPI API token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...  # Your TestPyPI API token
```

Or use API tokens:
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use the token as your password with username `__token__`

## Building

```bash
# Build wheel and source distribution
python -m build

# This creates:
# - dist/upcdatabase-0.1.0.tar.gz (source distribution)
# - dist/upcdatabase-0.1.0-py3-none-any.whl (wheel)
```

## Testing Before Publishing

### Test on TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ upcdatabase

# Test in Python
python -c "from upcdatabase import UPCDatabase; print(UPCDatabase.__doc__)"
```

## Publishing to PyPI

```bash
# Upload to official PyPI
twine upload dist/*

# Verify
pip install upcdatabase
```

## After Publishing

1. **Tag the release**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create a GitHub Release**:
   - Go to GitHub repository
   - Click "Releases"
   - "Create a new release"
   - Tag version and add changelog

3. **Update version** for next development:
   ```bash
   # In pyproject.toml, change version to 0.2.0.dev0
   ```

## Updating Package

When releasing a new version:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push
4. Run tests: `pytest tests/`
5. Clean old builds: `rm -rf dist/ build/ *.egg-info`
6. Build: `python -m build`
7. Upload: `twine upload dist/*`
8. Tag release in git

## PyPI Package URL

Once published, your package will be available at:
```
https://pypi.org/project/upcdatabase/
```

Users can install with:
```bash
pip install upcdatabase
```

## Troubleshooting

### Invalid distribution
```bash
twine check dist/*
```

### Credentials issues
```bash
# Use credentials file
twine upload --password-file ~/.pypi_password dist/*

# Or interactive
twine upload dist/*  # Will prompt for credentials
```

### Remove old builds before uploading
```bash
rm -rf dist/ build/ *.egg-info
python -m build
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
