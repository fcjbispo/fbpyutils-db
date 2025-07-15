# Technical Context - FBPyUtils-DB

## Technologies Used
- **Language**: Python 3.8+
- **Package Manager**: uv (modern Python package manager)
- **Testing**: pytest, pytest-cov
- **Type Checking**: mypy-compatible type hints
- **Code Formatting**: black, isort
- **Documentation**: Sphinx-compatible docstrings

## Development Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup development environment
uv sync
uv run pytest -s -vv --cov=fbpyutils_db --cov-report=xml:coverage.xml --cov-report=html:coverage_html --cov-fail-under=90 tests/
```

## Technical Constraints
- **Python Version**: Minimum 3.8 for compatibility
- **Dependencies**: Minimal external dependencies to keep package lightweight
- **Performance**: Functions should handle reasonably large datasets efficiently
- **Compatibility**: Cross-platform support (Windows, Linux, macOS)

## Dependencies
### Runtime Dependencies
- pandas: Data manipulation and analysis
- numpy: Numerical computing support

### Development Dependencies
- pytest: Testing framework
- pytest-cov: Coverage reporting
- black: Code formatting
- isort: Import sorting
- mypy: Type checking

## Tool Usage Patterns
- **uv**: For all package management and scrip
