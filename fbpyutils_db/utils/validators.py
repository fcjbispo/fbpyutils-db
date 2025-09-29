import pandas as pd
from typing import List

def check_columns(df: pd.DataFrame, columns: List[str]) -> bool:
    """
    Verify if all specified columns exist in the DataFrame.

    Args:
        df: Input DataFrame.
        columns: List of column names to check.

    Returns:
        bool: True if all columns present, False otherwise.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> check_columns(df, ['A', 'B'])
        True
        >>> check_columns(df, ['A', 'C'])
        False
        # Returns True only if all columns exist.
    """
    return all(c in df.columns for c in columns)
