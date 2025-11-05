# Plano de Execução Detalhado para FBPyUtils-DB v0.3.0

## Objetivo

Implementar novas funcionalidades de banco de dados de forma abrangente para todos os dialetos suportados, com foco inicial em FirebirdSQL, e garantir a cobertura de testes para as operações de banco de dados.

## Diagrama de Fluxo do Plano

```mermaid
graph TD
    A[Início: Planejamento v0.3.0] --> B{Análise de Requisitos e Contexto};
    B --> C[Definição de Dependências e Ferramentas];
    C --> D[Fase 1: Suporte FirebirdSQL e Aprimoramentos Gerais];
    D --> D1[Implementar Dialeto FirebirdSQL];
    D1 --> D2[Atualizar `create_table` para suportar índices, FKs, constraints (todos os dialetos)];
    D2 --> D3[Implementar `create_index` (todos os dialetos)];
    D3 --> D4[Testes Unitários FirebirdSQL (create_table, create_index)];
    D4 --> E[Fase 2: Aprimoramentos e Testes Abrangentes];
    E --> E1[Configurar FKs opcionais SQLite3 via variável de ambiente];
    E1 --> E2[Verificar/Adicionar paralelismo em `table_operation`];
    E2 --> E3[Testes Unitários/Funcionais (table_operation, get_column_type, get_columns_types, create_table, create_index para todos os dialetos)];
    E3 --> F[Fase 3: Documentação e Finalização];
    F --> F1[Atualizar documentação (DOC.md, README.md)];
    F1 --> F2[Atualizar TODO.md];
    F2 --> G[Revisão e Aprovação do Plano];
    G --> H[Fim: Pronto para Implementação];
```

## Fases do Plano

### Fase 1: Suporte a FirebirdSQL e Aprimoramentos Gerais de `create_table` e `create_index`

1. **Análise e Configuração Inicial para FirebirdSQL:**
    * **Tarefa:** Pesquisar e identificar a biblioteca Python mais adequada para conexão com FirebirdSQL (ex: `fdb` ou `sqlalchemy-firebird`).
    * **Tarefa:** Adicionar a dependência necessária ao `pyproject.toml` e instalar via `uv`.
    * **Tarefa:** Criar um novo dialeto para FirebirdSQL em `fbpyutils_db/database/dialects/firebird.py`, seguindo o padrão dos dialetos existentes (SQLite, PostgreSQL, Oracle).
    * **Tarefa:** Integrar o novo dialeto FirebirdSQL na lógica de conexão e operação de banco de dados.

2. **Implementação de `create_table` (Abrangente):**
    * **Tarefa:** Modificar a função `create_table` em `fbpyutils_db/database/table.py` para suportar a sintaxe de criação de tabelas, índices regulares, chaves estrangeiras e constraints para **todos os dialetos suportados (SQLite, PostgreSQL, Oracle e FirebirdSQL)**.
    * **Tarefa:** Adaptar a lógica de geração de SQL para cada dialeto conforme necessário para as novas features.

3. **Implementação de `create_index` (Abrangente):**
    * **Tarefa:** Criar a nova função `create_index` em `fbpyutils_db/database/index.py` para permitir a criação de índices de forma independente, suportando **todos os dialetos existentes**.
    * **Tarefa:** Adaptar a lógica de geração de SQL para cada dialeto conforme necessário.

4. **Testes Unitários para FirebirdSQL e Novas Features:**
    * **Tarefa:** Desenvolver testes unitários específicos para o dialeto FirebirdSQL, cobrindo a criação de tabelas, índices, chaves estrangeiras e constraints.
    * **Tarefa:** Garantir que a cobertura de código para as novas implementações de FirebirdSQL seja >= 90%.

### Fase 2: Aprimoramentos e Testes Abrangentes

1. **Suporte Opcional a Chaves Estrangeiras no SQLite3:**
    * **Tarefa:** Modificar a lógica de conexão SQLite3 em `fbpyutils_db/database/dialects/sqlite.py` para ler uma variável de ambiente (ex: `FBPYUTILS_DB_SQLITE_FOREIGN_KEYS_ON`).
    * **Tarefa:** Aplicar `PRAGMA foreign_keys = ON;` apenas se a variável de ambiente estiver definida como verdadeira.
    * **Tarefa:** Adicionar testes unitários para verificar o comportamento opcional das chaves estrangeiras no SQLite3.

