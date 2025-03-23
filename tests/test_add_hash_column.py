import pandas as pd
import pytest
from fbpyutils_db import add_hash_column


def test_add_hash_column_valid_input():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    column_name = "hash_col"
    result_df = add_hash_column(df, column_name)
    assert column_name in result_df.columns
    assert len(result_df[column_name][0]) == 12


def test_add_hash_column_different_length():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    column_name = "hash_col"
    length = 8
    result_df = add_hash_column(df, column_name, length=length)
    assert len(result_df[column_name][0]) == length


def test_add_hash_column_specific_columns():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"], "col3": [4, 5, 6]})
    column_name = "hash_col"
    columns = ["col1", "col2"]
    result_df = add_hash_column(df, column_name, columns=columns)
    assert column_name in result_df.columns


def test_add_hash_column_type_error():
    df = "not a dataframe"
    column_name = "hash_col"
    with pytest.raises(TypeError):
        add_hash_column(df, column_name)


def test_add_hash_column_value_error_length():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    column_name = "hash_col"
    length = 0
    with pytest.raises(ValueError):
        add_hash_column(df, column_name, length=length)


def test_add_hash_column_value_error_columns_not_list():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    column_name = "hash_col"
    columns = "not a list"
    with pytest.raises(ValueError):
        add_hash_column(df, column_name, columns=columns)


def test_add_hash_column_value_error_column_not_exists():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    column_name = "hash_col"
    columns = ["col1", "col4"]
    with pytest.raises(ValueError):
        add_hash_column(df, column_name, columns=columns)
