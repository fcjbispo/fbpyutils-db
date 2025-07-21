import io
import sys
import pytest
from fbpyutils_db import print_columns, normalize_columns


def test_print_columns_valid_input(capsys):
    cols = ["Name", "Age", "Address"]
    print_columns(cols)
    captured = capsys.readouterr()
    assert captured.out == "Name   , Age    , Address\n"




def test_print_columns_normalize(capsys):
    cols = ["Name!", "Age@", "#Address"]
    with pytest.raises(AttributeError):
        normalize_columns(cols)


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
    with pytest.raises(AttributeError):
        normalize_columns(cols)
