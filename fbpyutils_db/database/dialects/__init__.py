from sqlalchemy.engine import Engine
from typing import Any, Callable, Dict

from fbpyutils_db import logger # Ensure logger is imported here

from .sqlite import SQLiteDialect, get_sqlite_dialect_specific_query, is_sqlite
from .postgresql import (
    PostgreSQLDialect,
    get_postgresql_dialect_specific_query,
    is_postgresql,
)
from .oracle import OracleDialect, get_oracle_dialect_specific_query, is_oracle
from .firebird import (
    FirebirdDialect,
    get_firebird_dialect_specific_query,
    is_firebird,
)

from fbpyutils_db.database.dialects.base import BaseDialect

def get_dialect_specific_query(engine: Engine, query_name: str, **kwargs: Any) -> str:
    """
    Retrieve a SQL query tailored to the database dialect of the engine.

    Routes to dialect-specific query generators based on engine type.

    Args:
        engine: SQLAlchemy engine to detect dialect from.
        query_name: Name of the query (e.g., 'upsert').
        **kwargs: Parameters for query formatting.

    Returns:
        str: Formatted dialect-specific SQL query.

    Raises:
        ValueError: For unsupported dialect or unknown query_name.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('sqlite:///:memory:')
        >>> query = get_dialect_specific_query(engine, 'upsert', table_name='users', columns='id,name', values=':id,:name')
        >>> print(query)
        INSERT INTO users (id,name) VALUES (:id,:name) ON CONFLICT(id) DO UPDATE SET name = excluded.name
        # Returns SQLite upsert query for 'users' table.
    """
    logger.debug(f"Getting dialect specific query for engine '{engine.name}', query '{query_name}'")
    if is_sqlite(engine):
        return get_sqlite_dialect_specific_query(query_name, **kwargs)
    elif is_postgresql(engine):
        return get_postgresql_dialect_specific_query(query_name, **kwargs)
    elif is_oracle(engine):
        return get_oracle_dialect_specific_query(query_name, **kwargs)
    elif is_firebird(engine):
        return get_firebird_dialect_specific_query(query_name, **kwargs)
    else:
        logger.error(f"Unsupported database dialect: {engine.name}")
        raise ValueError(f"Unsupported database dialect: {engine.name}")

def get_dialect(engine: Engine) -> BaseDialect:
    """
    Return the appropriate dialect class for the engine's database type.

    Supports SQLite, PostgreSQL, Oracle, and Firebird.

    Args:
        engine: SQLAlchemy engine to identify dialect for.

    Returns:
        Type[BaseDialect]: Dialect class for the engine.

    Raises:
        ValueError: For unsupported database dialect.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> dialect_class = get_dialect(engine)
        >>> isinstance(dialect_class, type)
        True
        # Returns PostgreSQLDialect class for PostgreSQL engine.
    """
    logger.debug(f"Getting dialect for engine.name: '{engine.name}', engine.dialect.name: '{engine.dialect.name}'")
    if is_sqlite(engine):
        return SQLiteDialect
    elif is_postgresql(engine):
        return PostgreSQLDialect
    elif is_oracle(engine):
        return OracleDialect
    elif is_firebird(engine):
        return FirebirdDialect
    else:
        logger.debug(f"No specific dialect found. Falling back to error. engine.dialect.name: '{engine.dialect.name}'")
        logger.error(f"Unsupported database dialect: {engine.dialect.name}")
        raise ValueError(f"Unsupported database dialect: {engine.dialect.name}")


def get_dialect_specific_type_handler(engine: Engine) -> Callable[[str], Any]:
    """
    Return a handler function for dialect-specific type conversions.

    Currently a placeholder returning a default handler that logs warnings.

    Args:
        engine: SQLAlchemy engine to base handler on.

    Returns:
        Callable[[str], Any]: Function mapping dtype strings to types.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('sqlite:///:memory:')
        >>> handler = get_dialect_specific_type_handler(engine)
        >>> result = handler('int64')
        'int64'
        # Logs warning and returns original dtype as placeholder.
    """
    logger.debug(f"Getting dialect specific type handler for engine '{engine.name}'")
    # Esta função pode ser expandida para retornar um handler de tipos específico
    # para cada dialeto, se necessário. Por enquanto, retorna uma função dummy.
    def default_type_handler(dtype: str) -> Any:
        logger.warning(
            f"No specific type handler for dialect '{engine.name}'. Defaulting to generic type mapping."
        )
        # Aqui você pode chamar get_column_type do módulo types.py se for genérico
        # ou implementar lógica específica para cada dialeto.
        return dtype  # Retorna o dtype original ou um tipo genérico

    return default_type_handler
