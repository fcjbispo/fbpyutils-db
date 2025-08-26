import pandas as pd
import pytest
from fbpyutils_db.data.extract import get_data_from_pandas


def test_get_data_from_pandas_valid_dataframe():
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    data, columns = get_data_from_pandas(df)
    assert data == [[1, "a"], [2, "b"]]
    assert columns == ["col1", "col2"]


def test_get_data_from_pandas_include_index():
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    data, columns = get_data_from_pandas(df, include_index=True)
    assert data == [[0, 1, "a"], [1, 2, "b"]]
    assert columns == ["Index", "col1", "col2"]


def test_get_data_from_pandas_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(IndexError):
        get_data_from_pandas(df)


def test_get_data_from_pandas_invalid_input():
    with pytest.raises(TypeError):
        get_data_from_pandas("not a dataframe")
