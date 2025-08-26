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
from fbpyutils_db.database.dialects import get_dialect, FirebirdDialect
from unittest.mock import patch
import pytest


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


def test_create_table_with_primary_key_firebird():
    """
    Tests the create_table function with a primary key for FirebirdSQL.
    """
    # Using an in-memory SQLite for testing Firebird dialect logic without a real Firebird DB
    # In a real scenario, you would connect to a Firebird instance.
    # For unit tests, we focus on the SQL generation and basic interaction.
    # Using a dummy Firebird engine to ensure the dialect is correctly identified.
    engine = create_engine("sqlite:///:memory:") # Use SQLite in-memory for actual table creation
    dataframe = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    with patch('fbpyutils_db.database.table.get_dialect', return_value=FirebirdDialect):
        create_table(dataframe, engine, "test_table_fb_pk", keys=["id"], index="primary")

    inspector = inspect(engine)
    columns = inspector.get_columns("test_table_fb_pk")
    primary_key = inspector.get_pk_constraint("test_table_fb_pk")

    assert len(columns) == 2
    assert primary_key["constrained_columns"] == ["id"]


def test_create_table_with_unique_index_firebird():
    """
    Tests the create_table function with a unique index for FirebirdSQL.
    """
    engine = create_engine("sqlite:///:memory:") # Use SQLite in-memory for actual table creation
    dataframe = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    with patch('fbpyutils_db.database.table.get_dialect', return_value=FirebirdDialect):
        create_table(dataframe, engine, "test_table_fb_unique", keys=["name"], index="unique")

    inspector = inspect(engine)
    indexes = inspector.get_indexes("test_table_fb_unique")

    assert len(indexes) == 1
    assert indexes[0]["unique"] in [True, 1]
    assert indexes[0]["column_names"] == ["name"]


def test_create_table_with_foreign_key_firebird():
    """
    Tests the create_table function with a foreign key for FirebirdSQL.
    """
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()

    # Create parent table
    parent_df = pd.DataFrame({"id": [1, 2]})
    with patch('fbpyutils_db.database.table.get_dialect', return_value=FirebirdDialect):
        create_table(parent_df, engine, "parent_table_fb", keys=["id"], index="primary", metadata=metadata)

    # Create child table with foreign key reference
    child_df = pd.DataFrame({"id": [1, 2], "parent_id": [1, 2]})
    foreign_keys = [
        {
            "columns": ["parent_id"],
            "refcolumns": ["parent_table_fb.id"],
            "name": "fk_child_parent_fb"  # Firebird requires explicit name
        }
    ]
    with patch('fbpyutils_db.database.table.get_dialect', return_value=FirebirdDialect):
        create_table(
            child_df, engine, "child_table_fb", keys=["id"], index="primary", foreign_keys=foreign_keys, metadata=metadata
        )

    inspector = inspect(engine) # Initialize inspector here
    # Verify foreign key constraint was created
    foreign_keys = inspector.get_foreign_keys("child_table_fb")
    assert len(foreign_keys) == 1
    assert foreign_keys[0]['referred_table'] == 'parent_table_fb'
    assert foreign_keys[0]['referred_columns'] == ['id']
    assert foreign_keys[0]['constrained_columns'] == ['parent_id']
    assert foreign_keys[0]['name'] == 'fk_child_parent_fb'

    # Verify tables were created
    assert "parent_table_fb" in inspector.get_table_names()
    assert "child_table_fb" in inspector.get_table_names()


def test_create_table_with_check_constraint_firebird():
    """
    Tests the create_table function with a check constraint for FirebirdSQL.
    """
    engine = create_engine("sqlite:///:memory:") # Use SQLite in-memory for actual table creation
    dataframe = pd.DataFrame({"id": [1, 2], "value": [10, 20]})
    constraints = [
        {
            "type": "check",
            "sqltext": text("value > 0"),
            "name": "value_gt_0_fb"  # Firebird might require a name for check constraints too
        }
    ]
    with patch('fbpyutils_db.database.table.get_dialect', return_value=FirebirdDialect):
        create_table(
            dataframe, engine, "test_table_fb_check", keys=["id"], index="primary", constraints=constraints
        )

    assert inspect(engine).has_table("test_table_fb_check")


def test_create_table_with_invalid_dataframe_type():
    """
    Tests create_table with an invalid dataframe type.
    """
    engine = create_engine("sqlite:///:memory:")
    with pytest.raises(ValueError, match="Dataframe must be a Pandas DataFrame."):
        create_table("not_a_dataframe", engine, "test_table")


def test_create_table_with_invalid_keys_type():
    """
    Tests create_table with an invalid keys type.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2]})
    with pytest.raises(ValueError, match="Parameters 'keys' must be a list of str."):
        create_table(dataframe, engine, "test_table", keys="not_a_list")


def test_create_table_with_invalid_index_type():
    """
    Tests create_table with an invalid index type.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2]})
    with pytest.raises(ValueError, match="If an index will be created, it must be any of standard|unique|primary."):
        create_table(dataframe, engine, "test_table", keys=["id"], index="invalid_index")


def test_create_table_with_schema_and_metadata():
    """
    Tests create_table with both schema and metadata provided.
    Ensures the schema parameter is ignored and no error occurs.
    """
    engine = create_engine("sqlite:///:memory:")
    dataframe = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    metadata = MetaData()
    create_table(dataframe, engine, "test_table_schema_meta", schema="my_schema", metadata=metadata)

    inspector = inspect(engine)
    assert "test_table_schema_meta" in inspector.get_table_names()
    # Verify that the table was created without the schema prefix, as schema should be ignored
    # when metadata is provided without a schema in its constructor.
    # This test primarily ensures no error is raised and the table is created.
