# Publishing to PyPI

This document explains how to publish this package to PyPI.

## Prerequisites

1. Install build and twine:
```bash
pip install build twine
```

2. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

## Building the Package

Build the distribution files:
```bash
python -m build
```

This creates:
- `dist/rust-crate-pipeline-X.X.X.tar.gz` (source distribution)
- `dist/rust_crate_pipeline-X.X.X-py3-none-any.whl` (wheel)

## Testing on TestPyPI

First, test on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ rust-crate-pipeline
```

## Publishing to PyPI

Once tested, publish to the real PyPI:

```bash
python -m twine upload dist/*
```

## Automation with GitHub Actions

Consider setting up GitHub Actions for automated publishing. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Version Management

Update version numbers in:
- `pyproject.toml`
- `setup.py`
- `rust_crate_pipeline/__init__.py`

## API Token Setup

For automated publishing, use API tokens instead of username/password:

1. Go to PyPI account settings
2. Generate an API token
3. Use `__token__` as username and the token as password
