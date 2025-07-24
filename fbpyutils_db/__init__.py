"""
Utility functions to manipulate data, tables and dataframes.
"""

import os
import re
import warnings
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
import numpy as np
from sqlalchemy import (
    Engine,
    Selectable,
    inspect,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    text,
    Index,
)
from sqlalchemy.sql.sqltypes import TypeEngine
from sqlalchemy.sql import exists

import fbpyutils

# Setup logger and environment first
fbpyutils.setup(os.path.join(os.path.dirname(__file__), "app.json"))
env = fbpyutils.get_env()
logger = fbpyutils.get_logger()

# Importações diretas para acesso via fbpyutils_db.function_name()
from .utils.nan_handler import deal_with_nans
from .utils.validators import check_columns
from .hashing.hash_column import create_hash_column, add_hash_column
from .hashing.hash_index import add_hash_index
from .data.isolate import isolate
from .data.extract import get_data_from_pandas
from .data.normalize import normalize_columns
from .visualization.ascii_table import ascii_table, print_ascii_table
from .visualization.display import print_ascii_table_from_dataframe, print_columns
from .database.operations import table_operation
from .database.table import create_table
from .database.index import create_index
from .database.types import get_columns_types, get_column_type


# Stubs de deprecação para manter retrocompatibilidade
def _deal_with_nans_deprecated(*args, **kwargs):
    warnings.warn(
        "_deal_with_nans is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.utils.nan_handler.deal_with_nans instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return deal_with_nans(*args, **kwargs)

def _check_columns_deprecated(*args, **kwargs):
    warnings.warn(
        "_check_columns is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.utils.validators.check_columns instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return check_columns(*args, **kwargs)

def _create_hash_column_deprecated(*args, **kwargs):
    warnings.warn(
        "_create_hash_column is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.hashing.hash_column.create_hash_column instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return create_hash_column(*args, **kwargs)

def add_hash_column_deprecated(*args, **kwargs):
    warnings.warn(
        "add_hash_column is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.hashing.hash_column.add_hash_column instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return add_hash_column(*args, **kwargs)

def add_hash_index_deprecated(*args, **kwargs):
    warnings.warn(
        "add_hash_index is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.hashing.hash_index.add_hash_index instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return add_hash_index(*args, **kwargs)

def isolate_deprecated(*args, **kwargs):
    warnings.warn(
        "isolate is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.data.isolate.isolate instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return isolate(*args, **kwargs)

def get_data_from_pandas_deprecated(*args, **kwargs):
    warnings.warn(
        "get_data_from_pandas is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.data.extract.get_data_from_pandas instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_data_from_pandas(*args, **kwargs)

def normalize_columns_deprecated(*args, **kwargs):
    warnings.warn(
        "normalize_columns is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.data.normalize.normalize_columns instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return normalize_columns(*args, **kwargs)

def ascii_table_deprecated(*args, **kwargs):
    warnings.warn(
        "ascii_table is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.visualization.ascii_table.ascii_table instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return ascii_table(*args, **kwargs)

def print_ascii_table_deprecated(*args, **kwargs):
    warnings.warn(
        "print_ascii_table is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.visualization.ascii_table.print_ascii_table instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return print_ascii_table(*args, **kwargs)

def print_ascii_table_from_dataframe_deprecated(*args, **kwargs):
    warnings.warn(
        "print_ascii_table_from_dataframe is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.visualization.display.print_ascii_table_from_dataframe instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return print_ascii_table_from_dataframe(*args, **kwargs)

def print_columns_deprecated(*args, **kwargs):
    warnings.warn(
        "print_columns is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.visualization.display.print_columns instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return print_columns(*args, **kwargs)

def table_operation_deprecated(*args, **kwargs):
    warnings.warn(
        "table_operation is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.operations.table_operation instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return table_operation(*args, **kwargs)

def create_table_deprecated(*args, **kwargs):
    warnings.warn(
        "create_table is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.table.create_table instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return create_table(*args, **kwargs)

def create_index_deprecated(*args, **kwargs):
    warnings.warn(
        "create_index is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.index.create_index instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return create_index(*args, **kwargs)

def get_columns_types_deprecated(*args, **kwargs):
    warnings.warn(
        "get_columns_types is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.types.get_columns_types instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_columns_types(*args, **kwargs)

def get_column_type_deprecated(*args, **kwargs):
    warnings.warn(
        "get_column_type is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.types.get_column_type instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_column_type(*args, **kwargs)
