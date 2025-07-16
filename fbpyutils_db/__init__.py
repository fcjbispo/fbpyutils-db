"""
Utility functions to manipulate data, tables and dataframes.
"""

import os
import re
from typing import Any, Dict, List, Tuple, Union
import pandas as pd
import numpy as np
from sqlalchemy import (
    Engine,
    Selectable,
    inspect,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    text,
    Index,
)
from sqlalchemy.sql.sqltypes import TypeEngine
from sqlalchemy.sql import exists
from datetime import datetime, date
import hashlib

import fbpyutils


def _deal_with_nans(x: Any) -> Any:
    """
    This function handles null values and data types within a given input `x`. It checks if the input is a NaN value, None, an empty string, or a datetime/date with a NaT (not a time) value, and returns None for these cases. For other numeric types like float or int, it checks if the value is actually NaN. For datetime/date types, it checks if the value is a NaT value. If the input is of any other type, it returns the input as-is.

    Parameters:
    x (any): The input variable that may contain null values or special cases that need to be handled.

    Returns:
    The function returns `None` if the input is NaN, None, an empty string, a datetime with NaT, or a date with NaT. Otherwise, it returns the original input value.
    """
    if pd.isna(x) or x is None or (isinstance(x, str) and not x):
        return None
    elif isinstance(x, (float, np.float64)) and np.isnan(x):
        return None
    elif isinstance(x, (datetime, pd.Timestamp)) and pd.isna(x):
        return None
    elif isinstance(x, date) and pd.isna(pd.Timestamp(x)):
        return None
    return x


def isolate(df: pd.DataFrame, group_columns: List[str]):
    """
    Filters the dataframe to isolate rows with maximum values in unique_columns
    for each unique combination of values in group_columns.
    Parameters:
    -----------
    df : pd.DataFrame
        The input pandas dataframe.
    group_columns : list
        A list of column names used for grouping the dataframe.
    Returns:
    --------
    pd.DataFrame
        A pandas dataframe containing only the rows with maximum values in unique_columns
        for each unique combination of values in group_columns.
    Example:
    --------
    >>> df = pd.DataFrame({'Group': ['A', 'A', 'B', 'B'],
    ...                    'Value': [1, 2, 3, 4],
    ...                    'Unique': [5, 6, 7, 8]})
    >>> isolate(df, ['Group'], ['Value', 'Unique'])
      Group  Value  Unique
    1     A      2       6
    3     B      4       8
    """
    logger.debug(f"Starting isolate operation with group_columns: {group_columns}")
    logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Find the index of the row with the maximum 'Unique' value for each group
    idx = df.groupby(group_columns)["Unique"].idxmax()
    
    result = df.loc[idx]
    logger.info(f"Isolate operation completed. Result DataFrame shape: {result.shape}")
    
    return result


def _create_hash_column(x: Union[str, pd.Series], y: int = 12) -> pd.Series:
    """
    Creates a new hash column based on the values of an existing column in the dataframe.
    The hash is generated using MD5 and truncated to 'y' number of characters.

    Parameters:
    ----------
    x : str or pd.Series
        The column from the dataframe whose values will be hashed.
    y : int, optional (default=12)
        The length of the hash string to return.

    Returns:
    -------
    pd.Series
        A new pandas Series containing the MD5 hash of the input column values.

    Example:
    --------
    >>> df = pd.DataFrame({'SomeColumn': ['value1', 'value2']})
    >>> _create_hash_column(df['SomeColumn'])
    0    b'f96b61d7...a3f8b1cdd'
    1    b'f96b61d7...a3f8b1cde'
    """
    return x.apply(
        lambda value: hashlib.md5(str(value).encode()).hexdigest()[:y], axis=1
    )


