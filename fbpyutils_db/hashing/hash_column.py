import pandas as pd
import hashlib
from typing import List, Union

# Importa _check_columns do módulo utils.validators
from fbpyutils_db.utils.validators import check_columns

def create_hash_column(x: Union[str, pd.Series], y: int = 12) -> pd.Series:
    """
    Creates a new hash column based on the values of an existing column in the dataframe.
    The hash is generated using MD5 and truncated to 'y' number of characters.

    Parameters:
    ----------
    x : str or pd.Series
        The column from the dataframe whose values will be hashed.
    y : int, optional (default=12)
        The length of the hash string to return.

    Returns:
    -------
    pd.Series
        A new pandas Series containing the MD5 hash of the input column values.

    Example:
    --------
    >>> df = pd.DataFrame({'SomeColumn': ['value1', 'value2']})
    >>> create_hash_column(df['SomeColumn'])
    0    b'f96b61d7...a3f8b1cdd'
    1    b'f96b61d7...a3f8b1cde'
    """
    if isinstance(x, pd.DataFrame):
        # Para DataFrames, concatenar valores de cada linha
        def hash_row(row):
            # Tratar valores NaN/None
            values = [str(v) if pd.notna(v) else '' for v in row.values]
            combined = '|'.join(values)
            return hashlib.md5(combined.encode()).hexdigest()[:y]
        
        return x.apply(hash_row, axis=1)
    else:
        # Para Series únicas
        def safe_hash(value):
            if pd.isna(value):
                value = ''
            return hashlib.md5(str(value).encode()).hexdigest()[:y]
        
        return x.apply(safe_hash)


def add_hash_column(
    df: pd.DataFrame, column_name: str, length: int = 12, columns: List[str] = []
) -> pd.DataFrame:
    """
    Adds a hash column to the given DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column_name (str): The name of the column to be created.
        length (int) optional: The length of the column to be created. Defaults to 12.
        columns (list) optional: The columns names to be used as part of the hash column.
            If None or empty list (default) all columns will be used.
    Returns:
        pandas.DataFrame: A new DataFrame with the hash column added as the first column.
                        The order of other columns remains the same.
    """
    # Parameter checks
    if not isinstance(df, pd.DataFrame):
        # logger.error("Invalid DataFrame type provided") # Removido logger, pois não está disponível aqui
        raise TypeError("The 'df' parameter should be of type pandas.DataFrame.")
    if not isinstance(column_name, str):
        # logger.error("Invalid column_name type provided")
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
    
    # logger.debug(f"Adding hash column '{column_name}' with length={length}")
    # logger.debug(f"Using columns for hash: {columns if columns else 'all columns'}")
    # logger.debug(f"Input DataFrame shape: {df.shape}")
    
    # Creates the hash column
    if columns:
        xdf = df[columns].copy()
        # logger.debug(f"Using subset of columns: {columns}")
    else:
        xdf = df.copy()
        # logger.debug("Using all columns for hash generation")
    
    df[column_name] = create_hash_column(xdf, length)
    xcolumns = [column_name, *[c for c in df.columns if c != column_name]]
    
    # logger.info(f"Successfully added hash column '{column_name}' to DataFrame")
    # logger.debug(f"New DataFrame shape: {df.shape}")
    
    return df[xcolumns].copy()
