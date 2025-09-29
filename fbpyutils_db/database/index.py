from sqlalchemy import Index, Selectable
from typing import List

from fbpyutils_db import logger

def create_index(
    name: str, table: Selectable, keys: List[str], unique: bool = False
) -> Index:
    """
    Create an index on the specified keys for a given table.
    
    Args:
        name: The name of the index to be created.
        table: The table on which to create the index.
        keys: Column names that should be part of the index.
        unique: Whether the index should enforce uniqueness. Defaults to False.
    
    Returns:
        The created index object.
    
    Raises:
        ValueError: If no matching columns are found for the keys.
    
    Example:
        from sqlalchemy import Table, Column, Integer, String, MetaData
        from fbpyutils_db.database.index import create_index
        
        metadata = MetaData()
        table = Table('users', metadata, Column('id', Integer), Column('name', String))
        index = create_index('idx_users_name', table, ['name'], unique=False)
        # Returns: Index('idx_users_name', users.c.name)
    """
    logger.debug(f"Creating index '{name}' on columns: {keys}, unique: {unique}")
    
    index_cols = [c for c in table.columns if c.name in keys]
    if not index_cols:
        logger.warning(f"No columns found for index '{name}' with keys: {keys}")
        raise ValueError(f"No matching columns found for keys: {keys}")
    
    index_obj = Index(name, *index_cols, unique=unique)
    logger.debug(f"Index '{name}' created successfully with {len(index_cols)} columns")
    
    return index_obj