def _check_columns(df: pd.DataFrame, columns: List[str]) -> bool:
    """Checks if all the specified columns exist in the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe to check column existence in.
    columns (list): A list of column names to check for existence.

    Returns:
    bool: True if all columns exist, False otherwise.

    Example:
    >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> _check_columns(df, ['A', 'C'])
    True
    >>> _check_columns(df, ['A', 'B', 'C'])
    True
    >>> _check_columns(df, ['A', 'D'])
    False
    """
    return all(c in df.columns for c in columns)


def add_hash_column(
    df: pd.DataFrame, column_name: str, length: int = 12, columns: List[str] = []
) -> pd.DataFrame:
    """
    Adds a hash column to the given DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column_name (str): The name of the column to be created.
        length (int) optional: The length of the column to be created. Defaults to 12.
        columns (list) optional: The columns names to be used as part of the hash column.
            If None or empty list (default) all columns will be used.
    Returns:
        pandas.DataFrame: A new DataFrame with the hash column added as the first column.
                          The order of other columns remains the same.
    """
    # Parameter checks
    if not isinstance(df, pd.DataFrame):
        logger.error("Invalid DataFrame type provided")
        raise TypeError("The 'df' parameter should be of type pandas.DataFrame.")
    if not isinstance(column_name, str):
        logger.error("Invalid column_name type provided")
        raise TypeError("The 'index_name' parameter should be a string.")
    if not isinstance(length, int):
        logger.error("Invalid length type provided")
        raise TypeError("The 'length' parameter should be an integer.")
    if length <= 0:
        logger.error("Invalid length value provided")
        raise ValueError("The 'length' parameter should be greater than 0.")
    if columns and type(columns) != list:
        logger.error("Invalid columns type provided")
        raise ValueError("When given, columns must be a list of column names")
    if columns and not _check_columns(df, columns):
        logger.error("One or more specified columns not found in DataFrame")
        raise ValueError("When given, all column names should exist in the dataframe.")
    
    logger.debug(f"Adding hash column '{column_name}' with length={length}")
    logger.debug(f"Using columns for hash: {columns if columns else 'all columns'}")
    logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Creates the hash column
    if columns:
        xdf = df[columns].copy()
        logger.debug(f"Using subset of columns: {columns}")
    else:
        xdf = df.copy()
        logger.debug("Using all columns for hash generation")
    
    df[column_name] = _create_hash_column(xdf, length)
    xcolumns = [column_name, *[c for c in df.columns if c != column_name]]
    
    logger.info(f"Successfully added hash column '{column_name}' to DataFrame")
    logger.debug(f"New DataFrame shape: {df.shape}")
    
    return df[xcolumns].copy()


def add_hash_index(
    df: pd.DataFrame, index_name: str = "id", length: int = 12, columns: List[str] = []
) -> pd.DataFrame:
    """
    Replaces the dataframe index with a hash string with length of 12 characters
    calculated using all columns values for each row and renames the dataframe index
    to the name supplied by index_name.
    Parameters:
    -----------
    df : pd.DataFrame
        A pandas dataframe.
    index_name : str
        The name to be given to the new index. Defaults to 'id'
    length : int
        The length of the column to be created. Defaults to 12.
    columns : list optional
        The columns names to be used as part of the hash column.
        If None or empty list (default) all columns will be used.
    Returns:
    --------
    pd.DataFrame
        A pandas dataframe with the new index.
    Example:
    --------
    >>> df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    >>> add_hash_index(df, 'new_index')
               col1 col2
    new_index
    8b9c45e2a9f6   1   a
    3d4c4f4f4d1f   2   b
    5b5d8c7a2a4c   3   c
    """
    # Parameter checks
    if not isinstance(df, pd.DataFrame):
        logger.error("Invalid DataFrame type provided")
        raise TypeError("The 'df' parameter should be of type pandas.DataFrame.")
    if not isinstance(index_name, str):
        logger.error("Invalid index_name type provided")
        raise TypeError("The 'index_name' parameter should be a string.")
    if not isinstance(length, int):
        logger.error("Invalid length type provided")
        raise TypeError("The 'length' parameter should be an integer.")
    if length <= 0:
        logger.error("Invalid length value provided")
        raise ValueError("The 'length' parameter should be greater than 0.")
    if columns and type(columns) != list:
        logger.error("Invalid columns type provided")
        raise ValueError("When given, columns must be a list of column names")
    if columns and not _check_columns(df, columns):
        logger.error("One or more specified columns not found in DataFrame")
        raise ValueError("When given, all column names should exist in the dataframe.")
    
    logger.debug(f"Adding hash index '{index_name}' with length={length}")
    logger.debug(f"Using columns for hash: {columns if columns else 'all columns'}")
    logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Creates the hash column
    if columns:
        xdf = df[columns].copy()
        logger.debug(f"Using subset of columns: {columns}")
    else:
        xdf = df.copy()
        logger.debug("Using all columns for hash generation")
    
    hash_df = _create_hash_column(xdf, length)
    logger.debug(f"Generated {len(hash_df)} hash values for index")
    
    # Set the hash string as the new index
    df.index = hash_df
    # Rename the index
    df.index.name = index_name
    
    logger.info(f"Successfully added hash index '{index_name}' to DataFrame")
    logger.debug(f"New DataFrame shape: {df.shape}")
    
    return df


