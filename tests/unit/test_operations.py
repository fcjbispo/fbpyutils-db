import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine, text
from fbpyutils_db.database.operations import table_operation

# Fixture para um DataFrame de teste
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "value": [100, 200, 300]
    })

# Fixture para um engine de banco de dados mockado
@pytest.fixture
def mock_engine():
    engine = create_engine("sqlite:///:memory:")
    return engine

# Testes para validação de parâmetros
def test_table_operation_invalid_operation(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="Invalid operation. Valid values: append|upsert|replace."):
        table_operation(
            operation="invalid",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table"
        )

def test_table_operation_invalid_dataframe_type(mock_engine):
    with pytest.raises(ValueError, match="Dataframe must be a Pandas DataFrame."):
        table_operation(
            operation="upsert",
            dataframe="not_a_dataframe",
            engine=mock_engine,
            table_name="test_table",
            keys=["id"]
        )

def test_table_operation_missing_keys_for_upsert(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="For upsert operation 'keys' parameter is mandatory."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table"
        )

def test_table_operation_invalid_keys_type(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="Parameters 'keys' must be a list of str."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table",
            keys="not_a_list"
        )

def test_table_operation_invalid_index_type(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="If an index will be created, it must be any of standard|unique|primary."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table",
            keys=["id"],
            index="invalid_index"
        )

def test_table_operation_invalid_commit_at_type(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="Commit At must be a positive integer."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table",
            keys=["id"],
            commit_at="not_an_int"
        )

def test_table_operation_invalid_commit_at_value(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="Commit At must be a positive integer."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table",
            keys=["id"],
            commit_at=0
        )

def test_table_operation_invalid_parallel_type(sample_dataframe, mock_engine):
    with pytest.raises(ValueError, match="Parallel must be a boolean value."):
        table_operation(
            operation="upsert",
            dataframe=sample_dataframe,
            engine=mock_engine,
            table_name="test_table",
            keys=["id"],
            parallel="not_a_bool"
        )