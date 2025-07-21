import pandas as pd
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql.sqltypes import TypeEngine
from typing import List

from fbpyutils_db import logger

def get_columns_types(
    dataframe: pd.DataFrame, primary_keys: List[str] = []
) -> List[Column]:
    """
    Returns a list of Column objects representing the columns of the given dataframe.
    Args:
        dataframe (pandas.DataFrame): The input dataframe for which column types are to be determined.
        primary_keys (List[str]): Optional list of primary key column names.
    Returns:
        list: A list of Column objects, where each object represents a column in the dataframe.
    Raises:
        None.
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        >>> get_columns_types(df)
        [Column('A', 'int64'), Column('B', 'object')]
    Column object:
        - The Column object represents a column in a dataframe and stores its name and type.
        Attributes:
            name (str): The name of the column.
            dtype (str): The data type of the column.
        Example:
            >>> col = Column('A', 'int64')
            >>> col.name
            'A'
            >>> col.dtype
            'int64'
    """
    logger.debug(f"Getting column types for DataFrame with {len(dataframe.columns)} columns")
    logger.debug(f"Primary keys: {primary_keys}")
    
    columns = []
    for col in dataframe.columns:
        col_type = get_column_type(dataframe.dtypes[col])
        is_primary = col in primary_keys
        logger.debug(f"Column '{col}': type={col_type}, primary_key={is_primary}")
        columns.append(
            Column(
                col,
                col_type,
                primary_key=is_primary,
            )
        )
    
    logger.info(f"Generated {len(columns)} column definitions")
    return columns


def get_column_type(dtype: str) -> TypeEngine:
    """
    Map Pandas data types to SQLAlchemy data types.

    Args:
        dtype (dtype): The Pandas data type to be mapped.

    Returns:
        sqlalchemy.sql.sqltypes.TypeEngine: The corresponding SQLAlchemy data type.
        For string columns, a default 4000 chars lenght column is created.

    """
    logger.debug(f"Mapping pandas dtype '{dtype}' to SQLAlchemy type")
    
    if dtype in ("int64", "int32", "int"):
        sql_type = Integer()
    elif dtype in ("float64", "float32", "float"):
        sql_type = Float()
    elif dtype == "bool":
        sql_type = Boolean()
    elif dtype == "object":
        sql_type = String(4000)
    elif dtype == "datetime64[ns]":
        sql_type = DateTime()
    else:
        logger.warning(f"Unknown pandas dtype '{dtype}', defaulting to String(4000)")
        sql_type = String(4000)
    
    logger.debug(f"Mapped '{dtype}' to {type(sql_type).__name__}")
    return sql_type
