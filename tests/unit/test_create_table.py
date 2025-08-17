# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the create_table function.
"""

from __future__ import annotations

__all__ = []

import pandas as pd
from sqlalchemy import create_engine, inspect, text, MetaData
from sqlalchemy.engine import Engine

from fbpyutils_db.database.table import create_table


def test_create_table_with_primary_key():
    """
    Tests the create_table function with a primary key.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    create_table(dataframe, engine, "test_table", keys=["id"], index="primary")

    inspector = inspect(engine)
    columns = inspector.get_columns("test_table")
    primary_key = inspector.get_pk_constraint("test_table")

    assert len(columns) == 2
    assert primary_key["constrained_columns"] == ["id"]


def test_create_table_with_unique_index():
    """
    Tests the create_table function with a unique index.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    create_table(dataframe, engine, "test_table", keys=["name"], index="unique")

    inspector = inspect(engine)
    indexes = inspector.get_indexes("test_table")

    assert len(indexes) == 1
    assert indexes[0]["unique"] in [True, 1]
    assert indexes[0]["column_names"] == ["name"]


def test_create_table_with_foreign_key():
    """
    Tests the create_table function with a foreign key.
    """
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()  # Create a single metadata instance
    
    # Create parent table
    parent_df = pd.DataFrame({"id": [1, 2]})
    create_table(parent_df, engine, "parent_table", keys=["id"], index="primary", metadata=metadata)
    
    # Create child table with foreign key reference
    child_df = pd.DataFrame({"id": [1, 2], "parent_id": [1, 2]})
    foreign_keys = [
        {
            "columns": ["parent_id"],
            "refcolumns": ["parent_table.id"],
        }
    ]
    create_table(
        child_df, engine, "child_table", keys=["id"], index="primary", foreign_keys=foreign_keys, metadata=metadata
    )
    
    # Verify tables were created
    inspector = inspect(engine)
    assert "parent_table" in inspector.get_table_names()
    assert "child_table" in inspector.get_table_names()
    
    # Verify foreign key constraint was created
    foreign_keys = inspector.get_foreign_keys("child_table")
    assert len(foreign_keys) == 1
    assert foreign_keys[0]['referred_table'] == 'parent_table'
    assert foreign_keys[0]['referred_columns'] == ['id']

    inspector = inspect(engine)
    foreign_keys = inspector.get_foreign_keys("child_table")

    assert len(foreign_keys) == 1
    assert foreign_keys[0]["referred_table"] == "parent_table"
    assert foreign_keys[0]["referred_columns"] == ["id"]
    assert foreign_keys[0]["constrained_columns"] == ["parent_id"]


def test_create_table_with_check_constraint():
    """
    Tests the create_table function with a check constraint.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2], "value": [10, 20]})
    constraints = [
        {
            "type": "check",
            "sqltext": text("value > 0"),
            "name": "value_gt_0"
        }
    ]
    create_table(
        dataframe, engine, "test_table", keys=["id"], index="primary", constraints=constraints
    )

    # How to inspect check constraints is not straightforward in SQLAlchemy for all backends
    # This test mainly ensures that the table creation does not fail.
    assert inspect(engine).has_table("test_table")
