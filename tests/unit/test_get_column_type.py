# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the get_column_type function.
"""

from __future__ import annotations

__all__ = []

import pytest
from fbpyutils_db.database.types import get_column_type


def test_get_column_type_int64():
    """Test get_column_type with int64 dtype."""
    result = get_column_type("int64")
    assert result is not None
    assert result.__class__.__name__ == "Integer"


def test_get_column_type_int32():
    """Test get_column_type with int32 dtype."""
    result = get_column_type("int32")
    assert result is not None
    assert result.__class__.__name__ == "Integer"


def test_get_column_type_int():
    """Test get_column_type with int dtype."""
    result = get_column_type("int")
    assert result is not None
    assert result.__class__.__name__ == "Integer"


def test_get_column_type_float64():
    """Test get_column_type with float64 dtype."""
    result = get_column_type("float64")
    assert result is not None
    assert result.__class__.__name__ == "Float"


def test_get_column_type_float32():
    """Test get_column_type with float32 dtype."""
    result = get_column_type("float32")
    assert result is not None
    assert result.__class__.__name__ == "Float"


def test_get_column_type_float():
    """Test get_column_type with float dtype."""
    result = get_column_type("float")
    assert result is not None
    assert result.__class__.__name__ == "Float"


def test_get_column_type_bool():
    """Test get_column_type with bool dtype."""
    result = get_column_type("bool")
    assert result is not None
    assert result.__class__.__name__ == "Boolean"


def test_get_column_type_object():
    """Test get_column_type with object dtype."""
    result = get_column_type("object")
    assert result is not None
    assert result.__class__.__name__ == "String"


def test_get_column_type_edge_case_empty_string():
    """Test get_column_type with empty string dtype."""
    result = get_column_type("")
    assert result is not None
    assert result.__class__.__name__ == "String"
    assert result.length == 4000


def test_get_column_type_edge_case_numeric_string():
    """Test get_column_type with numeric string dtype."""
    result = get_column_type("int64")
    assert result is not None
    assert result.__class__.__name__ == "Integer"
    assert result.length == 4000


def test_get_column_type_datetime64_ns():
    """Test get_column_type with datetime64[ns] dtype."""
    result = get_column_type("datetime64[ns]")
    assert result is not None
    assert result.__class__.__name__ == "DateTime"


def test_get_column_type_unknown_dtype():
    """Test get_column_type with unknown dtype."""
    result = get_column_type("unknown_dtype")
    assert result is not None
    assert result.__class__.__name__ == "String"
    assert result.length == 4000


def test_get_column_type_edge_case_empty_string():
    """Test get_column_type with empty string dtype."""
    result = get_column_type("")
    assert result is not None
    assert result.__class__.__name__ == "String"
    assert result.length == 4000


def test_get_column_type_edge_case_numeric_string():
    """Test get_column_type with numeric string dtype."""
    result = get_column_type("int64")
    assert result is not None
    assert result.__class__.__name__ == "Integer"