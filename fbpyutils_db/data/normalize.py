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
