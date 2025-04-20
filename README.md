# fbpyutils-db

Francisco Bispo's Utilities for Database Operations with Python

## Description

This project provides a collection of Python utility functions focused on database interactions and data manipulation, primarily using Pandas and SQLAlchemy. Key functionalities include:

- Handling null values (`_deal_with_nans`).
- Normalizing column names (`normalize_columns`).
- Isolating DataFrame rows based on group criteria (`isolate`).
- Adding hash-based columns and indexes to DataFrames (`add_hash_column`, `add_hash_index`).
- Creating database tables from DataFrames (`create_table`).
- Performing bulk database operations (append, upsert, replace) (`table_operation`).
- Managing database indexes (`create_index`).
- Mapping Pandas types to SQLAlchemy types (`get_column_type`, `get_columns_types`).
- Extracting data from DataFrames (`get_data_from_pandas`).
- Generating ASCII table representations for display (`ascii_table`, `print_ascii_table`, etc.).

## Documentation

Detailed documentation is available within the source code docstrings. For project overview and updates, refer to the [project's GitHub repository](https://github.com/fcjbispo/fbpyutils-db).

For detailed function documentation, see [DOC.md](DOC.md).
To track the implementation and testing status of features, see [TODO.md](TODO.md).

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

## License
This project is licensed under the MIT License. For the full text of the license, see [the official MIT License](https://opensource.org/licenses/MIT).

---
## MIT License Disclaimer

Copyright (c) 2025 Francisco C J Bispo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**


