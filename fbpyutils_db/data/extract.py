"""Utilities for extracting data from Pandas DataFrames.

This module provides functions to convert Pandas DataFrames into list-based formats suitable for database operations or other processing.

Example:
    import pandas as pd
    from fbpyutils_db.data.extract import get_data_from_pandas
    
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    data, columns = get_data_from_pandas(df)
    # data: [[1, 3], [2, 4]]
    # columns: ['A', 'B']
"""
import pandas as pd
from typing import Any, List, Tuple

from fbpyutils_db import logger

def get_data_from_pandas(
    df: pd.DataFrame, include_index: bool = False
) -> Tuple[List[List[Any]], List[str]]:
    """
    Extracts data and column names from a Pandas DataFrame.

    Args:
        df: The input Pandas DataFrame.
        include_index: If True, includes the index as a column. Defaults to False.

    Returns:
        Tuple of (data rows as list of lists, column names as list).

    Raises:
        TypeError: If input is not a Pandas DataFrame.

    Example:
        import pandas as pd
        from fbpyutils_db.data.extract import get_data_from_pandas
        
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        data, columns = get_data_from_pandas(df, include_index=True)
        # data: [[0, 1, 3], [1, 2, 4]] (includes index as first column)
        # columns: ['Index', 'A', 'B']
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
