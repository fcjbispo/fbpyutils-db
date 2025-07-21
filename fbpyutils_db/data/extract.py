import pandas as pd
from typing import Any, List, Tuple

from fbpyutils_db import logger

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
