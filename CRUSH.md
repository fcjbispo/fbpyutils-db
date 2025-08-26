# CRUSH Agent Configuration

## Commands
- Test: `uv run pytest tests/unit/` 
- Test single file: `uv run pytest tests/unit/test_file.py`
- Test single test: `uv run pytest tests/unit/test_file.py::test_name`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run mypy fbpyutils_db/`

## VIBE Guide
Before proceeding with any changes, read the VIBE coding guide at:
https://github.com/fcjbispo/vibe-coding/blob/master/VIBE_GUIDE.md

## Code Style
- Use ruff for linting and formatting
- Use mypy for type checking
- Follow PEP 8 conventions
- Use descriptive variable names
- Add type hints to all functions
- Use docstrings for modules, classes, and functions
- Prefer explicit imports over wildcard imports
- Handle errors gracefully with specific exception handling
- Use f-strings for string formatting
- Keep functions small and focused
- Use pathlib for path operations
- Prefer comprehensions over loops when appropriate

## Naming
- Variables: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

## Testing
- Use pytest framework
- Write both unit and functional tests
- Mock external dependencies
- Test edge cases and error conditions
- Use fixtures for setup/teardown

## Imports
- Group imports: standard library, third-party, local
- Use absolute imports when possible
- Sort imports alphabetically within groups