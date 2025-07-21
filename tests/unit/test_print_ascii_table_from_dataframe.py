import pandas as pd
import pytest
from fbpyutils_db import print_ascii_table_from_dataframe
from io import StringIO
import sys


def test_print_ascii_table_from_dataframe_valid_dataframe(capsys):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    print_ascii_table_from_dataframe(df)
    captured = capsys.readouterr()
    assert "col1" in captured.out
    assert "col2" in captured.out


def test_print_ascii_table_from_dataframe_invalid_dataframe():
    with pytest.raises(ValueError):
        print_ascii_table_from_dataframe("not a dataframe")


def test_print_ascii_table_from_dataframe_empty_dataframe(capsys):
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        print_ascii_table_from_dataframe(df)


def test_print_ascii_table_from_dataframe_alignment(capsys):
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    print_ascii_table_from_dataframe(df, alignment="center")
    captured = capsys.readouterr()
    assert "col1" in captured.out
    assert "col2" in captured.out
