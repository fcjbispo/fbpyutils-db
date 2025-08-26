import io
import sys
import pytest
from fbpyutils_db.visualization.display import print_columns
from fbpyutils_db.data.normalize import normalize_columns


def test_print_columns_valid_input(capsys):
    cols = ["Name", "Age", "Address"]
    print_columns(cols)
    captured = capsys.readouterr()
    assert captured.out == "Name   , Age    , Address\n"




def test_print_columns_normalize(capsys):
    cols = ["Name!", "Age@", "#Address"]
    result = normalize_columns(cols)
    assert result == ["name", "age", "address"]


def test_print_columns_length(capsys):
    cols = ["Name", "Age", "Address"]
    print_columns(cols, length=10)
    captured = capsys.readouterr()
    assert captured.out == "Name      , Age       , Address   \n"


def test_print_columns_quotes(capsys):
    cols = ["Name", "Age", "Address"]
    print_columns(cols, quotes=True)
    captured = capsys.readouterr()
    assert captured.out == "'Name'   , 'Age'    , 'Address'\n"


def test_print_columns_all_options(capsys):
    cols = ["Name!", "Age@", "#Address"]
    result = normalize_columns(cols)
    assert result == ["name", "age", "address"]
