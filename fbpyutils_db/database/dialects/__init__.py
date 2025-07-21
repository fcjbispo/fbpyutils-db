from sqlalchemy.engine import Engine
from typing import Any, Callable, Dict

from .sqlite import get_sqlite_dialect_specific_query, is_sqlite
from .postgresql import get_postgresql_dialect_specific_query, is_postgresql
from .oracle import get_oracle_dialect_specific_query, is_oracle

from fbpyutils_db import logger

def get_dialect_specific_query(engine: Engine, query_name: str, **kwargs: Any) -> str:
    """
    Returns a dialect-specific SQL query based on the provided SQLAlchemy engine.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.
        query_name (str): The name of the query to retrieve (e.g., "upsert").
        **kwargs: Arbitrary keyword arguments for query formatting.

    Returns:
        str: The dialect-specific SQL query.

    Raises:
        ValueError: If the dialect is not supported or the query name is unknown.
    """
    logger.debug(f"Getting dialect specific query for engine '{engine.name}', query '{query_name}'")
    if is_sqlite(engine):
        return get_sqlite_dialect_specific_query(query_name, **kwargs)
    elif is_postgresql(engine):
        return get_postgresql_dialect_specific_query(query_name, **kwargs)
    elif is_oracle(engine):
        return get_oracle_dialect_specific_query(query_name, **kwargs)
    else:
        logger.error(f"Unsupported database dialect: {engine.name}")
        raise ValueError(f"Unsupported database dialect: {engine.name}")

def get_dialect_specific_type_handler(engine: Engine) -> Callable[[str], Any]:
    """
    Returns a function to handle dialect-specific type conversions.
    (Placeholder for future implementation)
    """
    logger.debug(f"Getting dialect specific type handler for engine '{engine.name}'")
    # Esta função pode ser expandida para retornar um handler de tipos específico
    # para cada dialeto, se necessário. Por enquanto, retorna uma função dummy.
    def default_type_handler(dtype: str) -> Any:
        logger.warning(f"No specific type handler for dialect '{engine.name}'. Defaulting to generic type mapping.")
        # Aqui você pode chamar get_column_type do módulo types.py se for genérico
        # ou implementar lógica específica para cada dialeto.
        return dtype # Retorna o dtype original ou um tipo genérico
    return default_type_handler
