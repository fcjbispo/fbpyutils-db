# -*- coding: utf-8 -*-
"""
This module provides the base class for database dialects.
"""

from __future__ import annotations

__all__ = ['BaseDialect']

from typing import Any


class BaseDialect:
    """
    A base class for database dialects.
    """

    def __init__(self, connection: Any):
        """
        Initializes the BaseDialect.

        Args:
            connection: The database connection object.
        """
        self.connection = connection

    def create_foreign_key(self, **kwargs: Any) -> Any:
        """
        Creates a foreign key constraint.

        Args:
            **kwargs: Arbitrary keyword arguments for foreign key creation.

        Returns:
            Any: The foreign key constraint object.
        """
        raise NotImplementedError

    def create_constraint(self, **kwargs: Any) -> Any:
        """
        Creates a constraint.

        Args:
            **kwargs: Arbitrary keyword arguments for constraint creation.

        Returns:
            Any: The constraint object.
        """
        raise NotImplementedError
