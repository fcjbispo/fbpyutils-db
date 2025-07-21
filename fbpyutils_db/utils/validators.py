import pandas as pd
from typing import List

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
