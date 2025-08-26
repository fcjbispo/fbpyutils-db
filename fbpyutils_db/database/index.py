from sqlalchemy import Index, Selectable
from typing import List

from fbpyutils_db import logger

def create_index(
    name: str, table: Selectable, keys: List[str], unique: bool = False
) -> Index:
    """Create an index on the specified keys for a given table.
    
    Args:
        name (str): The name of the index to be created.
        table (sqlalchemy.sql.expression.Selectable): The table on which to create the index.
        keys (list of str): Column names that should be part of the index.
        unique (bool, optional): Whether the index should enforce uniqueness. Default is False.
    
    Returns:
        sqlalchemy.Index: The created index object.
    """
    """Create an index on the specified keys for a given table.

    Args:
        name (str): The name of the index to be created.
        table (sqlalchemy.sql.expression.Selectable): The table on which to create the index.
        keys (list of str): A list of column names that should be part of the index.
        unique (bool, optional): Whether the index should enforce uniqueness. Default is False.
    """
    logger.debug(f"Creating index '{name}' on columns: {keys}, unique: {unique}")
    
    index_cols = [c for c in table.columns if c.name in keys]
    if not index_cols:
        logger.warning(f"No columns found for index '{name}' with keys: {keys}")
        raise ValueError(f"No matching columns found for keys: {keys}")
    
    index_obj = Index(name, *index_cols, unique=unique)
    logger.debug(f"Index '{name}' created successfully with {len(index_cols)} columns")
    
    return index_obj
