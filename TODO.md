# TODO List for fbpyutils-db

This file tracks the implementation and testing status of features in the `fbpyutils-db` library based on `SPEC.md` and existing test files.

## Implementation Status

| Feature Name | Initialized | Implemented | Tested | Coverage | Notes |
|--------------|-------------|-------------|--------|----------|-------|
| **Data Processing** |
| `normalize_columns` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `isolate` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `get_data_from_pandas` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `_deal_with_nans` | ✅ | ✅ | ⚠️ | 100% | Internal function, tested via other functions |
| `_check_columns` | ✅ | ✅ | ⚠️ | 100% | Internal function, tested via other functions |

| **Hashing** |
| `add_hash_column` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `add_hash_index` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `_create_hash_column` | ✅ | ✅ | ⚠️ | 100% | Internal function, tested via other functions |

| **Database Operations** |
| `create_table` | ✅ | ✅ | ❌ | 0% | Implemented, needs tests |
| `table_operation` | ✅ | ✅ | ❌ | 0% | Implemented, needs tests |
| `create_index` | ✅ | ✅ | ❌ | 0% | Implemented, needs tests |
| `get_column_type` | ✅ | ✅ | ❌ | 0% | Implemented, needs tests |
| `get_columns_types` | ✅ | ✅ | ❌ | 0% | Implemented, needs tests |

| **Visualization** |
| `ascii_table` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `print_ascii_table` | ✅ | ✅ | ⚠️ | 100% | Tested via `print_ascii_table_from_dataframe` |
| `print_ascii_table_from_dataframe` | ✅ | ✅ | ✅ | 100% | Complete with tests |
| `print_columns` | ✅ | ✅ | ✅ | 100% | Complete with tests |

## Legend
- ✅: Yes - Fully implemented and tested
- ❌: No - Not implemented or not tested
- ⚠️: Partially - Implemented but needs direct tests or is internal

## Current Test Coverage
- **Overall Coverage**: 52.08% (confirmed via coverage.xml - 125/240 lines covered)
- **Tested Functions**: 8 out of 13 public functions
- **Functions Needing Tests**: 5 (database-related functions)
- **Critical Gap**: Database operations module needs comprehensive testing

## Next Steps
1. **High Priority**: 
   - Add new features to `create_table` operation:
         - Support for creating regular indexes
         - Support for creating foreign keys
         - Support for creating constraints
   - Set foreign key constraint support on SQLite3 connections using PRAGMA foreign_keys = ON;
   - Add `create_index` operation
   - Check/Add parallel support on `table_operation`
   - Add unit tests for database-related functions
      - `create_table`
      - `table_operation`
      - `create_index`
      - `get_column_type`
      - `get_columns_types`

2. **Medium Priority**: Add integration tests for database workflows
3. **Low Priority**: Add performance benchmarks for large datasets

## Testing Strategy
- Use pytest with pytest-cov for coverage
- Mock database connections for unit tests
- Use SQLite in-memory database for integration tests
- Target 100% coverage for all public functions

## Documentation Status
- ✅ SPEC.md: Created with complete API specification
- ✅ DOC.md: Comprehensive documentation with examples
- ✅ README.md: Updated with project overview and links
- ✅ Memory Bank: Complete with VIBE guidelines
