# TODO List for fbpyutils-db

This file tracks the implementation and testing status of features in the `fbpyutils-db` library based on `DOC.md` and existing test files.

| Feature Name                       | Initialized | Implemented | Tested | Coverage | Notes                                      |
| ---------------------------------- | :---------: | :---------: | :----: | :------: | ------------------------------------------ |
| `_deal_with_nans`                  |      ✅      |      ✅      |   ❌   |  52.08%  | Internal function, documented.             |
| `isolate`                          |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_isolate.py` |
| `_create_hash_column`              |      ✅      |      ✅      |   ⚠️   |  52.08%  | Internal, tested via other functions.      |
| `_check_columns`                   |      ✅      |      ✅      |   ⚠️   |  52.08%  | Internal, tested via other functions.      |
| `add_hash_column`                  |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_add_hash_column.py` |
| `add_hash_index`                   |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_add_hash_index.py` |
| `table_operation`                  |      ✅      |      ✅      |   ❌   |  52.08%  | Documented. Needs tests.                   |
| `create_table`                     |      ✅      |      ✅      |   ❌   |  52.08%  | Documented. Needs tests.                   |
| `create_index`                     |      ✅      |      ✅      |   ❌   |  52.08%  | Documented. Needs tests.                   |
| `get_columns_types`                |      ✅      |      ✅      |   ❌   |  52.08%  | Documented. Needs tests.                   |
| `get_column_type`                  |      ✅      |      ✅      |   ❌   |  52.08%  | Documented. Needs tests.                   |
| `get_data_from_pandas`             |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_get_data_from_pandas.py` |
| `ascii_table`                      |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_ascii_table.py` |
| `print_ascii_table`                |      ✅      |      ✅      |   ⚠️   |  52.08%  | Documented. Needs direct tests.            |
| `print_ascii_table_from_dataframe` |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_print_ascii_table_from_dataframe.py` |
| `normalize_columns`                |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_normalize_columns.py` |
| `print_columns`                    |      ✅      |      ✅      |   ✅   |  52.08%  | Documented. Test file: `test_print_columns.py` |

**Legend:**
- ✅: Yes
- ❌: No
- ⚠️: Partially / Indirectly
- N/A: Not Applicable (Used for internal functions or when coverage data is not the primary focus)

**Next Steps:**
- Implement unit tests for functions marked with ❌ or ⚠️ in the 'Tested' column.
- Improve code coverage by adding tests for uncovered lines (currently 52.08%).
