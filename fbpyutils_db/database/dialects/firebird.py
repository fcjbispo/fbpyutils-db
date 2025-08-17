# -*- coding: utf-8 -*-
"""
This module provides a specific implementation for the Firebird database dialect.
It includes methods for creating tables, indexes, and other database objects,
as well as handling data types and other Firebird-specific features.
"""

from __future__ import annotations

__all__ = ['FirebirdDialect', 'is_firebird', 'get_firebird_dialect_specific_query']

from typing import Any
from sqlalchemy.engine import Engine

from sqlalchemy import ForeignKeyConstraint, CheckConstraint, UniqueConstraint
from fbpyutils_db.database.dialects.base import BaseDialect


class FirebirdDialect(BaseDialect):
    """
    A class to represent the Firebird database dialect.

    This class provides the specific implementation for creating tables,
    indexes, and other database objects in Firebird. It also handles
    data types and other Firebird-specific features.
    """

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Creates a foreign key constraint for FirebirdSQL.
        
        Args:
            **kwargs: Arbitrary keyword arguments for foreign key creation.
                Must include 'columns' (list of column names),
                'refcolumns' (list of referenced column names),
                and optionally 'name' (constraint name).
        
        Returns:
            Any: The foreign key constraint object.
        """
        # Firebird requires explicit name for foreign key constraints
        if 'name' not in kwargs:
            raise ValueError("Firebird foreign key constraint requires a name")
        
        # Extract parameters from kwargs
        columns = kwargs.pop('columns', [])
        refcolumns = kwargs.pop('refcolumns', [])
        
        # Create the foreign key constraint
        return ForeignKeyConstraint(columns, refcolumns, **kwargs)

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


def is_firebird(engine: Engine) -> bool:
    """
    Checks if the provided SQLAlchemy engine is for Firebird.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.

    Returns:
        bool: True if the engine is for Firebird, False otherwise.
    """
    return engine.name == "firebird"


def get_firebird_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Returns a Firebird-specific SQL query.

    Args:
        query_name (str): The name of the query to retrieve.
        **kwargs: Arbitrary keyword arguments for query formatting.

    Returns:
        str: The Firebird-specific SQL query.

    Raises:
        ValueError: If the query name is unknown.
    """
    queries = {
        "upsert": """
            MERGE INTO {table_name} target
            USING (SELECT {values_select} FROM DUAL) source
            ON ({on_conditions})
            WHEN MATCHED THEN UPDATE SET {updates}
            WHEN NOT MATCHED THEN INSERT ({columns}) VALUES ({values})
        """,
        "create_table": """
            CREATE TABLE {table_name} (
                {columns}
            )
        """,
        "create_index": """
            CREATE {unique} INDEX {index_name}
            ON {table_name} ({columns})
        """
    }
    if query_name in queries:
        return queries[query_name].format(**kwargs)
    raise ValueError(f"Unknown query for Firebird dialect: {query_name}")
