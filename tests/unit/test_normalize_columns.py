from fbpyutils_db import normalize_columns


import pytest
from fbpyutils_db import normalize_columns


def test_normalize_columns_valid_input():
    cols = ["Name", "Age", "Address"]
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == ["name", "age", "address"]


def test_normalize_columns_with_special_characters():
    cols = ["Name!", "Age@", "#Address"]
    with pytest.raises(AttributeError):
        normalize_columns(cols)


def test_normalize_columns_with_underscores():
    cols = ["Name_1", "Age_2", "Address_3"]
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == ["name_1", "age_2", "address_3"]


def test_normalize_columns_empty_list():
    cols = []
    normalized_cols = normalize_columns(cols)
    assert normalized_cols == []
