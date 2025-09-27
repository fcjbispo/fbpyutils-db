# fbpyutils-db

Francisco Bispo's Utilities for Database Operations with Python

## Description

This project provides a collection of Python utility functions focused on database interactions and data manipulation, primarily using Pandas and SQLAlchemy. Key functionalities include:

- Handling null values (`_deal_with_nans`).
- Normalizing column names (`normalize_columns`).
- Isolating DataFrame rows based on group criteria (`isolate`).
- Adding hash-based columns and indexes to DataFrames (`add_hash_column`, `add_hash_index`).
- Creating database tables from DataFrames with advanced features (`create_table`).
- Performing bulk database operations (append, upsert, replace) (`table_operation`).
- Managing database indexes (`create_index`).
- Mapping Pandas types to SQLAlchemy types (`get_column_type`, `get_columns_types`).
- Extracting data from DataFrames (`get_data_from_pandas`).
- Generating ASCII table representations for display (`ascii_table`, `print_ascii_table`, etc.).

## Version 0.3.1 - New Features

### Enhanced Database Support
- **Multi-dialect support**: Full support for SQLite, PostgreSQL, Oracle, and FirebirdSQL databases
- **Advanced table creation**: Support for indexes, foreign keys, and constraints in all supported dialects
- **Foreign key support**: Optional foreign key support for SQLite3 via environment variable
- **FirebirdSQL integration**: Complete FirebirdSQL dialect implementation with constraint support

### New Database Operations
- **create_index**: Standalone index creation function for all supported database dialects
- **Enhanced create_table**: Support for creating indexes, foreign keys, and constraints during table creation
- **Multi-dialect compatibility**: All database functions work seamlessly across SQLite, PostgreSQL, Oracle, and FirebirdSQL

## Documentation

### 📚 Complete Documentation
- **[DOC.md](DOC.md)** - Comprehensive documentation with usage examples and API reference
- **[TODO.md](TODO.md)** - Implementation and testing status tracker
- **[SPEC.md](SPEC.md)** - Technical specification and requirements

### 📖 Quick Links
- [Installation Guide](#installation)
- [Usage Examples](DOC.md#usage)
- [API Reference](DOC.md#functions)
- [Testing Status](TODO.md#implementation-status)

## Authors

- Francisco C J Bispo (fcjbispo@franciscobispo.net)

## Dependencies

- pandas
- numpy
- sqlalchemy

## Development Dependencies

- mock>=5.2.0
- pytest>=8.3.5
- pytest-cov>=6.0.0

## Installation

```bash
uv pip install .
```

## Tests

```bash
pytest tests
```

## Development

This project follows the VIBE (Vibe Intelligent Development Environment) guidelines. The codebase includes:

- **Memory Bank**: Complete project documentation in `memory_bank/` directory
- **Test Coverage**: >90% coverage with pytest and pytest-cov
- **Type Safety**: Full type hints throughout codebase
- **Documentation**: Comprehensive docs following Google-style docstrings

## License
This project is licensed under the MIT License. For the full text of the license, see [the official MIT License](https://opensource.org/licenses/MIT).

---
## MIT License Disclaimer

Copyright (c) 2025 Francisco C J Bispo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**
