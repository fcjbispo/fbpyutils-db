import pandas as pd
import pytest
from fbpyutils_db import add_hash_index


def test_add_hash_index_valid_input():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    index_name = "hash_index"
    result_df = add_hash_index(df, index_name)
    assert result_df.index.name == index_name
    assert len(result_df.index[0]) == 12


def test_add_hash_index_different_length():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    index_name = "hash_index"
    length = 8
    result_df = add_hash_index(df, index_name, length=length)
    assert len(result_df.index[0]) == length


def test_add_hash_index_specific_columns():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"], "col3": [4, 5, 6]})
    index_name = "hash_index"
    columns = ["col1", "col2"]
    result_df = add_hash_index(df, index_name, columns=columns)
    assert result_df.index.name == index_name


def test_add_hash_index_type_error():
    df = "not a dataframe"
    index_name = "hash_index"
    with pytest.raises(TypeError):
        add_hash_index(df, index_name)


def test_add_hash_index_value_error_length():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    index_name = "hash_index"
    length = 0
    with pytest.raises(ValueError):
        add_hash_index(df, index_name, length=length)


def test_add_hash_index_value_error_columns_not_list():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    index_name = "hash_index"
    columns = "not a list"
    with pytest.raises(ValueError):
        add_hash_index(df, index_name, columns=columns)


def test_add_hash_index_value_error_column_not_exists():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    index_name = "hash_index"
    columns = ["col1", "col4"]
    with pytest.raises(ValueError):
        add_hash_index(df, index_name, columns=columns)
