"""
PostgreSQL database dialect implementation.

Handles PostgreSQL-specific constraints and upsert queries using ON CONFLICT.
"""
from sqlalchemy.engine import Engine
from typing import Any, Dict

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db import logger
from fbpyutils_db.database.dialects.base import BaseDialect


class PostgreSQLDialect(BaseDialect):
    """
    PostgreSQL-specific dialect for constraints and queries.

    Uses standard constraints with ON CONFLICT for upserts.
    """

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Create a foreign key constraint for PostgreSQL.

        Args:
            **kwargs: Parameters like 'columns', 'refcolumns'.

        Returns:
            ForeignKeyConstraint: SQLAlchemy foreign key object.

        Example:
            >>> fk = dialect.create_foreign_key(columns=['user_id'], refcolumns=['id'], name='fk_users')
            # Creates foreign key from user_id to id.
        """
        return ForeignKeyConstraint(**kwargs)

    def create_constraint(self, **kwargs: Any) -> Any:
        """
        Create check or unique constraint for PostgreSQL.

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


def get_postgresql_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Generate PostgreSQL-specific SQL query, e.g., INSERT ... ON CONFLICT for upsert.

    Args:
        query_name: Query identifier (e.g., 'upsert').
        **kwargs: Formatting params like 'table_name', 'columns', 'keys'.

    Returns:
        str: Formatted PostgreSQL SQL.

    Raises:
        ValueError: For unknown query_name.

    Example:
        >>> query = get_postgresql_dialect_specific_query('upsert', table_name='users', columns='id,name', values=':id,:name', keys='id', updates='name = excluded.name')
        >>> print(query)
        INSERT INTO users (id,name) VALUES (:id,:name) ON CONFLICT (id) DO UPDATE SET name = excluded.name
        # Generates PostgreSQL upsert query with conflict on id.
    """
    logger.debug(f"Getting PostgreSQL dialect specific query for '{query_name}' with kwargs: {kwargs}")
    queries = {
        "upsert": """
            INSERT INTO {table_name} ({columns})
            VALUES ({values})
            ON CONFLICT ({keys}) DO UPDATE SET {updates}
        """,
        # Adicione outras queries específicas do PostgreSQL aqui, se necessário
    }
    query = queries.get(query_name)
    if not query:
        logger.error(f"Unknown PostgreSQL query name: {query_name}")
        raise ValueError(f"Unknown query name: {query_name}")
    logger.debug(f"Returning PostgreSQL query for '{query_name}'")
    return query.format(**kwargs)

def is_postgresql(engine: Engine) -> bool:
    """
    Detect if the engine uses PostgreSQL dialect.

    Args:
        engine: SQLAlchemy engine.

    Returns:
        bool: True if PostgreSQL, else False.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('postgresql://user:pass@localhost/db')
        >>> is_postgresql(engine)
        True
        # Returns True for PostgreSQL connection.
    """
    return engine.name == 'postgresql'
