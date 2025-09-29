"""
Oracle database dialect implementation.

Handles Oracle-specific constraints and upsert queries.
"""
from sqlalchemy.engine import Engine
from typing import Any, Dict

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db import logger
from fbpyutils_db.database.dialects.base import BaseDialect


class OracleDialect(BaseDialect):
    """
    Oracle-specific dialect for constraints and queries.

    Uses standard SQLAlchemy constraints with Oracle MERGE for upserts.
    """

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Create a foreign key constraint for Oracle.

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
        Create check or unique constraint for Oracle.

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


def get_oracle_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Generate Oracle-specific SQL query, e.g., MERGE for upsert.

    Args:
        query_name: Query identifier (e.g., 'upsert').
        **kwargs: Formatting params like 'table_name', 'columns'.

    Returns:
        str: Formatted Oracle SQL.

    Raises:
        ValueError: For unknown query_name.

    Example:
        >>> query = get_oracle_dialect_specific_query('upsert', table_name='users', columns='id,name', values=':id,:name', on_conditions='target.id = source.id', updates='name = source.name')
        >>> print(query)
        MERGE INTO users target USING (SELECT :id,:name FROM DUAL) source ON (target.id = source.id) WHEN MATCHED THEN UPDATE SET name = source.name WHEN NOT MATCHED THEN INSERT (id,name) VALUES (:id,:name)
        # Generates Oracle MERGE upsert query.
    """
    logger.debug(f"Getting Oracle dialect specific query for '{query_name}' with kwargs: {kwargs}")
    queries = {
        "upsert": """
            MERGE INTO {table_name} target
            USING (SELECT {values_select} FROM DUAL) source
            ON ({on_conditions})
            WHEN MATCHED THEN UPDATE SET {updates}
            WHEN NOT MATCHED THEN INSERT ({columns}) VALUES ({values})
        """,
        # Adicione outras queries específicas do Oracle aqui, se necessário
    }
    query = queries.get(query_name)
    if not query:
        logger.error(f"Unknown Oracle query name: {query_name}")
        raise ValueError(f"Unknown query name: {query_name}")
    logger.debug(f"Returning Oracle query for '{query_name}'")
    return query.format(**kwargs)

def is_oracle(engine: Engine) -> bool:
    """
    Detect if the engine uses Oracle dialect.

    Args:
        engine: SQLAlchemy engine.

    Returns:
        bool: True if Oracle, else False.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('oracle://user:pass@host/db')
        >>> is_oracle(engine)
        True
        # Returns True for Oracle connection.
    """
    return engine.name == 'oracle'
