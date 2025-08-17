from sqlalchemy.engine import Engine
from typing import Any, Dict

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db import logger
from fbpyutils_db.database.dialects.base import BaseDialect


class PostgreSQLDialect(BaseDialect):
    """
    A class to represent the PostgreSQL database dialect.
    """

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Creates a foreign key constraint.
        """
        return ForeignKeyConstraint(**kwargs)

    def create_constraint(self, **kwargs: Any) -> Any:
        """
        Creates a constraint.
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
    Returns PostgreSQL-specific SQL queries based on the query name.

    Args:
        query_name (str): The name of the query to retrieve.
        **kwargs: Arbitrary keyword arguments for query formatting.

    Returns:
        str: The PostgreSQL-specific SQL query.

    Raises:
        ValueError: If an unknown query name is provided.
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
    Checks if the given SQLAlchemy engine is for PostgreSQL.
    """
    return engine.name == 'postgresql'
