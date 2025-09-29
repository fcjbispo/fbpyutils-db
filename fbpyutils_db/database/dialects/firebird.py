# -*- coding: utf-8 -*-
"""
Firebird database dialect implementation.

Provides Firebird-specific constraint creation and query handling.
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
    Firebird-specific dialect for constraint and query operations.

    Implements foreign key and constraint creation with Firebird requirements.
    """

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Create a foreign key constraint for Firebird.

        Requires explicit 'name' parameter.

        Args:
            **kwargs: Includes 'columns', 'refcolumns', 'name' (required).

        Returns:
            ForeignKeyConstraint: SQLAlchemy foreign key object.

        Raises:
            ValueError: If 'name' is missing.

        Example:
            >>> fk = dialect.create_foreign_key(columns=['user_id'], refcolumns=['id'], name='fk_users_user')
            # Creates named foreign key from user_id to id.
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
        Create check or unique constraint for Firebird.

        Args:
            **kwargs: Includes 'type' ('check' or 'unique') and params like 'columns', 'sqltext'.

        Returns:
            Constraint: CheckConstraint or UniqueConstraint.

        Raises:
            ValueError: For unsupported type.

        Example:
            >>> check = dialect.create_constraint(type='check', sqltext='age > 0', name='check_age')
            # Creates check constraint enforcing age > 0.
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
    Detect if the engine uses Firebird dialect.

    Checks engine.name and engine.dialect.name for 'firebird'.

    Args:
        engine: SQLAlchemy engine.

    Returns:
        bool: True if Firebird, else False.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine('firebird://user:pass@host/db')
        >>> is_firebird(engine)
        True
        # Returns True for Firebird connection.
    """
    logger.debug(f"Checking if engine is Firebird. engine.name: '{engine.name}', engine.dialect.name: '{engine.dialect.name}'")
    return any(["firebird" in e for e in [engine.dialect.name, engine.name]])


def get_firebird_dialect_specific_query(query_name: str, **kwargs: Any) -> str:
    """
    Generate Firebird-specific SQL query.

    Currently raises NotImplementedError for all queries.

    Args:
        query_name: Query identifier (e.g., 'upsert').
        **kwargs: Formatting parameters.

    Returns:
        str: Firebird SQL query (placeholder).

    Raises:
        NotImplementedError: For any query_name.

    Example:
        >>> get_firebird_dialect_specific_query('upsert', table_name='users')
        Traceback (most recent call last):
         ...
        NotImplementedError: Firebird-specific query 'upsert' is not yet implemented.
        # Raises error as implementation pending.
    """
    raise NotImplementedError(
        f"Firebird-specific query '{query_name}' is not yet implemented."
    )

