from sqlalchemy.engine import Engine
from typing import Any, Dict

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db import logger
from fbpyutils_db.database.dialects.base import BaseDialect


class OracleDialect(BaseDialect):
    """
    A class to represent the Oracle database dialect.
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


def get_oracle_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Returns Oracle-specific SQL queries based on the query name.

    Args:
        query_name (str): The name of the query to retrieve.
        **kwargs: Arbitrary keyword arguments for query formatting.

    Returns:
        str: The Oracle-specific SQL query.

    Raises:
        ValueError: If an unknown query name is provided.
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
    Checks if the given SQLAlchemy engine is for Oracle.
    """
    return engine.name == 'oracle'
