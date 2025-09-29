"""
SQLite database dialect implementation.

Handles SQLite-specific constraints, foreign key enabling, and upsert queries using ON CONFLICT.
"""
from sqlalchemy.engine import Engine
from typing import Any, Dict

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db import logger
from fbpyutils_db.database.dialects.base import BaseDialect


import os
from sqlalchemy import event
from sqlalchemy.engine import Engine

class SQLiteDialect(BaseDialect):
    """
    SQLite-specific dialect for constraints and queries.

    Optionally enables foreign keys via environment variable.
    """

    def __init__(self, connection: Any):
        """
        Initialize SQLite dialect, enabling foreign keys if configured.

        Args:
            connection: Database connection object.

        Example:
            >>> os.environ['FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON'] = 'true'
            >>> with engine.connect() as conn:
            ...     dialect = SQLiteDialect(conn)
            # Enables PRAGMA foreign_keys=ON for the connection.
        """
        super().__init__(connection)
        if os.getenv("FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON", "false").lower() == "true":
            event.listen(self.connection, "connect", self._fk_pragma_on)

    def _fk_pragma_on(self, dbapi_con, con_record):
        """
        Enable foreign key enforcement in SQLite connection.

        Executes PRAGMA foreign_keys=ON.

        Args:
            dbapi_con: SQLite DB-API connection.
            con_record: SQLAlchemy connection record.

        Example:
            >>> # Called internally on connect event
            # dbapi_con.execute("pragma foreign_keys=ON")
            # Enables FK checks for the session.
        """
        dbapi_con.execute("pragma foreign_keys=ON")

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Create a foreign key constraint for SQLite.

        Args:
            **kwargs: Parameters like 'columns', 'refcolumns'.

        Returns:
            ForeignKeyConstraint: SQLAlchemy foreign key object.

        Example:
            >>> fk = dialect.create_foreign_key(columns=['user_id'], refcolumns=['id'], name='fk_users')
            # Creates foreign key from user_id to id (enforced if FK enabled).
        """
        return ForeignKeyConstraint(**kwargs)

    def create_constraint(self, **kwargs: Any) -> Any:
        """
        Create check or unique constraint for SQLite.

        Args:
            **kwargs: Includes 'type' ('check' or 'unique') and params.

        Returns:
            Constraint: CheckConstraint or UniqueConstraint.

        Raises:
            ValueError: For unsupported type.

        Example:
            >>> check = dialect.create_constraint(type='check', sqltext='age > 0', name='check_age')
            # Creates check constraint for age > 0.
        """
        constraint_type = kwargs.pop("type", None)
        if constraint_type == "check":
            return CheckConstraint(**kwargs)
        elif constraint_type == "unique":
            return UniqueConstraint(**kwargs)
        else:
            raise ValueError(f"Unsupported constraint type: {constraint_type}")


def get_sqlite_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Generate SQLite-specific SQL query, e.g., INSERT ... ON CONFLICT for upsert.

    Args:
        query_name: Query identifier (e.g., 'upsert').
        **kwargs: Formatting params like 'table_name', 'columns', 'keys'.

    Returns:
        str: Formatted SQLite SQL.

    Raises:
        ValueError: For unknown query_name.

    Example:
        >>> query = get_sqlite_dialect_specific_query('upsert', table_name='users', columns='id,name', values='?,?', keys='id', updates='name = excluded.name')
        >>> print(query)
        INSERT INTO users (id,name) VALUES (?,?,) ON CONFLICT(id) DO UPDATE SET name = excluded.name
        # Generates SQLite upsert query with conflict on id (note: uses ? placeholders).
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
    Detect if the engine uses SQLite dialect.

    Args:
        engine: SQLAlchemy engine.

    Returns:
        bool: True if SQLite, else False.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('sqlite:///:memory:')
        >>> is_sqlite(engine)
        True
        # Returns True for in-memory SQLite.
    """
    return engine.name == 'sqlite'
