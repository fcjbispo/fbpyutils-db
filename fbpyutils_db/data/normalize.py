import re
from typing import List

from fbpyutils_db import logger

def normalize_columns(cols: List[str]) -> List[str]:
    """
    Normalizes a list of column names by removing special characters and converting to lowercase.

    Args:
        cols (list): A list of column names.

    Returns:
        list: A list of normalized column names.

    Raises:
        ValueError: If any column name contains only special characters.

    Example:
        >>> cols = ['Name!', 'Age@', '#Address']
        >>> normalize_columns(cols)
        ['name', 'age', 'address']
    """
    logger.debug(f"Normalizing {len(cols)} column names")
    normalized = []
    
    for col in cols:
        # Remove special characters and convert to lowercase
        normalized_col = re.sub("[^0-9a-zA-Z_]+", "", col).lower()
        
        # Check if the column name is empty after normalization
        if not normalized_col:
            logger.error(f"Column name '{col}' contains only special characters and cannot be normalized")
            raise ValueError(
                f"Column name '{col}' contains only special characters and cannot be normalized."
            )
        
        normalized.append(normalized_col)
    
    logger.debug(f"Successfully normalized columns: {normalized}")
    return normalized
