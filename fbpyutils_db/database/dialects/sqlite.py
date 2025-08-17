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
    A class to represent the SQLite database dialect.
    """

    def __init__(self, connection: Any):
        """
        Initializes the SQLiteDialect.

        Args:
            connection: The database connection object.
        """
        super().__init__(connection)
        if os.getenv("FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON", "false").lower() == "true":
            event.listen(self.connection, "connect", self._fk_pragma_on)

    def _fk_pragma_on(self, dbapi_con, con_record):
        """
        Enables foreign key support in SQLite.
        """
        dbapi_con.execute("pragma foreign_keys=ON")

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
