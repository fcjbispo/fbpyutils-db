"""fbpyutils_db: Package providing utilities for database operations, data extraction, normalization, hashing, and visualization.

This package provides comprehensive utilities for database operations including:
- Database operations (create tables, indexes, manage data)
- Data extraction and isolation from various sources
- Data normalization and validation
- Hashing capabilities for columns and indexes
- Visualization tools for displaying data

Example usage:
    import fbpyutils_db
    
    # Setup logger and environment
    env = fbpyutils_db.env
    logger = fbpyutils_db.logger
    
    # Use database operations
    from fbpyutils_db.database import create_table, create_index
    
    # Use data utilities
    from fbpyutils_db.data import extract_data, normalize_columns
    
    # Use hashing utilities
    from fbpyutils_db.hashing import add_hash_column, add_hash_index
    
    # Use visualization utilities
    from fbpyutils_db.visualization import print_ascii_table_from_dataframe
"""
import os

import fbpyutils

# Setup logger and environment first
fbpyutils.setup(os.path.join(os.path.dirname(__file__), "app.json"))
env = fbpyutils.get_env()
logger = fbpyutils.get_logger()
