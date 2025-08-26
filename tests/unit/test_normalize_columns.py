import pytest
from fbpyutils_db.data.normalize import normalize_columns


def test_normalize_columns_valid_input():
    cols = ["Name", "Age", "Address"]
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == ["name", "age", "address"]


def test_normalize_columns_raises_value_error_for_empty_normalized_names():
    """Test that normalize_columns raises ValueError for names that become empty after normalization."""
    cols = ["!", "@", "#"]
    with pytest.raises(ValueError, match="Column name '.*' contains only special characters and cannot be normalized."):
        normalize_columns(cols)


def test_normalize_columns_with_underscores():
    cols = ["Name_1", "Age_2", "Address_3"]
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == ["name_1", "age_2", "address_3"]


def test_normalize_columns_empty_list():
    cols = []
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == []
