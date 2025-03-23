# fbpyutils-db

Este é um pacote Python que fornece funções utilitárias para manipulação de dados, tabelas e dataframes.

## Dependências

*   pandas
*   numpy
*   sqlalchemy

## Instalação

```bash
pip install fbpyutils-db
```

## Uso

O pacote oferece diversas funções para facilitar a manipulação de dados, incluindo:

*   `_deal_with_nans(x)`: Lida com valores nulos e tipos de dados em um dado input `x`.
*   `isolate(df, group_columns, unique_columns)`: Filtra o dataframe para isolar linhas com valores máximos em `unique_columns` para cada combinação única de valores em `group_columns`.
*   `_create_hash_column(x, y=12)`: Cria uma nova coluna de hash baseada nos valores de uma coluna existente no dataframe.
*   `add_hash_column(df, column_name, length=12, columns=[])`: Adiciona uma coluna de hash ao DataFrame fornecido.
*   `add_hash_index(df, index_name='id', length=12, columns=[])`: Substitui o índice do dataframe por uma string hash com comprimento de 12 caracteres.
*   `table_operation(operation, dataframe, engine, table_name, schema=None, keys=None, index=None, commit_at=50)`: Realiza operação de upsert ou replace em uma tabela com base no dataframe fornecido.
*   `create_table(dataframe, engine, table_name, schema=None, keys=None, index=None)`: Cria uma tabela no banco de dados usando o DataFrame pandas fornecido como um esquema.
*   `create_index(name, table, keys, unique=True)`: Cria um índice nas chaves especificadas para uma dada tabela.
*   `get_columns_types(dataframe, primary_keys=[])`: Retorna uma lista de objetos Column representando as colunas do dataframe fornecido.
*   `get_column_type(dtype)`: Mapeia tipos de dados Pandas para tipos de dados SQLAlchemy.
*   `get_data_from_pandas(df, include_index=False)`: Extrai dados e nomes de colunas de um DataFrame Pandas.
*   `ascii_table(data, columns=[], alignment='left', numrows=None)`: Cria uma representação de tabela ASCII dos dados fornecidos.
*   `print_ascii_table(data, columns=[], alignment='left')`: Imprime a representação de tabela ASCII dos dados fornecidos.
*   `print_ascii_table_from_dataframe(df, alignment='left')`: Imprime a representação de tabela ASCII de um DataFrame pandas.
*   `normalize_columns(cols)`: Normaliza uma lista de nomes de colunas.
*   `print_columns(cols, normalize=False, length=None, quotes=False)`: Imprime uma representação de string formatada de uma lista de colunas.

## Documentação

Para documentação completa e exemplos de uso, consulte o [GitHub do projeto](https://github.com/seu-usuario/fbpyutils-db).

## Licença

[MIT](LICENSE)