import pandas as pd
import pytest
from fbpyutils_db import isolate


def test_isolate_empty_dataframe():
    df = pd.DataFrame()
    group_columns = ["Group"]
    unique_columns = ["Value", "Unique"]
    with pytest.raises(KeyError):
        isolate(df, group_columns, unique_columns)


def test_isolate_single_group():
    df = pd.DataFrame({"Group": ["A", "A"], "Value": [1, 2], "Unique": [5, 6]})
    group_columns = ["Group"]
    unique_columns = ["Value", "Unique"]
    result = isolate(df, group_columns, unique_columns)
    expected = pd.DataFrame({"Group": ["A"], "Value": [2], "Unique": [6]}, index=[1])
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected.reset_index(drop=True)
    )


def test_isolate_multiple_groups():
    df = pd.DataFrame(
        {"Group": ["A", "A", "B", "B"], "Value": [1, 2, 3, 4], "Unique": [5, 6, 7, 8]}
    )
    group_columns = ["Group"]
    unique_columns = ["Value", "Unique"]
    result = isolate(df, group_columns, unique_columns)
    expected = pd.DataFrame(
        {"Group": ["A", "B"], "Value": [2, 4], "Unique": [6, 8]}, index=[1, 3]
    )
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), expected.reset_index(drop=True)
    )


def test_isolate_multiple_unique_columns():
    df = pd.DataFrame({"Group": ["A", "A"], "Value": [1, 1], "Unique": [5, 6]})
    group_columns = ["Group"]
    unique_columns = ["Value", "Unique"]
    result = isolate(df, group_columns, unique_columns)
    expected = pd.DataFrame({"Group": ["A"], "Value": [1], "Unique": [6]})
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True),
        expected.reset_index(drop=True),
        check_dtype=False,
    )


def test_isolate_no_group_columns():
    df = pd.DataFrame({"Value": [1, 2], "Unique": [5, 6]})
    group_columns = []
    unique_columns = ["Value", "Unique"]
    with pytest.raises(ValueError):
        isolate(df, group_columns, unique_columns)
