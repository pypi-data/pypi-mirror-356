# BOL OCR Client - Publishing Guide

## Overview

The BOL OCR client package is ready for PyPI publishing with automated GitHub Actions workflows and manual publishing scripts.

## Prerequisites

### 1. PyPI Account Setup
You need to create accounts and get API tokens:

1. **PyPI Account**: Create account at https://pypi.org/account/register/
2. **TestPyPI Account**: Create account at https://test.pypi.org/account/register/ (for testing)
3. **API Tokens**:
   - Go to Account Settings → API tokens
   - Create token with "Entire account" scope
   - Save the token securely (starts with `pypi-`)

### 2. GitHub Secrets
Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):
- `PYPI_API_TOKEN`: Your PyPI API token
- `TEST_PYPI_API_TOKEN`: Your TestPyPI API token (optional, for testing)

## Publishing Methods

### Method 1: GitHub Actions (Recommended)

#### Automatic on Tag Push
```bash
# Create and push a tag
git tag client-v0.1.1
git push origin client-v0.1.1
```

This automatically:
- Updates version numbers
- Runs tests and quality checks
- Builds the package
- Publishes to PyPI
- Creates a GitHub release

#### Manual Trigger
1. Go to GitHub Actions → "Publish Python Client Package"
2. Click "Run workflow"
3. Enter the version number (e.g., `0.1.1`)
4. Click "Run workflow"

### Method 2: Local Publishing

#### Using the Helper Script
```bash
cd client/

# Test build (dry run)
python scripts/publish.py --version 0.1.1 --dry-run

# Publish to TestPyPI first (recommended)
python scripts/publish.py --version 0.1.1 --test

# Publish to PyPI
python scripts/publish.py --version 0.1.1
```

#### Manual Steps
```bash
cd client/

# 1. Update version numbers
# Edit pyproject.toml: version = "0.1.1"
# Edit src/bol_ocr_client/__init__.py: __version__ = "0.1.1"

# 2. Run tests and checks
uv run pytest
uv run ruff check .
uv run mypy .

# 3. Build package
uv run python -m build

# 4. Check package
uv run twine check dist/*

# 5. Upload to PyPI
uv run twine upload dist/*
```

## Testing Before Publishing

### 1. Test on TestPyPI
```bash
# Upload to TestPyPI
python scripts/publish.py --version 0.1.1-test --test

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bol-ocr-client==0.1.1-test
```

### 2. Local Testing
```bash
# Build and install locally
cd client/
uv run python -m build
pip install dist/bol_ocr_client-0.1.0-py3-none-any.whl

# Test in a new environment
python -c "from bol_ocr_client import BOLClient; print('Import successful!')"
```

## Version Management

### Version Format
- Use semantic versioning: `MAJOR.MINOR.PATCH`
- Examples: `0.1.0`, `0.1.1`, `1.0.0`

### Version Locations
Update these files when changing versions:
1. `pyproject.toml` - `version = "X.Y.Z"`
2. `src/bol_ocr_client/__init__.py` - `__version__ = "X.Y.Z"`

### Tag Format
- Use tags like: `client-v0.1.1`
- This triggers the GitHub Actions workflow

## Package Information

- **Package Name**: `bol-ocr-client`
- **Install Command**: `pip install bol-ocr-client`
- **GitHub**: https://github.com/jvogel/ocr-api
- **PyPI**: https://pypi.org/project/bol-ocr-client/ (after first publish)

## Troubleshooting

### Common Issues

1. **API Token Issues**
   - Ensure token has correct permissions
   - Token format: `pypi-AgEIcHl...` (starts with `pypi-`)
   - Check token hasn't expired

2. **Version Conflicts**
   - PyPI doesn't allow re-uploading same version
   - Increment version number for new uploads
   - Use TestPyPI for testing versions

3. **Build Failures**
   - Ensure all tests pass: `uv run pytest`
   - Check code quality: `uv run ruff check .`
   - Verify types: `uv run mypy .`

4. **Import Errors After Install**
   - Check package structure in `dist/` files
   - Verify `__init__.py` exports are correct
   - Test with fresh virtual environment

### Getting Help

- Check GitHub Actions logs for automated publishing issues
- Use `uv run twine check dist/*` to validate packages before upload
- Test with TestPyPI before publishing to main PyPI
