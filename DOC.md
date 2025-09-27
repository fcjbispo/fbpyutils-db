# fbpyutils-db

[![PyPI Version](https://img.shields.io/pypi/v/fbpyutils-db.svg)](https://pypi.org/project/fbpyutils-db/)
[![License](https://img.shields.io/pypi/l/fbpyutils-db.svg)](https://opensource.org/licenses/MIT)

## Overview

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
- Generating ASCII table representations for display (`ascii_table`, `print_ascii_table`, `print_ascii_table_from_dataframe`).

## Version 0.3.1 - New Features
- **Update fbpyutils to version 1.7.2**
- **Add comprehensive docstrings for all modules**

## Version 0.3.0 - New Features

### Enhanced Database Support
- **Multi-dialect support**: Full support for SQLite, PostgreSQL, Oracle, and FirebirdSQL databases
- **Advanced table creation**: Support for indexes, foreign keys, and constraints in all supported dialects
- **Foreign key support**: Optional foreign key support for SQLite3 via environment variable
- **FirebirdSQL integration**: Complete FirebirdSQL dialect implementation with constraint support

### New Database Operations
- **create_index**: Standalone index creation function for all supported database dialects
- **Enhanced create_table**: Support for creating indexes, foreign keys, and constraints during table creation
- **Multi-dialect compatibility**: All database functions work seamlessly across SQLite, PostgreSQL, Oracle, and FirebirdSQL

## Installation

```bash
pip install fbpyutils-db
```
*Note: The exact package name on PyPI might differ. Please verify the correct name if installation fails. The command `uv pip install .` can be used for local development installation.*

## Usage

### Database Dialect Support

FBPyUtils-DB supports multiple database dialects with full compatibility for advanced features:

- **SQLite**: Lightweight file-based database with optional foreign key support
- **PostgreSQL**: Robust, production-ready database with full constraint support
- **Oracle**: Enterprise-grade database with advanced constraint capabilities
- **FirebirdSQL**: Cross-platform database with complete constraint support

### Environment Variables

- **FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON**: Set to `true` to enable foreign key constraints in SQLite3

### Functions

#### `add_hash_column`

Adds a hash column to the given DataFrame.

```python
from fbpyutils_db import add_hash_column
import pandas as pd

df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
df_with_hash = add_hash_column(df, 'hash_id', length=8, columns=['col1'])
print(df_with_hash)
#   hash_id  col1 col2
# 0  6b86b273     1    a
# 1  d4735e3a     2    b
```

**Parameters:**

- `df` (pd.DataFrame): The input DataFrame.
- `column_name` (str): The name of the hash column to be created.
- `length` (int, optional): The length of the hash string. Defaults to 12.
- `columns` (List[str], optional): List of column names to be used for generating the hash. If None or empty (default), all columns are used.

**Returns:**

- pd.DataFrame: A new DataFrame with the hash column added as the first column.

---

#### `add_hash_index`

Replaces the DataFrame index with a hash string and renames the index.

```python
from fbpyutils_db import add_hash_index
import pandas as pd

df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
df_indexed = add_hash_index(df, 'new_index', length=12, columns=['col1', 'col2'])
print(df_indexed)
#            col1 col2
# new_index
# 8b9c45e2a9f6    1    a
# 3d4c4f4f4d1f    2    b
# 5b5d8c7a2a4c    3    c
```

**Parameters:**

- `df` (pd.DataFrame): The input DataFrame.
- `index_name` (str, optional): The name to be given to the new index. Defaults to 'id'.
- `length` (int, optional): The length of the hash string. Defaults to 12.
- `columns` (List[str], optional): List of column names to be used for generating the index hash. If None or empty (default), all columns are used.

**Returns:**

- pd.DataFrame: A DataFrame with the new hash index.

---

#### `ascii_table`

Creates an ASCII table representation of the given data.

```python
from fbpyutils_db import ascii_table

data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
columns = ['Name', 'Age', 'Country']
table_lines = ascii_table(data, columns=columns, alignment='center')
for line in table_lines:
    print(line)
# +-------+-----+---------+
# |  Name | Age | Country |
# +-------+-----+---------+
# |  John |  25 |   USA   |
# | Alice |  30 |  Canada |
# |  Bob  |  40 |    UK   |
# +-------+-----+---------+
```

**Parameters:**

- `data` (List[List[Any]]): A list of lists representing the data rows.
- `columns` (List[str], optional): A list of column names. Defaults to an empty list.
- `alignment` (str, optional): The alignment of the table cells ('left', 'right', 'center'). Defaults to 'left'.
- `numrows` (int, optional): The number of rows to display. If None, all rows are displayed. Defaults to None.

**Returns:**

- List[str]: A list of strings representing the ASCII table, or None if data is empty.

---

#### `create_index`

Creates a SQLAlchemy Index object for a given table and keys, supporting all database dialects (SQLite, PostgreSQL, Oracle, FirebirdSQL).

```python
from sqlalchemy import Table, MetaData, Column, Integer, String
from fbpyutils_db import create_index

# Basic index creation
metadata = MetaData()
my_table = Table('my_table', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('value', Integer))

# Create unique index
unique_index = create_index('idx_name_unique', my_table, ['name'], unique=True)
# Creates a unique index on the 'name' column

# Create standard (non-unique) index
standard_index = create_index('idx_value', my_table, ['value'], unique=False)
# Creates a standard index on the 'value' column

# Create composite index
composite_index = create_index('idx_name_value', my_table, ['name', 'value'])
# Creates a composite index on both 'name' and 'value' columns
```

**Parameters:**

- `name` (str): The name of the index to be created.
- `table` (Selectable): The SQLAlchemy table on which to create the index.
- `keys` (List[str]): A list of column names that should be part of the index.
- `unique` (bool, optional): Whether the index should enforce uniqueness. Defaults to False.

**Returns:**

- Index: The created SQLAlchemy Index object.

**Supported Database Dialects:**
- **SQLite**: Supports standard and unique indexes
- **PostgreSQL**: Supports standard, unique, and composite indexes
- **Oracle**: Supports standard, unique, and composite indexes
- **FirebirdSQL**: Supports standard, unique, and composite indexes with proper naming conventions

---

#### `create_table`

Creates a table in the database using a pandas DataFrame as a schema with support for indexes, foreign keys, and constraints across all supported database dialects (SQLite, PostgreSQL, Oracle, FirebirdSQL).

```python
from sqlalchemy import create_engine
import pandas as pd
from fbpyutils_db import create_table

# Basic table creation
df = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B']})
engine = create_engine('sqlite:///:memory:') # Example with in-memory SQLite
create_table(df, engine, 'my_new_table', keys=['id'], index='primary')
# Creates the 'my_new_table' table with primary key in the database

# Advanced table creation with indexes, foreign keys, and constraints
df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'username': ['john', 'alice', 'bob'],
    'email': ['john@example.com', 'alice@example.com', 'bob@example.com']
})

# Define foreign keys
foreign_keys = [
    {
        'name': 'fk_users_department',
        'columns': ['department_id'],
        'refcolumns': ['id'],
        'table_name': 'departments'
    }
]

# Define constraints
constraints = [
    {'type': 'unique', 'name': 'uk_users_email', 'columns': ['email']},
    {'type': 'check', 'name': 'ck_users_username', 'conditions': "username != ''"}
]

create_table(
    df,
    engine,
    'users',
    keys=['user_id'],
    index='primary',
    foreign_keys=foreign_keys,
    constraints=constraints
)
# Creates the 'users' table with primary key, foreign key, and constraints
```

**Parameters:**

- `dataframe` (pd.DataFrame): The pandas DataFrame containing the schema information.
- `engine` (Engine): The SQLAlchemy engine for database connection.
- `table_name` (str): The name of the table to be created.
- `schema` (str, optional): The name of the schema where the table will be created. Defaults to None.
- `keys` (List[str], optional): List of column names to use as keys for index/primary key creation. Defaults to [].
- `index` (str, optional): Type of index to create using the `keys` ('standard', 'unique', 'primary'). Defaults to None (no index).
- `foreign_keys` (List[dict], optional): List of foreign key definitions. Each dict should contain 'name', 'columns', 'refcolumns', and optionally 'table_name'. Defaults to [].
- `constraints` (List[dict], optional): List of constraint definitions. Each dict should contain 'type' ('unique', 'check'), 'name', and 'columns' or 'conditions'. Defaults to [].
- `metadata` (MetaData, optional): SQLAlchemy MetaData object to use. If None, a new one will be created.

**Returns:**

- None

**Supported Database Dialects:**
- **SQLite**: Supports indexes, foreign keys (when `FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON=true`), and constraints
- **PostgreSQL**: Full support for indexes, foreign keys, and constraints
- **Oracle**: Full support for indexes, foreign keys, and constraints
- **FirebirdSQL**: Full support for indexes, foreign keys, and constraints with proper naming requirements

---

#### `get_column_type`

Maps a Pandas data type to a SQLAlchemy data type.

```python
from fbpyutils_db import get_column_type
import numpy as np

dtype_int = np.int64
sql_type = get_column_type(dtype_int)
print(sql_type)
# INTEGER

dtype_str = np.object_
sql_type_str = get_column_type(dtype_str)
print(sql_type_str)
# VARCHAR
```

**Parameters:**

- `dtype` (np.dtype or str): The Pandas data type to be mapped.

**Returns:**

- TypeEngine: The corresponding SQLAlchemy data type. String columns default to `String(4000)`.

---

#### `get_columns_types`

Returns a list of SQLAlchemy Column objects representing the columns of the given DataFrame.

```python
import pandas as pd
from fbpyutils_db import get_columns_types

df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
columns = get_columns_types(df, primary_keys=['A'])
print(columns)
# [Column('A', Integer(), table=None, primary_key=True, nullable=False), Column('B', String(), table=None)]
```

**Parameters:**

- `dataframe` (pd.DataFrame): The input DataFrame.
- `primary_keys` (List[str], optional): List of primary key column names. Defaults to [].

**Returns:**

- List[Column]: A list of SQLAlchemy Column objects.

---

#### `get_data_from_pandas`

Extracts data and column names from a Pandas DataFrame.

```python
import pandas as pd
from fbpyutils_db import get_data_from_pandas

df = pd.DataFrame({'Name': ['John', 'Alice', 'Bob'], 'Age': [25, 30, 40]})
data, columns = get_data_from_pandas(df, include_index=True)
print(data)
# [[0, 'John', 25], [1, 'Alice', 30], [2, 'Bob', 40]]
print(columns)
# ['Index', 'Name', 'Age']
```

**Parameters:**

- `df` (pd.DataFrame): A Pandas DataFrame.
- `include_index` (bool, optional): If True, includes the index column in the extracted data. Defaults to False.

**Returns:**

- Tuple[List[List[Any]], List[str]]: A tuple containing the extracted data (list of lists) and column names (list of strings).

---

#### `isolate`

Filters the DataFrame to isolate rows with maximum values in the 'Unique' column for each unique combination of values in `group_columns`. *Note: The original docstring mentions `unique_columns`, but the implementation uses a hardcoded `"Unique"` column.*

```python
import pandas as pd
from fbpyutils_db import isolate

df = pd.DataFrame({'Group': ['A', 'A', 'B', 'B'],
                   'Value': [1, 2, 3, 4],
                   'Unique': [5, 6, 7, 8]}) # Requires a column named 'Unique'
grouped_df = isolate(df, ['Group'])
print(grouped_df)
#   Group  Value  Unique
# 1     A      2       6
# 3     B      4       8
```

**Parameters:**

- `df` (pd.DataFrame): The input pandas DataFrame. Must contain a column named 'Unique'.
- `group_columns` (List[str]): A list of column names used for grouping the DataFrame.

**Returns:**

- pd.DataFrame: A pandas DataFrame containing only the rows with maximum values in the 'Unique' column for each unique combination of values in `group_columns`.

---

#### `normalize_columns`

Normalizes a list of column names by removing special characters (except underscore) and converting to lowercase.

```python
from fbpyutils_db import normalize_columns

cols = ['Name!', 'Age@', '#Address', 'Valid_Col']
try:
    normalized = normalize_columns(cols)
    print(normalized)
except AttributeError as e:
    print(e)
# Column names contain special characters that cannot be normalized.

cols_valid = ['First Name', 'Age', 'Address_1']
normalized_valid = normalize_columns(cols_valid) # This will raise AttributeError due to space
# Correct usage requires columns without special chars first:
cols_clean = ['FirstName', 'Age', 'Address_1']
normalized_clean = normalize_columns(cols_clean)
print(normalized_clean)
# ['firstname', 'age', 'address_1']
```
*Note: The implementation raises an error if any special characters (other than '_') are present, rather than removing them.*

**Parameters:**

- `cols` (List[str]): A list of column names.

**Returns:**

- List[str]: A list of normalized column names (lowercase, special characters removed).

**Raises:**

- `AttributeError`: If any column name contains special characters other than underscores.

---

#### `print_ascii_table`

Prints the ASCII table representation of the given data.

```python
from fbpyutils_db import print_ascii_table

data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
columns = ['Name', 'Age', 'Country']
print_ascii_table(data, columns=columns, alignment='center')
# Output:
# +-------+-----+---------+
# |  Name | Age | Country |
# +-------+-----+---------+
# |  John |  25 |   USA   |
# | Alice |  30 |  Canada |
# |  Bob  |  40 |    UK   |
# +-------+-----+---------+
```

**Parameters:**

- `data` (List[List[Any]]): A list of lists representing the data rows.
- `columns` (List[str], optional): A list of column names. Defaults to an empty list.
- `alignment` (str, optional): The alignment of the table cells ('left', 'right', 'center'). Defaults to 'left'.
- `numrows` (int, optional): The number of rows to display. If None, all rows are displayed. Defaults to None.

**Returns:**

- None

---

#### `print_ascii_table_from_dataframe`

Prints the ASCII table representation of a pandas DataFrame.

```python
import pandas as pd
from fbpyutils_db import print_ascii_table_from_dataframe

df = pd.DataFrame({'Name': ['John', 'Alice', 'Bob'], 'Age': [25, 30, 40], 'Country': ['USA', 'Canada', 'UK']})
print_ascii_table_from_dataframe(df, alignment='center')
# Output:
# +-------+-----+---------+
# |  Name | Age | Country |
# +-------+-----+---------+
# |  John |  25 |   USA   |
# | Alice |  30 |  Canada |
# |  Bob  |  40 |    UK   |
# +-------+-----+---------+
```

**Parameters:**

- `df` (pd.DataFrame): A pandas DataFrame.
- `alignment` (str, optional): The alignment of the table cells ('left', 'right', 'center'). Defaults to 'left'.

**Returns:**

- None

---

#### `print_columns`

Prints a formatted string representation of a list of columns.

```python
from fbpyutils_db import print_columns

cols = ['Name', 'Age', 'Address']
print_columns(cols, length=10, quotes=True)
# 'Name'    , 'Age'     , 'Address'
```

**Parameters:**

- `cols` (List[str]): A list of column names.
- `normalize` (bool, optional): If True, normalizes the columns before printing (requires valid column names for normalization). Defaults to False.
- `length` (int, optional): The desired padded length for each column name. If None, determined automatically. Defaults to None.
- `quotes` (bool, optional): If True, adds single quotes around each column name. Defaults to False.

**Returns:**

- None

---

#### `table_operation`

Performs append, upsert, or replace operations on a database table using data from a DataFrame.

```python
from sqlalchemy import create_engine
import pandas as pd
from fbpyutils_db import table_operation

df = pd.DataFrame({'id': [1, 2, 3], 'value': ['A', 'B', 'C']})
engine = create_engine('sqlite:///:memory:')
# Ensure table exists first (e.g., using create_table)
create_table(df, engine, 'my_data_table', keys=['id'], index='primary')

# Upsert operation
result = table_operation('upsert', df, engine, 'my_data_table', keys=['id'], commit_at=10)
print(result)
# {'operation': 'upsert', 'table_name': '.my_data_table', 'insertions': 3, 'updates': 0, 'skips': 0, 'failures': []}

# Append operation (will skip existing keys if table has unique constraint)
df_new = pd.DataFrame({'id': [3, 4], 'value': ['D', 'E']})
result_append = table_operation('append', df_new, engine, 'my_data_table', keys=['id'], commit_at=10)
print(result_append)
# {'operation': 'append', 'table_name': '.my_data_table', 'insertions': 1, 'updates': 0, 'skips': 1, 'failures': []}

# Replace operation
df_replace = pd.DataFrame({'id': [5, 6], 'value': ['F', 'G']})
result_replace = table_operation('replace', df_replace, engine, 'my_data_table', keys=['id'], commit_at=10)
print(result_replace)
# {'operation': 'replace', 'table_name': '.my_data_table', 'insertions': 2, 'updates': 0, 'skips': 0, 'failures': []}
```

**Parameters:**

- `operation` (str): The operation to perform ('append', 'upsert', 'replace').
- `dataframe` (pd.DataFrame): The DataFrame containing the data.
- `engine` (Engine): The SQLAlchemy engine connection.
- `table_name` (str): The name of the target table.
- `schema` (str, optional): The database schema name. Defaults to None.
- `keys` (List[str], optional): List of column names to use as keys (mandatory for 'upsert').
- `index` (str, optional): If the table doesn't exist, specifies the index type ('standard', 'unique', 'primary') to create using `keys`. Defaults to None.
- `commit_at` (int, optional): Number of rows to process before committing. Defaults to 50.

**Returns:**

- Dict[str, Any]: A dictionary containing results: operation type, table name, counts of insertions, updates, skips, and a list of failures.

---

### Internal Functions (Usually not called directly)

#### `_check_columns`

Checks if all specified columns exist in the DataFrame.

**Parameters:**

- `df` (pd.DataFrame): The DataFrame to check.
- `columns` (List[str]): List of column names to check.

**Returns:**

- bool: True if all columns exist, False otherwise.

---

#### `_create_hash_column`

Creates a pandas Series containing MD5 hashes of the input Series values.

**Parameters:**

- `x` (pd.Series): The input Series whose values will be hashed.
- `y` (int, optional): The length of the hash string. Defaults to 12.

**Returns:**

- pd.Series: A Series containing the truncated MD5 hashes.

---

#### `_deal_with_nans`

Handles various null/NaN representations (NaN, None, empty string, NaT) and returns None for them, otherwise returns the original value.

**Parameters:**

- `x` (Any): The input value to check.

**Returns:**

- Any: None if the input is considered null/NaN/NaT, otherwise the original input `x`.

---

## Contributing

Instructions on how to contribute to the project, including setting up the development environment and guidelines for pull requests, can be found in the main project repository or contributing guidelines file (if available). Typically involves forking the repository, creating a feature branch, making changes, adding tests, and submitting a pull request.

## Support

For support, reporting bugs, or suggesting new features, please use the issue tracker on the [project's GitHub repository](https://github.com/fcjbispo/fbpyutils-db).

## License

[MIT](https://opensource.org/licenses/MIT)
