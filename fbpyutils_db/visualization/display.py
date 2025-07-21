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
