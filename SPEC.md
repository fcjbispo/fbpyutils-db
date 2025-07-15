# SPEC.md - FBPyUtils-DB Specification

## Project Overview
FBPyUtils-DB is a Python utility library focused on database operations and data manipulation, providing tools for data processing, hashing, and table formatting.

## Functional Requirements

### Core Utilities
1. **Data Normalization**
   - Normalize column names by removing special characters and converting to lowercase
   - Validate column names for database compatibility

2. **Data Hashing**
   - Generate hash-based columns for data integrity
   - Create hash-based indexes for DataFrames
   - Support configurable hash length

3. **Database Operations**
   - Create database tables from pandas DataFrames
   - Map pandas data types to SQLAlchemy types
   - Support bulk operations (append, upsert, replace)
   - Manage database indexes

4. **Data Visualization**
   - Generate ASCII table representations
   - Display DataFrame contents in formatted tables
   - Support different alignment options

5. **Data Processing**
   - Handle null values in DataFrames
   - Isolate rows based on group criteria
   - Extract data from pandas DataFrames

## Non-Functional Requirements

### Performance
- Handle datasets with up to 100,000 rows efficiently
- Memory usage should scale linearly with data size

### Compatibility
- Python 3.8+ compatibility
- Cross-platform support (Windows, Linux, macOS)
- SQLAlchemy 1.4+ compatibility

### Quality Assurance
- Test coverage >= 90%
- Type hints throughout codebase
- Comprehensive documentation
- Error handling with informative messages

## API Specification

### Public Functions

#### Data Processing
- `normalize_columns(cols: List[str]) -> List[str]`
- `isolate(df: pd.DataFrame, group_columns: List[str]) -> pd.DataFrame`
- `get_data_from_pandas(df: pd.DataFrame, include_index: bool = False) -> Tuple[List[List[Any]], List[str]]`

#### Hashing
- `add_hash_column(df: pd.DataFrame, column_name: str, length: int = 12, columns: List[str] = None) -> pd.DataFrame`
- `add_hash_index(df: pd.DataFrame, index_name: str = 'id', length: int = 12, columns: List[str] = None) -> pd.DataFrame`

#### Database Operations
- `create_table(dataframe: pd.DataFrame, engine: Engine, table_name: str, schema: str = None, keys: List[str] = [], index: str = None) -> None`
- `table_operation(operation: str, dataframe: pd.DataFrame, engine: Engine, table_name: str, schema: str = None, keys: List[str] = [], index: str = None, commit_at: int = 50) -> Dict[str, Any]`
- `create_index(name: str, table: Selectable, keys: List[str], unique: bool = True) -> Index`
- `get_column_type(dtype: np.dtype) -> TypeEngine`
- `get_columns_types(dataframe: pd.DataFrame, primary_keys: List[str] = []) -> List[Column]`

#### Visualization
- `ascii_table(data: List[List[Any]], columns: List[str] = [], alignment: str = 'left', numrows: int = None) -> List[str]`
- `print_ascii_table(data: List[List[Any]], columns: List[str] = [], alignment: str = 'left', numrows: int = None) -> None`
- `print_ascii_table_from_dataframe(df: pd.DataFrame, alignment: str = 'left') -> None`
- `print_columns(cols: List[str], normalize: bool = False, length: int = None, quotes: bool = False) -> None`

### Internal Functions
- `_deal_with_nans(df: pd.DataFrame) -> pd.DataFrame`
- `_create_hash_column(x: pd.Series, y: int = 12) -> pd.Series`
- `_check_columns(df: pd.DataFrame, columns: List[str]) -> bool`

## Data Types Mapping

| Pandas Type | SQLAlchemy Type |
|-------------|-----------------|
| int64       | INTEGER         |
| float64     | FLOAT           |
| object      | VARCHAR(4000)   |
| bool        | BOOLEAN         |
| datetime64  | DATETIME        |

## Error Handling
- All functions should provide clear error messages
- Validate input parameters
- Handle edge cases gracefully
- Log errors appropriately

## Testing Requirements
- Unit tests for all public functions
- Integration tests for database operations
- Edge case testing
- Performance benchmarks for large datasets

## Documentation Requirements
- Google-style docstrings for all functions
- Usage examples in documentation
- Type hints for all parameters and return values
- README with installation and usage instructions