def table_operation(
    operation: str,
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = None,
    keys: list[str] = None,
    index: str = None,
    commit_at: int = 50,
) -> Dict[str, Any]:
    """
    Perform upsert or replace operation on a table based on the provided dataframe.

    Args:
        operation (str, optional): The operation to be performed ('upsert' or 'replace').
        dataframe (pd.DataFrame): The pandas DataFrame containing the data to be inserted or updated.
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine engine.
        table_name (str): The name of the table to operate on.
        schema (str, optional): the schena name to preffix the table objects.
        keys (list of str, optional for operation=replace): List of column names to use as keys for upsert operation.
        index (str, optional): Whether to create an index and what kind using the keys. Default is None (not create index).
            If an index must be created, index be in 'standard' or 'unique'.
        commit_at (int, optional): Number of rows to commit in the database at once. Defaults to 50.
            Must be > 1 and < total rows of the dataframe.

    Returns:
        dict: A dictionary containing information about the performed operation.

    """
    logger.info(f"Starting table operation: {operation}")
    logger.debug(f"Table: {table_name}, Schema: {schema}")
    logger.debug(f"DataFrame shape: {dataframe.shape}")
    logger.debug(f"Keys: {keys}, Index: {index}, Commit at: {commit_at}")
    
    # Check parameters
    if operation not in ("append", "upsert", "replace"):
        logger.error(f"Invalid operation: {operation}")
        raise ValueError("Invalid operation. Valid values: append|upsert|replace.")

    if not type(dataframe) == pd.DataFrame:
        logger.error("Invalid DataFrame type provided")
        raise ValueError("Dataframe must be a Pandas DataFrame.")

    if operation == "upsert" and not keys:
        logger.error("Missing keys parameter for upsert operation")
        raise ValueError("For upsert operation 'keys' parameter is mandatory.")

    if keys and not type(keys) == list:
        logger.error("Invalid keys type provided")
        raise ValueError("Parameters 'keys' must be a list of str.")

    if (keys and index) and index not in ("standard", "unique", "primary"):
        logger.error(f"Invalid index type: {index}")
        raise ValueError(
            "If an index will be created, it must be any of standard|unique|primary."
        )

    commit_at = commit_at or 50
    if not type(commit_at) == int or (commit_at < 1 and commit_at > len(dataframe)):
        logger.error(f"Invalid commit_at value: {commit_at}")
        raise ValueError("Commit At must be > 1 and < total rows of DataFrame.")

    # Check if the table exists in the database, if not create it
    table_exists = inspect(engine).has_table(table_name, schema=schema)
    logger.debug(f"Table '{table_name}' exists: {table_exists}")
    
    if not table_exists:
        logger.info(f"Creating table '{table_name}' as it doesn't exist")
        create_table(dataframe, engine, table_name, schema, keys, index)

    # Get the table object
    metadata = MetaData(schema)
    table = Table(table_name, metadata, autoload_with=engine)

    # Initialize reports for insertions, updates, and failures
    inserts = 0
    updates = 0
    skips = 0
    failures = []
    
    logger.info(f"Starting {operation} operation on {len(dataframe)} rows")

    try:
        with engine.connect() as conn:
            step = "drop table"
            if operation == "replace":
                logger.info("Performing replace operation - clearing table")
                conn.execute(table.delete())
                conn.commit()
                logger.debug("Table cleared successfully")

            rows = 0
            processed_rows = 0
            
            for i, row in dataframe.iterrows():
                try:
                    values = {
                        col: _deal_with_nans(row[col]) for col in dataframe.columns
                    }
                    
                    logger.debug(f"Processing row {i}: {values}")

                    row_exists = False
                    step = "check existence"
                    if keys:
                        # Check if row exists in the table based on keys
                        exists_query = (
                            table.select()
                            .where(
                                exists(
                                    table.select().where(
                                        text(
                                            " AND ".join(
                                                [f"{col} = :{col}" for col in keys]
                                            )
                                        )
                                    )
                                )
                            )
                            .params(**values)
                        )
                        if conn.execute(exists_query).fetchone():
                            row_exists = True
                            logger.debug(f"Row {i} exists based on keys {keys}")
                    
                    if row_exists:
                        if operation == "upsert":
                            # Perform update
                            step = "replace with update"
                            update_values = {
                                k: values[k] for k in values.keys() if k not in keys
                            }
                            
                            logger.debug(f"Updating row {i} with values: {update_values}")

                            update_stmt = (
                                table.update()
                                .where(
                                    text(
                                        " AND ".join([f"{col}=:{col}" for col in keys])
                                    )
                                )
                                .values(**update_values)
                            )

                            update_stmt = text(str(update_stmt))
                            conn.execute(update_stmt, values)
                            updates += 1
                            logger.debug(f"Row {i} updated successfully")
                        else:
                            skips += 1
                            logger.debug(f"Row {i} skipped (already exists)")
                    else:
                        # Perform insert
                        step = "perform insert"
                        insert_stmt = table.insert().values(**values)
                        conn.execute(insert_stmt)
                        inserts += 1
                        logger.debug(f"Row {i} inserted successfully")

                    rows += 1
                    processed_rows += 1
                    
                    if rows >= commit_at:
                        conn.commit()
                        logger.debug(f"Committed {rows} rows")
                        rows = 0
                        
                    if processed_rows % 100 == 0:
                        logger.info(f"Processed {processed_rows}/{len(dataframe)} rows")
                        
                except Exception as e:
                    logger.error(f"Error processing row {i}: {str(e)}")
                    failures.append(
                        {
                            "step": step,
                            "row": (
                                i,
                                ", ".join(
                                    [f"{k}='{str(v)}'" for k, v in values.items()]
                                ),
                            ),
                            "error": str(e),
                        }
                    )
                    conn.rollback()
                    continue
            conn.commit()
            logger.info(f"Operation completed. Total processed: {processed_rows}")
    except Exception as e:
        logger.error(f"Critical error in table operation: {str(e)}")
        conn.rollback()
        failures.append({"step": step, "row": None, "error": str(e)})

    result = {
        "operation": operation,
        "table_name": ".".join([schema, table_name]),
        "insertions": inserts,
        "updates": updates,
        "skips": skips,
        "failures": failures,
    }
    
    logger.info(f"Operation summary: {inserts} inserts, {updates} updates, {skips} skips, {len(failures)} failures")
    
    if failures:
        logger.warning(f"Operation completed with {len(failures)} failures")
        for failure in failures[:5]:  # Log first 5 failures
            logger.warning(f"Failure: {failure}")
    
    return result


