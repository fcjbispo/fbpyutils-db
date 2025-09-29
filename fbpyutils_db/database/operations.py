import pandas as pd
from sqlalchemy import Engine, MetaData, Table, text, inspect
from sqlalchemy.sql import exists
from typing import Any, Dict, List

from fbpyutils_db import logger

# Importa funções de outros módulos
from fbpyutils_db.utils.nan_handler import deal_with_nans
from fbpyutils_db.database.table import create_table

def table_operation(
    operation: str,
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str,
    schema: str = None,
    keys: list[str] = None,
    index: str = None,
    commit_at: int = 50,
    parallel: bool = False,
    max_workers: int = None,
) -> Dict[str, Any]:
    """
    Perform append, upsert, or replace operation on a database table using a DataFrame.

    This function handles data insertion, updating existing rows based on keys, or replacing
    the entire table content. It creates the table if it does not exist and optionally
    creates indexes.

    Args:
        operation: The operation type ('append', 'upsert', or 'replace').
        dataframe: Pandas DataFrame with data to insert or update.
        engine: SQLAlchemy database engine.
        table_name: Name of the target table.
        schema: Optional schema name to prefix the table.
        keys: List of column names for upsert keys (required for 'upsert').
        index: Index type to create on keys ('standard', 'unique', or 'primary'). Defaults to None.
        commit_at: Rows to commit in batches. Defaults to 50.
        parallel: Enable parallel processing. Defaults to False.
        max_workers: Number of parallel workers. Defaults to None (auto-detected).

    Returns:
        Dict[str, Any]: Summary with 'operation', 'table_name', 'insertions', 'updates',
        'skips', and 'failures'.

    Raises:
        ValueError: For invalid operation, DataFrame type, missing keys, or invalid parameters.

    Example:
        >>> import pandas as pd
        >>> from sqlalchemy import create_engine
        >>> df = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
        >>> engine = create_engine('sqlite:///:memory:')
        >>> result = table_operation('upsert', df, engine, 'users', keys=['id'])
        >>> print(result['insertions'])
        2
        # Inserts 2 new rows into 'users' table.
    """
    logger.info(f"Starting table operation: {operation}")
    logger.debug(f"Table: {table_name}, Schema: {schema}")
    logger.debug(f"Keys: {keys}, Index: {index}, Commit at: {commit_at}")
    
    # Check parameters
    if operation not in ("append", "upsert", "replace"):
        logger.error(f"Invalid operation: {operation}")
        raise ValueError("Invalid operation. Valid values: append|upsert|replace.")

    if not isinstance(dataframe, pd.DataFrame):
        logger.error("Invalid DataFrame type provided")
        raise ValueError("Dataframe must be a Pandas DataFrame.")
    
    logger.debug(f"DataFrame shape: {dataframe.shape}") # Moved this line after DataFrame validation

    if operation == "upsert" and not keys:
        logger.error("Missing keys parameter for upsert operation")
        raise ValueError("For upsert operation 'keys' parameter is mandatory.")

    if keys and not type(keys) == list:
        logger.error("Invalid keys type provided")
        raise ValueError("Parameters 'keys' must be a list of str.")

    if (keys and index) and index not in ("standard", "unique", "primary"):
        logger.error(f"Invalid index type: {index}")
        raise ValueError(
            "If an index will be created, it must be any of standard|unique|primary."
        )

    if not isinstance(commit_at, int) or commit_at < 1:
        logger.error(f"Invalid commit_at value: {commit_at}")
        raise ValueError("Commit At must be a positive integer.")

    if not type(parallel) == bool:
        logger.error(f"Invalid parallel type: {parallel}")
        raise ValueError("Parallel must be a boolean value.")

    # Check if the table exists in the database, if not create it
    table_exists = inspect(engine).has_table(table_name, schema=schema)
    logger.debug(f"Table '{table_name}' exists: {table_exists}")
    
    if not table_exists:
        logger.info(f"Creating table '{table_name}' as it doesn't exist")
        create_table(dataframe, engine, table_name, schema, keys, index)

    # Get the table object
    metadata = MetaData(schema)
    table = Table(table_name, metadata, autoload_with=engine)

    # Initialize reports for insertions, updates, and failures
    inserts = 0
    updates = 0
    skips = 0
    processed_rows = 0 # Initialize processed_rows here
    failures = []
    
    logger.info(f"Starting {operation} operation on {len(dataframe)} rows")

    total_rows = len(dataframe) # Initialize total_rows here

    try:
        with engine.connect() as conn:
            step = "drop table"
            if operation == "replace":
                logger.info("Performing replace operation - clearing table")
                conn.execute(table.delete())
                conn.commit()
                logger.debug("Table cleared successfully")
                
                # Parallel processing implementation
                if parallel:
                    # Determine max_workers if not specified
                    if max_workers is None:
                        import os
                        max_workers = min(32, (os.cpu_count() or 1) + 4)
                    
                    logger.info(f"Processing {total_rows} rows in parallel with {max_workers} workers")
                    from concurrent.futures import ThreadPoolExecutor
                    
                    # Function to process a single row with its own connection
                    def process_row(row_data, row_idx, table, keys, operation, engine):
                        try:
                            with engine.connect() as worker_conn:
                                values = {
                                    col: deal_with_nans(row_data[col]) for col in dataframe.columns
                                }
                                
                                row_exists = False
                                if keys:
                                    exists_query = table.select().where(
                                        text(" AND ".join([f"{col} = :{col}" for col in keys]))
                                    ).params(**values)
                                    row_exists = worker_conn.execute(exists_query).fetchone() is not None
                                
                                if row_exists:
                                    if operation == "upsert":
                                        update_values = {
                                            k: values[k] for k in values.keys() if k not in keys
                                        }
                                        update_stmt = table.update().where(
                                            text(" AND ".join([f"{col}=:{col}" for col in keys]))
                                        ).values(**update_values)
                                        worker_conn.execute(update_stmt)
                                        return ("update", row_idx, values)
                                    return ("skip", row_idx, values)
                                
                                insert_stmt = table.insert().values(**values)
                                worker_conn.execute(insert_stmt)
                                return ("insert", row_idx, values)
                        except Exception as e:
                            return ("error", row_idx, values, str(e))
                    
                    # Process all rows in parallel
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = [
                            executor.submit(process_row, row, i, table, keys, operation, engine)
                            for i, row in dataframe.iterrows()
                        ]
                        
                        for future in futures:
                            result = future.result()
                            if result[0] == "insert":
                                inserts += 1
                            elif result[0] == "update":
                                updates += 1
                            elif result[0] == "skip":
                                skips += 1
                            else:
                                failures.append({
                                    "step": "parallel processing",
                                    "row": result[1],
                                    "error": result[3] if len(result) > 3 else "Unknown error"
                                })
                else:
                    # If parallel is False, the sequential processing will be handled below
                    pass # No-op, as sequential processing is now outside this block

            # Sequential processing (original logic, now outside the 'if operation == "replace"' block)
            if not parallel:
                rows = 0
                for i, row in dataframe.iterrows():
                    try:
                        values = {
                            col: deal_with_nans(row[col]) for col in dataframe.columns
                        }
                    
                        logger.debug(f"Processing row {i}/{total_rows}: {values}")
                        
                        row_exists = False
                        step = "check existence"
                        if keys:
                            # Check if row exists in the table based on keys
                            exists_query = (
                                table.select()
                                .where(
                                    exists(
                                        table.select().where(
                                            text(
                                                " AND ".join(
                                                    [f"{col} = :{col}" for col in keys]
                                                )
                                            )
                                        )
                                    )
                                )
                                .params(**values)
                            )
                            if conn.execute(exists_query).fetchone():
                                row_exists = True
                                logger.debug(f"Row {i} exists based on keys {keys}")
                        
                        if row_exists:
                            if operation == "upsert":
                                # Perform update
                                step = "replace with update"
                                update_values = {
                                    k: values[k] for k in values.keys() if k not in keys
                                }
                                
                                logger.debug(f"Updating row {i} with values: {update_values}")

                                update_stmt = (
                                    table.update()
                                    .where(
                                        text(
                                            " AND ".join([f"{col}=:{col}" for col in keys])
                                        )
                                    )
                                    .values(**update_values)
                                )

                                update_stmt = text(str(update_stmt))
                                conn.execute(update_stmt, values)
                                updates += 1
                                logger.debug(f"Row {i} updated successfully")
                            else:
                                skips += 1
                                logger.debug(f"Row {i} skipped (already exists)")
                        else:
                            # Perform insert
                            step = "perform insert"
                            insert_stmt = table.insert().values(**values)
                            conn.execute(insert_stmt)
                            inserts += 1
                            logger.debug(f"Row {i} inserted successfully")

                        rows += 1
                        processed_rows += 1
                        
                        if rows >= commit_at:
                            conn.commit()
                            logger.debug(f"Committed {rows} rows")
                            rows = 0
                            
                        if processed_rows % 100 == 0:
                            logger.info(f"Processed {processed_rows}/{len(dataframe)} rows")
                            
                    except Exception as e:
                        logger.error(f"Error processing row {i}/{total_rows}: {str(e)}")
                        failures.append(
                            {
                                "step": step,
                                "row": (
                                    i,
                                    ", ".join(
                                        [f"{k}='{str(v)}'" for k, v in values.items()]
                                    ),
                                ),
                                "error": str(e),
                            }
                        )
                        conn.rollback()
                        continue
                conn.commit()
                logger.info(f"Operation completed. Total processed: {processed_rows}")
    except Exception as e:
        logger.error(f"Critical error in table operation: {str(e)}")
        conn.rollback()
        failures.append({"step": step, "row": None, "error": str(e)})

    result = {
        "operation": operation,
        "table_name": f"{schema}.{table_name}" if schema else table_name,
        "insertions": inserts,
        "updates": updates,
        "skips": skips,
        "failures": failures,
    }
    
    logger.info(f"Operation summary: {inserts} inserts, {updates} updates, {skips} skips, {len(failures)} failures")
    
    if failures:
        logger.warning(f"Operation completed with {len(failures)} failures")
        for failure in failures[:5]:  # Log first 5 failures
            logger.warning(f"Failure: {failure}")
    
    return result
