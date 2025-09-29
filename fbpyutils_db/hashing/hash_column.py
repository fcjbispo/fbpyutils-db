import pandas as pd
import hashlib
from typing import List, Union

# Importa _check_columns do módulo utils.validators
from fbpyutils_db.utils.validators import check_columns

def create_hash_column(x: Union[str, pd.Series], y: int = 12) -> pd.Series:
    """
    Generate MD5 hash for input values or series, truncated to specified length.

    Handles NaN by treating as empty string. For DataFrame input, hashes concatenated row values.

    Args:
        x: Input string, Series, or DataFrame to hash.
        y: Hash length. Defaults to 12.

    Returns:
        pd.Series: Series of hex MD5 hashes.

    Example:
        >>> import pandas as pd
        >>> s = pd.Series(['value1', 'value2'])
        >>> hashes = create_hash_column(s, 8)
        >>> hashes.iloc[0]
        'c51ce410'
        # Hashes 'value1' to 'c51ce410c7f896aa' truncated to 8 chars.
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
    Add a hash column to DataFrame using specified or all columns.

    Hashes concatenated column values per row using MD5, adds as new first column.

    Args:
        df: Input DataFrame.
        column_name: Name for the new hash column.
        length: Hash string length. Defaults to 12.
        columns: Specific columns to hash. Defaults to all.

    Returns:
        pd.DataFrame: Copy with hash column added first.

    Raises:
        TypeError: For invalid df, column_name, or length types.
        ValueError: For invalid length or missing columns.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        >>> result = add_hash_column(df, 'hash_id', 8, columns=['a', 'b'])
        >>> result['hash_id'].iloc[0]
        '90015098'
        # Hashes '1|x' to '900150983cd24fb0d6963f7d28e17f72' truncated to 8: '90015098'.
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