def create_table(
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = None,
    keys: List[str] = [],
    index: str = None,
) -> None:
    """
    Create a table in the database using the provided pandas DataFrame as a schema.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame containing the schema information.
        table_name (str): The name of the table to be created.
        schema (str, optional): The name of the schema to be created. Default is None.
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine engine.
        keys (list of str, optional): List of column names to use as keys for index creation. Default is None.
        index (str, optional): Whether to create an index and what kind using the keys. Default is None (not create index).
            If an index muste be created, index be in 'standard' or 'unique'.

    """
    logger.info(f"Creating table '{table_name}' in schema '{schema}'")
    
    # Check parameters
    if not type(dataframe) == pd.DataFrame:
        logger.error("Invalid dataframe type provided")
        raise ValueError("Dataframe must be a Pandas DataFrame.")

    if keys and not type(keys) == list:
        logger.error("Invalid keys type provided")
        raise ValueError("Parameters 'keys' must be a list of str.")

    if keys and index and index not in ("standard", "unique", "primary"):
        logger.error(f"Invalid index type: {index}")
        raise ValueError(
            "If an index will be created, it must be any of standard|unique|primary."
        )

    logger.debug(f"Creating table with keys: {keys}, index type: {index}")
    
    metadata = MetaData(schema)

    if keys and index == "primary":
        columns = get_columns_types(dataframe, primary_keys=keys)
    else:
        columns = get_columns_types(dataframe, primary_keys=[])

    table = Table(table_name, metadata, *columns)

    # Create the index if required
    if keys and index in ("standard", "unique"):
        unique = index == "unique"
        idx_suffix = "uk" if unique else "ik"
        index_name = f"{table_name}_i001_{idx_suffix}"
        logger.debug(f"Creating {index} index '{index_name}' on columns: {keys}")
        table.indexes.add(
            create_index(index_name, table, keys, unique)
        )

    logger.info(f"Creating table structure in database")
    result = metadata.create_all(engine)
    logger.info(f"Table '{table_name}' created successfully")
    return result


