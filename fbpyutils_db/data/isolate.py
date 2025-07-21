import pandas as pd
from typing import List

from fbpyutils_db import logger

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
