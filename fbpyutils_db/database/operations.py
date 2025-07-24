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
) -> Dict[str, Any]:
    """
    Perform upsert or replace operation on a table based on the provided dataframe.

    Args:
        operation (str, optional): The operation to be performed ('append', 'upsert' or 'replace').
        dataframe (pd.DataFrame): The pandas DataFrame containing the data to be inserted or updated.
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine engine.
        table_name (str): The name of the table to operate on.
        schema (str, optional): the schena name to preffix the table objects.
        keys (list of str, required for operation=upsert): List of column names to use as keys for upsert operation.
        index (str, optional): Whether to create an index and what kind using the keys. Default is None (not create index).
            If an index must be created, index be in 'standard' or 'unique'.
        commit_at (int, optional): Number of rows to commit in the database at once. Defaults to 50.
            Must be > 1 and < total rows of the dataframe.

    Returns:
        dict: A dictionary containing information about the performed operation.

    """
    logger.info(f"Starting table operation: {operation}")
    logger.debug(f"Table: {table_name}, Schema: {schema}")
    logger.debug(f"DataFrame shape: {dataframe.shape}")
    logger.debug(f"Keys: {keys}, Index: {index}, Commit at: {commit_at}")
    
    # Check parameters
    if operation not in ("append", "upsert", "replace"):
        logger.error(f"Invalid operation: {operation}")
        raise ValueError("Invalid operation. Valid values: append|upsert|replace.")

    if not type(dataframe) == pd.DataFrame:
        logger.error("Invalid DataFrame type provided")
        raise ValueError("Dataframe must be a Pandas DataFrame.")

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

    commit_at = commit_at or 50
    if not type(commit_at) == int or (commit_at < 1 and commit_at > len(dataframe)):
        logger.error(f"Invalid commit_at value: {commit_at}")
        raise ValueError("Commit At must be > 1 and < total rows of DataFrame.")

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
    failures = []
    
    logger.info(f"Starting {operation} operation on {len(dataframe)} rows")

    try:
        with engine.connect() as conn:
            step = "drop table"
            if operation == "replace":
                logger.info("Performing replace operation - clearing table")
                conn.execute(table.delete())
                conn.commit()
                logger.debug("Table cleared successfully")

            rows = 0
            processed_rows = 0
            
            for i, row in dataframe.iterrows():
                try:
                    values = {
                        col: deal_with_nans(row[col]) for col in dataframe.columns
                    }
                    
                    logger.debug(f"Processing row {i}: {values}")

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
                    logger.error(f"Error processing row {i}: {str(e)}")
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
