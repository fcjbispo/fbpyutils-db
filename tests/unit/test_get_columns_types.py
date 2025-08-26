# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the get_columns_types function.
"""

from __future__ import annotations

__all__ = []

import pytest
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float
from fbpyutils_db.database.types import get_columns_types


def test_get_columns_types_basic_dataframe():
    """Test get_columns_types with a basic DataFrame."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    
    result = get_columns_types(df)
    
    assert len(result) == 3
    assert all(isinstance(col, Column) for col in result)
    
    # Check column names
    column_names = [col.name for col in result]
    assert "id" in column_names
    assert "name" in column_names
    assert "age" in column_names
    
    # Check column types
    column_types = {col.name: col.type.__class__.__name__ for col in result}
    assert column_types["id"] == "Integer"
    assert column_types["name"] == "String"
    assert column_types["age"] == "Integer"


def test_get_columns_types_with_nan_values():
    """Test get_columns_types with NaN values."""
    df = pd.DataFrame({
        "id": [1, 2, np.nan],
        "name": ["Alice", np.nan, "Charlie"],
        "age": [25, np.nan, 35]
    })
    
    result = get_columns_types(df)
    
    assert len(result) == 3
    assert all(isinstance(col, Column) for col in result)
    
    # Check column names
    column_names = [col.name for col in result]
    assert "id" in column_names
    assert "name" in column_names
    assert "age" in column_names
    
    # Check column types - NaN values should be handled as Float
    column_types = {col.name: col.type.__class__.__name__ for col in result}
    assert column_types["id"] == "Float"  # NaN makes it Float
    assert column_types["name"] == "String"
    assert column_types["age"] == "Float"  # NaN makes it Float


def test_get_columns_types_with_primary_keys():
    """Test get_columns_types with primary keys specified."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    })
    
    result = get_columns_types(df, primary_keys=["id"])
    
    assert len(result) == 3
    
    # Find the primary key column
    primary_key_col = next(col for col in result if col.primary_key)
    assert primary_key_col.name == "id"
    assert primary_key_col.primary_key is True
    
    # Check that other columns are not primary keys
    for col in result:
        if col.name != "id":
            assert col.primary_key is False


def test_get_columns_types_multiple_primary_keys():
    """Test get_columns_types with multiple primary keys."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "code": ["A", "B", "C"],
        "name": ["Alice", "Bob", "Charlie"]
    })
    
    result = get_columns_types(df, primary_keys=["id", "code"])
    
    assert len(result) == 3
    
    # Find primary key columns
    primary_key_cols = [col for col in result if col.primary_key]
    assert len(primary_key_cols) == 2
    assert "id" in [col.name for col in primary_key_cols]
    assert "code" in [col.name for col in primary_key_cols]


def test_get_columns_types_empty_dataframe():
    """Test get_columns_types with an empty DataFrame."""
    df = pd.DataFrame()
    
    result = get_columns_types(df)
    
    assert len(result) == 0


def test_get_columns_types_single_column():
    """Test get_columns_types with a single column DataFrame."""
    df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
    
    result = get_columns_types(df)
    
    assert len(result) == 1
    assert result[0].name == "name"
    assert result[0].type.__class__.__name__ == "String"


def test_get_columns_types_mixed_data_types():
    """Test get_columns_types with mixed data types."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25.5, 30.2, 35.8],
        "active": [True, False, True],
        "created_at": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"])
    })
    
    result = get_columns_types(df)
    
    assert len(result) == 5
    
    column_types = {col.name: col.type.__class__.__name__ for col in result}
    assert column_types["id"] == "Integer"
    assert column_types["name"] == "String"
    assert column_types["age"] == "Float"
    assert column_types["active"] == "Boolean"
    assert column_types["created_at"] == "DateTime"


def test_get_columns_types_with_nan_values():
    """Test get_columns_types with NaN values."""
    df = pd.DataFrame({
        "id": [1, 2, None],
        "name": ["Alice", None, "Charlie"],
        "score": [85.5, None, 92.3]
    })
    
    result = get_columns_types(df)
    
    assert len(result) == 3
    
    column_types = {col.name: col.type.__class__.__name__ for col in result}
    assert column_types["id"] == "Float"  # None values make it Float
    assert column_types["name"] == "String"
    assert column_types["score"] == "Float"


def test_get_columns_types_primary_keys_with_empty_list():
    """Test get_columns_types with empty primary keys list."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"]
    })
    
    result = get_columns_types(df, primary_keys=[])
    
    assert len(result) == 2
    
    # No columns should be primary keys
    for col in result:
        assert col.primary_key is False


def test_get_columns_types_primary_keys_with_nonexistent_column():
    """Test get_columns_types with non-existent primary key column."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"]
    })
    
    # Should handle non-existent column gracefully
    result = get_columns_types(df, primary_keys=["nonexistent"])
    
    assert len(result) == 2
    
    # No columns should be primary keys since "nonexistent" doesn't exist
    for col in result:
        assert col.primary_key is False


def test_get_columns_types_with_object_columns():
    """Test get_columns_types with object columns."""
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "description": ["Short", "A very long description", "Medium"],
        "category": ["A", "B", "C"]
    })
    
    result = get_columns_types(df)
    
    assert len(result) == 3
    
    # Object columns should be mapped to String(4000)
    for col in result:
        if col.name in ["description", "category"]:
            assert col.type.__class__.__name__ == "String"
            assert col.type.length == 4000