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
    Create a database table from a DataFrame schema, optionally with indexes, foreign keys, and constraints.

    Infers column types from the DataFrame and creates the table structure. Supports primary keys,
    standard/unique indexes, and dialect-specific constraints.

    Args:
        dataframe: Pandas DataFrame defining the table schema.
        engine: SQLAlchemy database engine.
        table_name: Name of the table to create.
        schema: Optional schema name.
        keys: List of primary key column names.
        index: Index type on keys ('standard', 'unique', or 'primary'). Defaults to None.
        foreign_keys: List of foreign key definitions as dicts.
        constraints: List of constraint definitions as dicts.
        metadata: Optional SQLAlchemy MetaData object.

    Returns:
        None

    Raises:
        ValueError: For invalid DataFrame, keys, or index type.

    Example:
        >>> import pandas as pd
        >>> from sqlalchemy import create_engine
        >>> df = pd.DataFrame({'id': [1], 'name': ['Test']})
        >>> engine = create_engine('sqlite:///:memory:')
        >>> create_table(df, engine, 'test_table', keys=['id'], index='primary')
        # Creates 'test_table' with 'id' as primary key.
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