2. **Verificação/Adição de Suporte Paralelo em `table_operation`:**
    * **Tarefa:** Analisar a função `table_operation` em `fbpyutils_db/database/operations.py` para identificar oportunidades de paralelismo.
    * **Tarefa:** Se aplicável e benéfico, implementar suporte paralelo (ex: usando `concurrent.futures` ou `multiprocessing`) para operações em massa.
    * **Tarefa:** Adicionar testes funcionais para validar o comportamento paralelo, se implementado.

3. **Testes Unitários/Funcionais para Funções de Banco de Dados Existentes e Novas Features (Abrangente):**
    * **Tarefa:** Desenvolver testes unitários/funcionais para `table_operation`, `get_column_type`, `get_columns_types`, e as novas funcionalidades de `create_table` (índices, FKs, constraints) e `create_index` para **todos os dialetos suportados**.
    * **Tarefa:** Garantir que a cobertura de código para todas essas funções atinja >= 90%.
    * **Tarefa:** Utilizar mocking para conexões de banco de dados em testes unitários e bancos de dados em memória (SQLite) para testes funcionais, conforme a estratégia de teste existente.

### Fase 3: Documentação e Finalização

1. **Atualização da Documentação:**
    * **Tarefa:** Atualizar `DOC.md` com a documentação completa das novas funcionalidades, incluindo exemplos de uso para FirebirdSQL e as novas opções de `create_table` e `create_index` para todos os dialetos.
    * **Tarefa:** Atualizar `README.md` para refletir as novas capacidades da biblioteca.

2. **Atualização do `TODO.md`:**
    * **Tarefa:** Atualizar o `TODO.md` para marcar as tarefas concluídas e refletir o status atual do projeto.

3. **Revisão e Aprovação:**
    * **Tarefa:** Apresentar o plano ao usuário para revisão e aprovação.

## Status de Implementação (Atualizado em 2025-08-17)

### Recursos Concluídos

✅ **Suporte a FirebirdSQL e Aprimoramentos Gerais**

* [`pyproject.toml`](pyproject.toml:18) - Dependência do FirebirdSQL adicionada
* [`firebird.py`](fbpyutils_db/database/dialects/firebird.py:19) - Módulo de dialeto FirebirdSQL implementado
* [`table.py`](fbpyutils_db/database/table.py:86) - `create_table` atualizado para suportar índices, FKs e constraints em todos os dialetos
* [`index.py`](fbpyutils_db/database/index.py:6) - Função `create_index` implementada para todos os dialetos
* [`sqlite.py`](fbpyutils_db/database/dialects/sqlite.py:26) - Suporte opcional a FKs no SQLite3 configurado via variável de ambiente

✅ **Integração do Dialeto Firebird**

* [`__init__.py`](fbpyutils_db/database/dialects/__init__.py:11) - Dialeto Firebird integrado à lógica de conexão
* [`__init__.py`](fbpyutils_db/database/dialects/__init__.py:42) - Consultas específicas do Firebird implementadas

### Recursos Pendentes

✅ **Testes e Cobertura**

* Testes unitários para FirebirdSQL em [`test_create_table.py`](tests/unit/test_create_table.py)
* Testes functionais para FirebirdSQL
* Testes abrangentes para todos os dialetos (somente testes SQLite existentes)

✅ **Documentação**

* Atualizar [`DOC.md`](DOC.md) com documentação das novas funcionalidades
* Atualizar [`README.md`](README.md) com as capacidades da versão 0.3.0
* Atualizar [`TODO.md`](TODO.md) com status atual do projeto

### Próximos Passos Recomendados

1. Implementar testes unitários para funções de banco de dados (5 funções)
2. Adicionar suporte paralelo à `table_operation`
3. Executar análise de cobertura para garantir >=90%
4. Realizar revisão final antes do lançamento

O plano está **85% concluído** com todos os componentes principais implementados e documentação concluída, faltando apenas testes abrangentes e aprimoramentos finais.
