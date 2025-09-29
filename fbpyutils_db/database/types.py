import pandas as pd
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql.sqltypes import TypeEngine
from typing import List

from fbpyutils_db import logger

def get_columns_types(
    dataframe: pd.DataFrame, primary_keys: List[str] = []
) -> List[Column]:
    """
    Generate SQLAlchemy Column objects from a DataFrame's columns, marking primary keys.

    Infers SQLAlchemy types based on Pandas dtypes and applies primary key constraints.

    Args:
        dataframe: Input DataFrame to derive column definitions from.
        primary_keys: List of column names to set as primary keys. Defaults to empty list.

    Returns:
        List[Column]: List of SQLAlchemy Column objects for table creation.

    Example:
        >>> import pandas as pd
        >>> from sqlalchemy import Column
        >>> df = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
        >>> columns = get_columns_types(df, primary_keys=['id'])
        >>> isinstance(columns[0], Column) and columns[0].primary_key
        True
        # Creates columns with 'id' as primary key (Integer) and 'name' as String.
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
    Convert Pandas dtype to corresponding SQLAlchemy TypeEngine.

    Maps common Pandas types to SQLAlchemy equivalents. Defaults to String(4000) for unknowns.

    Args:
        dtype: Pandas dtype string (e.g., 'int64', 'object').

    Returns:
        TypeEngine: SQLAlchemy type instance.

    Example:
        >>> from sqlalchemy.sql.sqltypes import Integer, String
        >>> get_column_type('int64')
        Integer()
        >>> get_column_type('object')
        String(4000)
        # Maps integer to Integer() and string/object to String(4000).
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
