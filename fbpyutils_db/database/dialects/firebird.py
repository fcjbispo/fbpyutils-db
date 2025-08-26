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
from fbpyutils_db import logger


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
    Checks if the given SQLAlchemy engine is a Firebird engine.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.

    Returns:
        bool: True if the engine is Firebird, False otherwise.
    """
    logger.debug(f"Checking if engine is Firebird. engine.name: '{engine.name}', engine.dialect.name: '{engine.dialect.name}'")
    return any(["firebird" in e for e in [engine.dialect.name, engine.name]])


def get_firebird_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Returns a Firebird-specific SQL query based on the query name.
    This is a placeholder and will raise NotImplementedError for now.
    """
    raise NotImplementedError(
        f"Firebird-specific query '{query_name}' is not yet implemented."
    )

