import pandas as pd
from typing import List

# Importa _create_hash_column do módulo hash_column
from fbpyutils_db.hashing.hash_column import create_hash_column
# Importa _check_columns do módulo utils.validators
from fbpyutils_db.utils.validators import check_columns

def add_hash_index(
    df: pd.DataFrame, index_name: str = "id", length: int = 12, columns: List[str] = []
) -> pd.DataFrame:
    """
    Replace DataFrame index with MD5 hash of row values, renamed to index_name.

    Uses all or specified columns to generate unique hash index per row.

    Args:
        df: Input DataFrame.
        index_name: Name for the new hash index. Defaults to 'id'.
        length: Hash string length. Defaults to 12.
        columns: Specific columns to hash. Defaults to all.

    Returns:
        pd.DataFrame: Copy with hash-based index.

    Raises:
        TypeError: For invalid df, index_name, or length types.
        ValueError: For invalid length or missing columns.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        >>> result = add_hash_index(df, 'hash_idx', 8)
        >>> result.index[0]
        '90015098'
        # Hashes row '1|a' to '90015098', sets as index named 'hash_idx'.
    """
    # Parameter checks
    if not isinstance(df, pd.DataFrame):
        # logger.error("Invalid DataFrame type provided")
        raise TypeError("The 'df' parameter should be of type pandas.DataFrame.")
    if not isinstance(index_name, str):
        # logger.error("Invalid index_name type provided")
        raise TypeError("The 'index_name' parameter should be a string.")
    if not isinstance(length, int):
        # logger.error("Invalid length type provided")
        raise TypeError("The 'length' parameter should be an integer.")
    if length <= 0:
        # logger.error("Invalid length value provided")
        raise ValueError("The 'length' parameter should be greater than 0.")
    if columns and type(columns) != list:
        # logger.error("Invalid columns type provided")
        raise ValueError("When given, columns must be a list of column names")
    if columns and not check_columns(df, columns):
        # logger.error("One or more specified columns not found in DataFrame")
        raise ValueError("When given, all column names should exist in the dataframe.")
    
    # logger.debug(f"Adding hash index '{index_name}' with length={length}")
    # logger.debug(f"Using columns for hash: {columns if columns else 'all columns'}")
    # logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Creates the hash column
    if columns:
        xdf = df[columns].copy()
        # logger.debug(f"Using subset of columns: {columns}")
    else:
        xdf = df.copy()
        # logger.debug("Using all columns for hash generation")
    
    hash_df = create_hash_column(xdf, length)
    # logger.debug(f"Generated {len(hash_df)} hash values for index")
    
    # Set the hash string as the new index
    df.index = hash_df
    # Rename the index
    df.index.name = index_name
    
    # logger.info(f"Successfully added hash index '{index_name}' to DataFrame")
    # logger.debug(f"New DataFrame shape: {df.shape}")
    
    return df