def create_index(
    name: str, table: Selectable, keys: List[str], unique: bool = True
) -> Index:
    """Create an index on the specified keys for a given table.

    Args:
        name (str): The name of the index to be created.
        table (sqlalchemy.sql.expression.Selectable): The table on which to create the index.
        keys (list of str): A list of column names that should be part of the index.
        unique (bool, optional): Whether the index should enforce uniqueness. Default is True.
    """
    logger.debug(f"Creating index '{name}' on columns: {keys}, unique: {unique}")
    
    index_cols = [c for c in table.columns if c.name in keys]
    if not index_cols:
        logger.warning(f"No columns found for index '{name}' with keys: {keys}")
        raise ValueError(f"No matching columns found for keys: {keys}")
    
    index_obj = Index(name, *index_cols, unique=unique)
    logger.debug(f"Index '{name}' created successfully with {len(index_cols)} columns")
    
    return index_obj


def get_columns_types(
    dataframe: pd.DataFrame, primary_keys: List[str] = []
) -> List[Column]:
    """
    Returns a list of Column objects representing the columns of the given dataframe.
     Args:
        dataframe (pandas.DataFrame): The input dataframe for which column types are to be determined.
        primary_keys (List[str]): Optional list of primary key column names.
     Returns:
        list: A list of Column objects, where each object represents a column in the dataframe.
     Raises:
        None.
     Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        >>> get_columns_types(df)
        [Column('A', 'int64'), Column('B', 'object')]
     Column object:
        - The Column object represents a column in a dataframe and stores its name and type.
         Attributes:
            name (str): The name of the column.
            dtype (str): The data type of the column.
         Example:
            >>> col = Column('A', 'int64')
            >>> col.name
            'A'
            >>> col.dtype
            'int64'
    """
    logger.debug(f"Getting column types for DataFrame with {len(dataframe.columns)} columns")
    logger.debug(f"Primary keys: {primary_keys}")
    
    columns = []
    for col in dataframe.columns:
        col_type = get_column_type(dataframe.dtypes[col])
        is_primary = col in primary_keys
        logger.debug(f"Column '{col}': type={col_type}, primary_key={is_primary}")
        columns.append(
            Column(
                col,
                col_type,
                primary_key=is_primary,
            )
        )
    
    logger.info(f"Generated {len(columns)} column definitions")
    return columns


