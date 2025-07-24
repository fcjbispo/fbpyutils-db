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
    Replaces the dataframe index with a hash string with length of 12 characters
    calculated using all columns values for each row and renames the dataframe index
    to the name supplied by index_name.
    Parameters:
    -----------
    df : pd.DataFrame
        A pandas dataframe.
    index_name : str
        The name to be given to the new index. Defaults to 'id'
    length : int
        The length of the column to be created. Defaults to 12.
    columns : list optional
        The columns names to be used as part of the hash column.
        If None or empty list (default) all columns will be used.
    Returns:
    --------
    pd.DataFrame
        A pandas dataframe with the new index.
    Example:
    --------
    >>> df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    >>> add_hash_index(df, 'new_index')
            col1 col2
    new_index
    8b9c45e2a9f6   1   a
    3d4c4f4f4d1f   2   b
    5b5d8c7a2a4c   3   c
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
