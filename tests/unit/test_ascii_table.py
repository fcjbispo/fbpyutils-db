import pytest
from fbpyutils_db import ascii_table


def test_ascii_table_empty_data():
    data = []
    columns = []
    result = ascii_table(data, columns)
    assert result is None


def test_ascii_table_valid_data():
    data = [["John", 25, "USA"], ["Alice", 30, "Canada"]]
    columns = ["Name", "Age", "Country"]
    result = ascii_table(data, columns)
    assert isinstance(result, list)
    assert len(result) == 6


def test_ascii_table_column_mismatch():
    data = [["John", 25], ["Alice", 30, "Canada"]]
    columns = ["Name", "Age", "Country"]
    with pytest.raises(ValueError):
        ascii_table(data, columns)


def test_ascii_table_alignment():
    data = [["John", 25, "USA"], ["Alice", 30, "Canada"]]
    columns = ["Name", "Age", "Country"]
    result = ascii_table(data, columns, alignment="center")
    assert isinstance(result, list)


def test_ascii_table_no_columns():
    data = [["John", 25, "USA"], ["Alice", 30, "Canada"]]
    result = ascii_table(data)
    assert isinstance(result, list)
    assert len(result) == 6
