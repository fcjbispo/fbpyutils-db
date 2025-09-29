"""
Visualization utilities for printing DataFrame tables and column lists.

Supports ASCII table output from DataFrames and formatted column printing.
"""
import pandas as pd
import re
from typing import Any, List

from fbpyutils_db import logger

# Importa funções de outros módulos de visualização e dados
from fbpyutils_db.visualization.ascii_table import print_ascii_table
from fbpyutils_db.data.extract import get_data_from_pandas
from fbpyutils_db.data.normalize import normalize_columns


def print_ascii_table_from_dataframe(df: pd.DataFrame, alignment: str = "left") -> None:
    """
    Print ASCII table from DataFrame by extracting data and headers.

    Uses get_data_from_pandas to convert DataFrame to list format.

    Args:
        df: Input pandas DataFrame.
        alignment: Cell alignment ('left', 'right', 'center'). Defaults to 'left'.

    Returns:
        None

    Raises:
        ValueError: If DataFrame extraction fails.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'Name': ['John', 'Alice'], 'Age': [25, 30]})
        >>> print_ascii_table_from_dataframe(df, 'center')
        +-------+-----+
        | Name  | Age |
        +-------+-----+
        | John  |  25 |
        | Alice |  30 |
        +-------+-----+
        # Prints centered ASCII table from DataFrame.
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


def print_columns(
    cols: List[str], normalize: bool = False, length: int = None, quotes: bool = False
) -> None:
    """
    Print formatted list of column names, optionally normalized and padded.

    Normalizes to lowercase if specified, adds quotes, pads to max length.

    Args:
        cols: List of column names.
        normalize: Convert to lowercase. Defaults to False.
        length: Pad width. Defaults to max column length.
        quotes: Enclose in single quotes. Defaults to False.

    Returns:
        None

    Example:
        >>> cols = ['Name', 'Age', 'Address']
        >>> print_columns(cols, normalize=True, length=10, quotes=True)
        'name     ', 'age      ', 'address  '
        # Prints quoted, normalized, left-padded columns.
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
