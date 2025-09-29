"""Utilities for isolating rows with maximum 'Unique' values per group in DataFrames.

This module provides functions to select specific rows from DataFrames based on grouping and maximum values.

Example:
    import pandas as pd
    from fbpyutils_db.data.isolate import isolate
    
    df = pd.DataFrame({
        'group': ['A', 'A', 'B', 'B'],
        'Unique': [10, 20, 15, 25],
        'value': [1, 2, 3, 4]
    })
    result = isolate(df, group_columns=['group'])
    # result: DataFrame with rows where 'Unique' is max per group
    #         group  Unique  value
    #         A      20      2
    #         B      25      4
"""
import pandas as pd
from typing import List

from fbpyutils_db import logger

def isolate(df: pd.DataFrame, group_columns: List[str]):
    """
    Isolates rows with the maximum value in the 'Unique' column for each group defined by group_columns.

    Args:
        df: The input Pandas DataFrame. Must contain a 'Unique' column.
        group_columns: List of column names for grouping.

    Returns:
        pd.DataFrame: Filtered DataFrame containing the rows with max 'Unique' per group.

    Raises:
        KeyError: If 'Unique' column is missing or group_columns are invalid.

    Example:
        import pandas as pd
        from fbpyutils_db.data.isolate import isolate
        
        df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'Unique': [10, 20, 15, 25],
            'value': [1, 2, 3, 4]
        })
        result = isolate(df, group_columns=['group'])
        # Returns DataFrame:
        #   group  Unique  value
        #   A      20      2
        #   B      25      4
    """
    logger.debug(f"Starting isolate operation with group_columns: {group_columns}")
    logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Find the index of the row with the maximum 'Unique' value for each group
    idx = df.groupby(group_columns)["Unique"].idxmax()
    
    result = df.loc[idx]
    logger.info(f"Isolate operation completed. Result DataFrame shape: {result.shape}")
    
    return result
