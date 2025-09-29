"""Database module providing utilities for database operations, table creation, indexing, and dialect support.

This module includes tools for managing database schemas, performing operations, and handling different database dialects such as PostgreSQL, Oracle, Firebird, and SQLite.

Example:
    from fbpyutils_db.database import create_table, Dialect
    
    # Initialize a dialect
    dialect = Dialect('postgresql')
    
    # Create a table
    create_table(dialect, 'users', columns=['id INTEGER PRIMARY KEY', 'name VARCHAR(100)'])
    # Creates a users table in PostgreSQL with specified columns
"""