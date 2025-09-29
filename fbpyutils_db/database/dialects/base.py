# -*- coding: utf-8 -*-
"""
Base class for database dialect implementations.

Defines abstract methods for creating foreign keys and constraints.
"""

from __future__ import annotations

__all__ = ['BaseDialect']

from typing import Any


class BaseDialect:
    """
    Abstract base class for database-specific dialect implementations.

    Subclasses must implement create_foreign_key and create_constraint.
    """

    def __init__(self, connection: Any):
        """
        Initialize the dialect with a database connection.

        Args:
            connection: Database connection object.

        Example:
            >>> from sqlalchemy import create_engine
            >>> engine = create_engine('sqlite:///:memory:')
            >>> with engine.connect() as conn:
            ...     dialect = BaseDialect(conn)
            # Initializes dialect with connection (subclass required for full use).
        """
        self.connection = connection

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Create a foreign key constraint (abstract method).

        Subclasses implement dialect-specific logic.

        Args:
            **kwargs: Parameters like 'columns', 'refcolumns', 'name'.

        Returns:
            ForeignKeyConstraint: SQLAlchemy foreign key object.

        Raises:
            NotImplementedError: In base class.

        Example:
            >>> # In subclass like SQLiteDialect
            >>> fk = dialect.create_foreign_key(columns=['user_id'], refcolumns=['id'], name='fk_users')
            # Returns ForeignKeyConstraint for user_id referencing id.
        """
        raise NotImplementedError

    def create_constraint(self, **kwargs: Any) -> Any:
        """
        Create a constraint (abstract method).

        Supports check or unique types in subclasses.

        Args:
            **kwargs: Includes 'type' ('check' or 'unique') and other params.

        Returns:
            Constraint: SQLAlchemy constraint object (CheckConstraint or UniqueConstraint).

        Raises:
            NotImplementedError: In base class.
            ValueError: For unsupported types in subclasses.

        Example:
            >>> # In subclass
            >>> check = dialect.create_constraint(type='check', sqltext='age > 0', name='check_age')
            # Returns CheckConstraint enforcing age > 0.
        """
        raise NotImplementedError
