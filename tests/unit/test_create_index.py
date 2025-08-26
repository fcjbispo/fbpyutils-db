# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the create_index function.
"""

from __future__ import annotations

__all__ = []

import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String
from fbpyutils_db.database.index import create_index


@pytest.fixture
def sample_metadata():
    """Create sample metadata for testing."""
    return MetaData()


@pytest.fixture
def sample_table(sample_metadata):
    """Create a sample table for testing."""
    return Table(
        "test_table",
        sample_metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("email", String(100)),
        Column("age", Integer)
    )


def test_create_index_basic(sample_table):
    """Test create_index with basic parameters."""
    result = create_index("test_index", sample_table, ["id"])
    
    assert result is not None
    assert result.name == "test_index"
    assert len(result.columns) == 1
    assert result.columns[0].name == "id"
    assert result.unique is False  # Default is False


def test_create_index_unique(sample_table):
    """Test create_index with unique=True."""
    result = create_index("unique_index", sample_table, ["email"], unique=True)
    
    assert result is not None
    assert result.name == "unique_index"
    assert len(result.columns) == 1
    assert result.columns[0].name == "email"
    assert result.unique is True


def test_create_index_multiple_columns(sample_table):
    """Test create_index with multiple columns."""
    result = create_index("composite_index", sample_table, ["name", "age"])
    
    assert result is not None
    assert result.name == "composite_index"
    assert len(result.columns) == 2
    column_names = [col.name for col in result.columns]
    assert "name" in column_names
    assert "age" in column_names
    assert result.unique is False


def test_create_index_unique_multiple_columns(sample_table):
    """Test create_index with unique=True and multiple columns."""
    result = create_index("unique_composite_index", sample_table, ["name", "email"], unique=True)
    
    assert result is not None
    assert result.name == "unique_composite_index"
    assert len(result.columns) == 2
    column_names = [col.name for col in result.columns]
    assert "name" in column_names
    assert "email" in column_names
    assert result.unique is True


def test_create_index_nonexistent_column(sample_table):
    """Test create_index with non-existent column."""
    with pytest.raises(ValueError, match="No matching columns found for keys"):
        create_index("invalid_index", sample_table, ["nonexistent_column"])


def test_create_index_empty_keys(sample_table):
    """Test create_index with empty keys list."""
    with pytest.raises(ValueError, match="No matching columns found for keys"):
        create_index("empty_index", sample_table, [])


def test_create_index_nonexistent_columns(sample_table):
    """Test create_index with all non-existent columns."""
    with pytest.raises(ValueError, match="No matching columns found for keys"):
        create_index("invalid_index", sample_table, ["nonexistent1", "nonexistent2"])


def test_create_index_partial_nonexistent_columns(sample_table):
    """Test create_index with some non-existent columns."""
    # Should work with existing columns and ignore non-existent ones
    result = create_index("partial_index", sample_table, ["name", "nonexistent"])
    
    assert result is not None
    assert result.name == "partial_index"
    assert len(result.columns) == 1
    assert result.columns[0].name == "name"
    assert result.unique is False


def test_create_index_same_column_multiple_times(sample_table):
    """Test create_index with same column specified multiple times."""
    # Should handle duplicate column names gracefully
    result = create_index("duplicate_index", sample_table, ["id", "id"])
    
    assert result is not None
    assert result.name == "duplicate_index"
    # Should only have one column (duplicates should be removed)
    assert len(result.columns) == 1
    assert result.columns[0].name == "id"
    assert result.unique is False


def test_create_index_long_name(sample_table):
    """Test create_index with a very long name."""
    long_name = "very_long_index_name_that_exceeds_normal_limits_but_should_still_work"
    result = create_index(long_name, sample_table, ["id"])
    
    assert result is not None
    assert result.name == long_name
    assert len(result.columns) == 1
    assert result.columns[0].name == "id"
    assert result.unique is False


def test_create_index_special_characters_in_name(sample_table):
    """Test create_index with special characters in name."""
    special_name = "index_with_special_chars_123"
    result = create_index(special_name, sample_table, ["id"])
    
    assert result is not None
    assert result.name == special_name
    assert len(result.columns) == 1
    assert result.columns[0].name == "id"
    assert result.unique is False


def test_create_index_all_columns(sample_table):
    """Test create_index with all table columns."""
    result = create_index("all_columns_index", sample_table, ["id", "name", "email", "age"])
    
    assert result is not None
    assert result.name == "all_columns_index"
    assert len(result.columns) == 4
    column_names = [col.name for col in result.columns]
    assert "id" in column_names
    assert "name" in column_names
    assert "email" in column_names
    assert "age" in column_names
    assert result.unique is False


def test_create_index_primary_key_column(sample_table):
    """Test create_index with primary key column."""
    result = create_index("primary_key_index", sample_table, ["id"])
    
    assert result is not None
    assert result.name == "primary_key_index"
    assert len(result.columns) == 1
    assert result.columns[0].name == "id"
    assert result.unique is False


def test_create_index_non_unique_default(sample_table):
    """Test that default unique parameter is False."""
    result = create_index("default_index", sample_table, ["name"])
    
    assert result is not None
    assert result.unique is False


def test_create_index_explicit_non_unique(sample_table):
    """Test create_index with explicit unique=False."""
    result = create_index("non_unique_index", sample_table, ["name"], unique=False)
    
    assert result is not None
    assert result.unique is False