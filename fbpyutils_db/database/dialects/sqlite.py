from sqlalchemy.engine import Engine
from typing import Any, Dict

from fbpyutils_db import logger

def get_sqlite_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Returns SQLite-specific SQL queries based on the query name.

    Args:
        query_name (str): The name of the query to retrieve.
        **kwargs: Arbitrary keyword arguments for query formatting.

    Returns:
        str: The SQLite-specific SQL query.

    Raises:
        ValueError: If an unknown query name is provided.
    """
    logger.debug(f"Getting SQLite dialect specific query for '{query_name}' with kwargs: {kwargs}")
    queries = {
        "upsert": """
            INSERT INTO {table_name} ({columns})
            VALUES ({values})
            ON CONFLICT({keys}) DO UPDATE SET {updates}
        """,
        # Adicione outras queries específicas do SQLite aqui, se necessário
    }
    query = queries.get(query_name)
    if not query:
        logger.error(f"Unknown SQLite query name: {query_name}")
        raise ValueError(f"Unknown query name: {query_name}")
    logger.debug(f"Returning SQLite query for '{query_name}'")
    return query.format(**kwargs)

def is_sqlite(engine: Engine) -> bool:
    """
    Checks if the given SQLAlchemy engine is for SQLite.
    """
    return engine.name == 'sqlite'