def get_column_type(dtype: str) -> TypeEngine:
    """
    Map Pandas data types to SQLAlchemy data types.

    Args:
        dtype (dtype): The Pandas data type to be mapped.

    Returns:
        sqlalchemy.sql.sqltypes.TypeEngine: The corresponding SQLAlchemy data type.
        For string columns, a default 4000 chars lenght column is created.

    """
    logger.debug(f"Mapping pandas dtype '{dtype}' to SQLAlchemy type")
    
    if dtype in ("int64", "int32", "int"):
        sql_type = Integer()
    elif dtype in ("float64", "float32", "float"):
        sql_type = Float()
    elif dtype == "bool":
        sql_type = Boolean()
    elif dtype == "object":
        sql_type = String()
    elif dtype == "datetime64[ns]":
        sql_type = DateTime()
    else:
        logger.warning(f"Unknown pandas dtype '{dtype}', defaulting to String(4000)")
        sql_type = String(4000)
    
    logger.debug(f"Mapped '{dtype}' to {type(sql_type).__name__}")
    return sql_type


def get_data_from_pandas(
    df: pd.DataFrame, include_index: bool = False
) -> Tuple[List[List[Any]], List[str]]:
    """
    Extracts data and column names from a Pandas DataFrame.

    Args:
        df (pandas.DataFrame): A Pandas DataFrame.
        include_index (bool, optional): If True, includes the index column in the extracted data. Defaults to False.

    Returns:
        tuple: A tuple containing the extracted data and column names.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'Name': ['John', 'Alice', 'Bob'], 'Age': [25, 30, 40]})
        >>> data, columns = get_data_from_pandas(df)
        >>> print(data)
        [['John', 25], ['Alice', 30], ['Bob', 40]]
        >>> print(columns)
        ['Name', 'Age']
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Invalid input type provided, expected pandas DataFrame")
        raise TypeError("Input must be a pandas DataFrame")
    
    logger.debug(f"Extracting data from DataFrame with include_index={include_index}")
    logger.debug(f"Input DataFrame shape: {df.shape}")

    data = [list(d) for d in df.to_records(index=include_index)]
    columns = list(c for c in df.columns)

    if include_index:
        columns.insert(0, "Index")

    logger.info(f"Successfully extracted {len(data)} rows and {len(columns)} columns")
    logger.debug(f"Extracted columns: {columns}")
    
    return data, columns


def ascii_table(
    data: List[List[Any]],
    columns: List[str] = [],
    alignment: str = "left",
    numrows: int = None,
) -> List[str]:
    """
    Creates an ASCII table representation of the given data.

    Args:
        data (list): A list of lists representing the data rows.
        columns (list, optional): A list of column names. Defaults to an empty list.
        alignment (str, optional): The alignment of the table cells. Valid values are 'left', 'right', or 'center'. Defaults to 'left'.
        numrows (int, optional): The number of rows to display. If None, all rows are displayed. Defaults to None.

    Returns:
        list: A list of strings representing the ASCII table.

    Example:
        >>> data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
        >>> columns = ['Name', 'Age', 'Country']
        >>> table = ascii_table(data, columns=columns, alignment='center')
        >>> for line in table:
        ...     print(line)
        +-------+-----+---------+
        |  Name | Age | Country |
        +-------+-----+---------+
        |  John |  25 |   USA   |
        | Alice |  30 |  Canada |
        |  Bob  |  40 |    UK   |
        +-------+-----+---------+

    """
    logger.debug(f"Creating ASCII table with {len(data)} rows, {len(columns)} columns")
    logger.debug(f"Alignment: {alignment}, numrows: {numrows}")
    
    if len(data) == 0:
        logger.warning("Empty data provided to ascii_table")
        return None

    data = [list(e) for e in data]
    columns = list([c for c in columns])
    alignment = alignment or "left"

    def pad(x, size, char=" ", where="center"):
        char = char or " "
        where = where or "center"
        return (
            str(x).rjust(size, char)
            if where == "right"
            else (
                str(x).ljust(size, char)
                if where == "left"
                else str(x).center(size, char)
            )
        )

    def line(rows, sizes, where="center"):
        return (
            "|"
            + "|".join(
                [pad(rows[i], sizes[i], where=where) for i in range(0, len(rows))]
            )
            + "|"
        )

    col_lenghts = tuple(set([len(d) for d in data]))

    if len(col_lenghts) == 0:
        return None

    if len(col_lenghts) > 1:
        raise ValueError("Number of columns mismatch among rows.")

    if alignment not in ("left", "right", "center"):
        raise ValueError("Alignment valid values: left|right|center")

    if columns is None or len(columns) == 0:
        columns = [f"column_{i}" for i in range(0, col_lenghts[0])]

    if len(columns) != col_lenghts[0]:
        logger.error(f"Column length mismatch: data has {col_lenghts[0]} columns, but {len(columns)} provided")
        logger.debug(f"Column lengths: {col_lenghts}, columns: {columns}")
        raise ValueError(f"Number of columns mismatch with data row.")

    if numrows is None or numrows > len(data):
        numrows = len(data)
    xdata = [
        [row[i] for i in range(len(data[0])) if columns[i] in columns] for row in data
    ][0:numrows]

    max_sizes = list(
        max(n)
        for n in list(
            list(len(str(r[i])) for r in xdata) for i in range(0, len(xdata[0]))
        )
    )

    col_sizes = [len(str(c)) for c in columns]
    new_max_sizes = []
    for i, _ in enumerate(max_sizes):
        new_max_sizes.append(max(max_sizes[i], col_sizes[i]))
    max_sizes = new_max_sizes

    line_sep = "".join(["+" + "-" * i for i in max_sizes]) + "+"

    table = []
    table.append(line_sep)
    table.append(line(columns, max_sizes))
    table.append(line_sep)
    for row in data:
        table.append(line(row, max_sizes, where=alignment))
    table.append(line_sep)

    logger.debug(f"Successfully created ASCII table with {len(table)} lines")
    return table


def print_ascii_table(
    data: List[List[Any]],
    columns: List[str] = [],
    alignment: str = "left",
    numrows: int = None,
) -> None:
    """
    Prints the ASCII table representation of the given data.

    Args:
        data (list): A list of lists representing the data rows.
        columns (list, optional): A list of column names. Defaults to an empty list.
        alignment (str, optional): The alignment of the table cells. Valid values are 'left', 'right', or 'center'. Defaults to 'left'.

    Returns:
        None

    Example:
        >>> data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
        >>> columns = ['Name', 'Age', 'Country']
        >>> print_ascii_table(data, columns=columns, alignment='center')
        +-------+-----+---------+
        |  Name | Age | Country |
        +-------+-----+---------+
        |  John |  25 |   USA   |
        | Alice |  30 |  Canada |
        |  Bob  |  40 |    UK   |
        +-------+-----+---------+

    """
    if data is None:
        return None

    logger.info(f"Printing ASCII table with {len(data) if data else 0} rows")
    table = ascii_table(data, columns=columns, alignment=alignment, numrows=numrows)

    for line in table:
        print(line)
    logger.debug(f"Successfully printed ASCII table with {len(table)} lines")


def print_ascii_table_from_dataframe(df: pd.DataFrame, alignment: str = "left") -> None:
    """
    Prints the ASCII table representation of a pandas DataFrame.
    - Attempts to extract the data and column names from the pandas DataFrame using a helper function.
    - Raises a ValueError if the DataFrame is invalid.

    Args:
        df (pandas.DataFrame): A pandas DataFrame.
        alignment (str, optional): The alignment of the table cells. Valid values are 'left', 'right', or 'center'. Defaults to 'left'.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'Name': ['John', 'Alice', 'Bob'], 'Age': [25, 30, 40], 'Country': ['USA', 'Canada', 'UK']})
        >>> print_ascii_table_from_dataframe(df, alignment='center')
        +-------+-----+---------+
        |  Name | Age | Country |
        +-------+-----+---------+
        |  John |  25 |   USA   |
        | Alice |  30 |  Canada |
        |  Bob  |  40 |    UK   |
        +-------+-----+---------+

    """
    data, columns = None, None
    try:
        logger.info(f"Converting DataFrame to ASCII table with {len(df)} rows and {len(df.columns)} columns")
        data, columns = get_data_from_pandas(df)
        logger.debug(f"Successfully extracted data from DataFrame: {len(data)} rows, {len(columns)} columns")
    except Exception as e:
        logger.error(f"Failed to extract data from DataFrame: {e}")
        raise ValueError(f"Invalid pandas dataframe: {e}.")

    if all([data, columns]):
        logger.info("Data and columns extracted successfully, printing ASCII table")
        print_ascii_table(data, columns, alignment)
    else:
        logger.warning("No data or columns to display in ASCII table")


def normalize_columns(cols: List[str]) -> List[str]:
    """
    Normalizes a list of column names by removing special characters and converting to lowercase.

    Args:
        cols (list): A list of column names.

    Returns:
        list: A list of normalized column names.

    Raises:
        AttributeError: If any column name contains special characters that cannot be normalized.

    Example:
        >>> cols = ['Name!', 'Age@', '#Address']
        >>> normalize_columns(cols)
        ['name', 'age', 'address']
    """
    logger.debug(f"Normalizing {len(cols)} column names")
    # test if the column names contain special characters
    if any([re.search("[^0-9a-zA-Z_]+", x) for x in cols]):
        logger.warning(f"Column names contain special characters: {cols}")
        raise AttributeError(
            "Column names contain special characters that cannot be normalized."
        )
    normalized = [re.sub("[^0-9a-zA-Z_]+", "", x).lower() for x in cols]
    logger.debug(f"Successfully normalized columns: {normalized}")
    return normalized


def print_columns(
    cols: List[str], normalize: bool = False, length: int = None, quotes: bool = False
) -> None:
    """
    Prints a formatted string representation of a list of columns.

    Args:
        cols (list): A list of column names.
        normalize (bool, optional): If True, normalizes the columns before printing. Defaults to False.
        length (int, optional): The desired length for each column. If not provided, the length will be determined automatically. Defaults to None.
        quotes (bool, optional): If True, adds single quotes around each column name. Defaults to False.

    Returns:
        None

    Example:
        >>> cols = ['Name', 'Age', 'Address']
        >>> print_columns(cols, normalize=True, length=10, quotes=True)
        'name     ', 'age      ', 'address  '
    """
    logger.debug(f"Printing {len(cols)} columns with options: normalize={normalize}, length={length}, quotes={quotes}")
    
    if normalize:
        logger.debug("Normalizing column names")
        cols = normalize_columns(cols)

    if quotes:
        logger.debug("Adding quotes to column names")
        cols = [f"'{c}'" for c in cols]

    length = length or max([len(c) for c in cols])
    logger.debug(f"Using column length: {length}")

    colstrings = ", ".join([c.ljust(length, " ") for c in cols])
    
    logger.info(f"Columns: {colstrings}")
    print(colstrings)


fbpyutils.setup()

env = fbpyutils.get_env()
logger = fbpyutils.get_logger()
