import pandas as pd
from sqlalchemy import Engine, MetaData, Table, Column
from typing import List

from fbpyutils_db import logger

# Importa funções de outros módulos
from fbpyutils_db.database.dialects import get_dialect
from fbpyutils_db.database.index import create_index
from fbpyutils_db.database.types import get_columns_types

def create_table(
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = None,
    keys: List[str] = [],
    index: str = None,
    foreign_keys: List[dict] = [],
    constraints: List[dict] = [],
    metadata: MetaData = None,
) -> None:
    """
    Create a table in the database using the provided pandas DataFrame as a schema.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame containing the schema information.
        table_name (str): The name of the table to be created.
        schema (str, optional): The name of the schema to be created. Default is None.
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine engine.
        keys (list of str, optional): List of column names to use as keys for index creation. Default is None.
        index (str, optional): Whether to create an index and what kind using the keys. Default is None (not create index).
            If an index muste be created, index be in 'standard' or 'unique'.
        foreign_keys (list of dict, optional): List of foreign keys to be created. Default is None.
        constraints (list of dict, optional): List of constraints to be created. Default is None.
        metadata (MetaData, optional): SQLAlchemy MetaData object to use. If None, a new one will be created.

    """
    logger.info(f"Creating table '{table_name}' in schema '{schema}'")

    dialect = get_dialect(engine)(engine)
    
    # Check parameters
    if not type(dataframe) == pd.DataFrame:
        logger.error("Invalid dataframe type provided")
        raise ValueError("Dataframe must be a Pandas DataFrame.")

    if keys and not type(keys) == list:
        logger.error("Invalid keys type provided")
        raise ValueError("Parameters 'keys' must be a list of str.")

    if keys and index and index not in ("standard", "unique", "primary"):
        logger.error(f"Invalid index type: {index}")
        raise ValueError(
            "If an index will be created, it must be any of standard|unique|primary."
        )

    logger.debug(f"Creating table with keys: {keys}, index type: {index}")
    
    # Use provided metadata or create a new one
    if metadata is None:
        metadata = MetaData(schema)
    elif schema is not None:
        logger.warning("Schema parameter ignored when metadata is provided")

    if keys and index == "primary":
        columns = get_columns_types(dataframe, primary_keys=keys)
    else:
        columns = get_columns_types(dataframe, primary_keys=[])

    table = Table(table_name, metadata, *columns)

    # Create the index if required
    if keys and index in ("standard", "unique"):
        unique = index == "unique"
        idx_suffix = "uk" if unique else "ik"
        index_name = f"{table_name}_i001_{idx_suffix}"
        logger.debug(f"Creating {index} index '{index_name}' on columns: {keys}")
        table.indexes.add(
            create_index(index_name, table, keys, unique)
        )

    # Add foreign keys
    if foreign_keys:
        for fk in foreign_keys:
            table.append_constraint(dialect.create_foreign_key(**fk))

    # Add constraints
    if constraints:
        for constraint in constraints:
            table.append_constraint(dialect.create_constraint(**constraint))

    logger.info(f"Creating table structure in database")
    result = metadata.create_all(engine)
    logger.info(f"Table '{table_name}' created successfully")
    return result
