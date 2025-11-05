# Plano de Refatoração - Release v0.2.0

## Visão Geral
Este documento detalha o plano completo para refatorar o módulo `fbpyutils_db` da versão monolítica atual para uma arquitetura modular, mantendo retrocompatibilidade com warnings de deprecação até a v0.4.0.

## Objetivos
- **Refatoração modular** do código atual (973 linhas em `__init__.py`)
- **Compatibilidade multi-banco** (SQLite3, PostgreSQL, Oracle)
- **Aumentar cobertura de testes** para 90%+
- **Manter retrocompatibilidade** com warnings de deprecação

## Arquitetura Proposta

```mermaid
graph TD
    fbpyutils_db[fbpyutils_db]
    fbpyutils_db --> data[data/]
    fbpyutils_db --> database[database/]
    fbpyutils_db --> hashing[hashing/]
    fbpyutils_db --> visualization[visualization/]
    fbpyutils_db --> utils[utils/]
    
    data --> normalize[normalize.py]
    data --> isolate[isolate.py]
    data --> extract[extract.py]
    
    database --> operations[operations.py]
    database --> table[table.py]
    database --> index[index.py]
    database --> types[types.py]
    database --> dialects[dialects/]
    
    dialects --> sqlite[sqlite.py]
    dialects --> postgresql[postgresql.py]
    dialects --> oracle[oracle.py]
    
    hashing --> hash_column[hash_column.py]
    hashing --> hash_index[hash_index.py]
    
    visualization --> ascii_table[ascii_table.py]
    visualization --> display[display.py]
    
    utils --> nan_handler[nan_handler.py]
    utils --> validators[validators.py]
```

## Estrutura de Diretórios Final

```
fbpyutils_db/
├── __init__.py          # Retrocompatibilidade com warnings
├── data/
│   ├── __init__.py
│   ├── normalize.py
│   ├── isolate.py
│   └── extract.py
├── database/
│   ├── __init__.py
│   ├── operations.py
│   ├── table.py
│   ├── index.py
│   ├── types.py
│   └── dialects/
│       ├── __init__.py
│       ├── sqlite.py
│       ├── postgresql.py
│       └── oracle.py
├── hashing/
│   ├── __init__.py
│   ├── hash_column.py
│   └── hash_index.py
├── visualization/
│   ├── __init__.py
│   ├── ascii_table.py
│   └── display.py
├── utils/
│   ├── __init__.py
│   ├── nan_handler.py
│   └── validators.py
tests/
├── unit/
└── functional/
```

## Fases de Implementação

### Fase 1: Refatoração Modular (3-4 dias)
**Objetivo:** Dividir o código monolítico em módulos coesos mantendo retrocompatibilidade.

**Tarefas:**
1. Criar estrutura de diretórios
2. Extrair funções para módulos específicos
3. Implementar sistema de importação com warnings de deprecação
4. Garantir que todas as funções continuem acessíveis via `fbpyutils_db.*`

**Exemplo de warning de deprecação:**
```python
import warnings

def table_operation(*args, **kwargs):
    warnings.warn(
        "table_operation is deprecated and will be removed in v0.4.0. "
        "Use fbpyutils_db.database.table.operation instead.",
        DeprecationWarning,
        stacklevel=2
    )
    from .database.table import operation
    return operation(*args, **kwargs)
```

### Fase 2: Compatibilidade Multi-Banco (2-3 dias)
**Objetivo:** Adicionar suporte nativo para SQLite3, PostgreSQL e Oracle.

**Tarefas:**
1. Implementar detecção automática de dialect
2. Criar queries específicas para cada banco
3. Adicionar tratamento de diferenças de tipos de dados
4. Criar testes funcionais para cada banco

**Variáveis de ambiente para testes:**
- `DB_SQLITE_URL`: sqlite:///test.db
- `DB_PG_URL`: postgresql://user:pass@localhost/test
- `DB_ORA_URL`: oracle://user:pass@localhost:1521/test

### Fase 3: Testes e Documentação (2-3 dias)
**Objetivo:** Atingir 90%+ de cobertura de testes e documentar a nova arquitetura.

**Estrutura de Testes:**
- `tests/unit/` - Testes unitários (mockados, rápidos)
- `tests_functional/` - Testes de integração com bancos reais

**Comandos de teste:**
```bash
# Testes unitários
uv run pytest -s -vv --cov=fbpyutils_db --cov-report=xml:coverage.xml --cov-report=html:coverage_html --cov-fail-under=90 tests/unit/

# Testes funcionais (requer aprovação)
uv run pytest -s -vv tests_functional/
```

## Dependências

### Novas Dependências de Produção
```bash
uv add psycopg2-binary  # PostgreSQL
uv add cx-oracle        # Oracle
```

### Novas Dependências de Desenvolvimento
```bash
uv add --group dev pytest-postgresql
uv add --group dev pytest-oracle
```

### Tarefas pré-build
- Atualizar da versão v0.1.1 para v0.2.0 em pyproject.toml e app.json
- Realizar os testes unitários e funcionais

### Build
- Executar
```
uv lock && uv sync && uv build
```
- Copiar o arquivo .whl da nova versão para a pasta D:\Builds\fbpyutils_db


## Diretrizes de Segurança

### Testes com Bancos Reais
**IMPORTANTE:** Todos os testes funcionais que realizam conexões com bancos de dados reais **REQUEREM APROVAÇÃO EXPLÍCITA** antes da execução. Isso inclui:

1. Testes que usam as variáveis de ambiente `DB_ORA_URL`, `DB_PG_URL`, e `DB_SQLITE_URL`
2. Testes que criam/modificam dados em bancos de produção
3. Testes que podem afetar o estado de bancos compartilhados

**Processo de aprovação:**
- Os testes funcionais serão claramente identificados
- Um prompt de confirmação será exibido antes da execução
- O usuário pode optar por rodar apenas testes unitários

## Cronograma Estimado

| Fase | Duração | Entregáveis |
|------|---------|-------------|
| Fase 1 - Refatoração Modular | 3-4 dias | Código modularizado, retrocompatibilidade |
| Fase 2 - Multi-Banco | 2-3 dias | Suporte SQLite3/PostgreSQL/Oracle |
| Fase 3 - Testes | 2-3 dias | 90%+ cobertura, documentação atualizada |
| **Total** | **7-10 dias** | **Release v0.2.0 completa** |

## Checklist de Aprovação

- [x] Plano de refatoração aprovado
- [x] Estrutura de diretórios definida
- [x] Cronograma aceito
- [x] Diretrizes de segurança estabelecidas
- [ ] Aprovação para testes funcionais (será solicitada quando necessário)

## Próximos Passos

1. **Iniciar implementação** da Fase 1 (refatoração modular)
2. **Criar estrutura de diretórios** e módulos
3. **Implementar sistema de retrocompatibilidade** com warnings
4. **Adicionar testes** conforme avança o desenvolvimento

---

**Nota:** Este plano foi aprovado pelo usuário e está pronto para execução. Qualquer alteração requer nova aprovação.
