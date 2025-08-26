import os
import pytest
import pandas as pd
import oracledb
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

from fbpyutils_db.database.operations import table_operation

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define as URLs de conexão a partir das variáveis de ambiente
# Os testes serão parametrizados para rodar com as URLs que estiverem definidas.
db_urls_to_test = []
if url := os.getenv("DB_SQLITE_URL"):
    db_urls_to_test.append(pytest.param(url, id="sqlite"))
if url := os.getenv("DB_PG_URL"):
    db_urls_to_test.append(pytest.param(url, id="postgresql"))
if url := os.getenv("DB_ORA_URL"):
    db_urls_to_test.append(pytest.param(url, id="oracle"))
if url := os.getenv("DB_FDB_URL"):
    db_urls_to_test.append(pytest.param(url, id="firebird"))

# Se nenhuma URL de banco de dados for fornecida, os testes falharão.
if not db_urls_to_test:
    pytest.fail(
        "Nenhuma URL de banco de dados configurada. "
        "Defina DB_SQLITE_URL, DB_PG_URL, ou DB_ORA_URL para rodar os testes funcionais.",
        pytrace=False
    )

@pytest.fixture(params=db_urls_to_test, scope="module")
def db_engine(request):
    """
    Fixture parametrizada para criar e retornar um engine de banco de dados.
    Pula o teste se a conexão com o banco de dados falhar.
    Limpa as tabelas de teste antes e depois de cada teste.
    """
    db_url = request.param
    try:
        engine = create_engine(db_url)
        # Testa a conexão
        with engine.connect():
            pass
    except Exception as e:
        pytest.skip(f"Não foi possível conectar ao banco de dados em {db_url}: {e}")

    table_names = ["test_table", "test_table_replace", "test_table_append"]

    # Limpa as tabelas antes dos testes
    with engine.connect() as connection:
        for table_name in table_names:
            if inspect(engine).has_table(table_name):
                connection.execute(text(f"DROP TABLE {table_name}"))
        connection.commit()
    
    yield engine
    
    # Limpa as tabelas depois dos testes
    with engine.connect() as connection:
        for table_name in table_names:
            if inspect(engine).has_table(table_name):
                connection.execute(text(f"DROP TABLE {table_name}"))
        connection.commit()

def test_table_operation_upsert(db_engine):
    """
    Testa a operação de upsert (inserção e atualização) em diferentes bancos de dados.
    """
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "value": [100, 200, 300]
    })
    table_name = "test_table"
    keys = ["id"]

    # Primeira inserção (upsert)
    result = table_operation(
        operation="upsert",
        dataframe=df,
        engine=db_engine,
        table_name=table_name,
        keys=keys
    )
    assert result["insertions"] == 3
    assert result["updates"] == 0
    assert not result["failures"]

    # Verifica se os dados foram inseridos corretamente
    with db_engine.connect() as connection:
        count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        assert count == 3
        data = pd.read_sql_table(table_name, connection, index_col="id")
        pd.testing.assert_frame_equal(
            df.set_index("id").sort_index(), 
            data.sort_index(), 
            check_dtype=False
        )

    # Atualiza dados existentes e insere um novo
    df_update = pd.DataFrame({
        "id": [1, 4],
        "name": ["Alicia", "David"],
        "value": [150, 400]
    })
    result_update = table_operation(
        operation="upsert",
        dataframe=df_update,
        engine=db_engine,
        table_name=table_name,
        keys=keys
    )
    assert result_update["insertions"] == 1
    assert result_update["updates"] == 1
    assert not result_update["failures"]

    # Verifica se os dados foram atualizados e inseridos corretamente
    with db_engine.connect() as connection:
        count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        assert count == 4
        expected_df = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "name": ["Alicia", "Bob", "Charlie", "David"],
            "value": [150, 200, 300, 400]
        }).set_index("id")
        data_after_update = pd.read_sql_table(table_name, connection, index_col="id")
        pd.testing.assert_frame_equal(
            expected_df.sort_index(), 
            data_after_update.sort_index(), 
            check_dtype=False
        )

def test_table_operation_replace(db_engine):
    """
    Testa a operação de replace (substituição completa da tabela).
    """
    df_initial = pd.DataFrame({
        "id": [1, 2],
        "name": ["Old A", "Old B"],
        "value": [10, 20]
    })
    table_name = "test_table_replace"

    # Insere dados iniciais
    table_operation(
        operation="append",
        dataframe=df_initial,
        engine=db_engine,
        table_name=table_name,
        keys=["id"]
    )
    with db_engine.connect() as connection:
        count_initial = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        assert count_initial == 2

    # Substitui a tabela com novos dados
    df_replace = pd.DataFrame({
        "id": [10, 11],
        "name": ["New X", "New Y"],
        "value": [1000, 1100]
    })
    result_replace = table_operation(
        operation="replace",
        dataframe=df_replace,
        engine=db_engine,
        table_name=table_name,
        keys=["id"]
    )
    assert result_replace["insertions"] == 2
    assert result_replace["updates"] == 0
    assert not result_replace["failures"]

    # Verifica se a tabela foi substituída corretamente
    with db_engine.connect() as connection:
        count_after_replace = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        assert count_after_replace == 2
        data_after_replace = pd.read_sql_table(table_name, connection, index_col="id")
        pd.testing.assert_frame_equal(
            df_replace.set_index("id").sort_index(), 
            data_after_replace.sort_index(), 
            check_dtype=False
        )

def test_table_operation_append(db_engine):
    """
    Testa a operação de append (apenas inserção de novos dados).
    """
    df_initial = pd.DataFrame({
        "id": [1, 2],
        "name": ["Append A", "Append B"],
        "value": [10, 20]
    })
    table_name = "test_table_append"
    keys = ["id"]

    # Primeira inserção (append)
    result_initial = table_operation(
        operation="append",
        dataframe=df_initial,
        engine=db_engine,
        table_name=table_name,
        keys=keys
    )
    assert result_initial["insertions"] == 2
    assert result_initial["updates"] == 0
    assert not result_initial["failures"]

    # Tenta adicionar dados, incluindo um ID duplicado (deve ser ignorado pelo append)
    df_append_more = pd.DataFrame({
        "id": [2, 3],
        "name": ["Append B Updated", "Append C"],
        "value": [25, 30]
    })
    result_append_more = table_operation(
        operation="append",
        dataframe=df_append_more,
        engine=db_engine,
        table_name=table_name,
        keys=keys
    )
    assert result_append_more["insertions"] == 1 # Apenas o ID 3 deve ser inserido
    assert result_append_more["updates"] == 0
    assert result_append_more["skips"] == 1 # O ID 2 deve ser pulado
    assert not result_append_more["failures"]

    # Verifica o estado final da tabela
    with db_engine.connect() as connection:
        count_final = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        assert count_final == 3
        expected_df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Append A", "Append B", "Append C"],
            "value": [10, 20, 30]
        }).set_index("id")
        data_final = pd.read_sql_table(table_name, connection, index_col="id")
        pd.testing.assert_frame_equal(
            expected_df.sort_index(), 
            data_final.sort_index(), 
            check_dtype=False
        )

