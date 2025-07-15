# System Patterns - FBPyUtils-DB

## Architecture Overview
FBPyUtils-DB follows a modular utility library architecture with these key patterns:

## Design Patterns in Use
- **Functional Programming**: Most utilities are implemented as pure functions
- **Single Responsibility Principle**: Each function has one clear purpose
- **Type Hints**: Extensive use of Python type hints for better IDE support
- **Error Handling**: Graceful error handling with informative messages

## Component Relationships
```
fbpyutils_db/
├── __init__.py          # Package initialization
├── app.json            # Package metadata
└── py.typed           # Type checking support
```

## Critical Implementation Paths
1. **Data Processing Pipeline**: normalize_columns → add_hash_column → add_hash_index
2. **Visualization Pipeline**: get_data_from_pandas → print_ascii_table_from_dataframe
3. **Testing Pipeline**: pytest → coverage → report generation

## Key Technical Decisions
- **Testing Framework**: pytest with pytest-cov for coverage
- **Type System**: Full type hints with mypy compatibility
- **Documentation**: Docstrings following Google style
- **Packaging**: Standard Python package structure with pyproject.toml
