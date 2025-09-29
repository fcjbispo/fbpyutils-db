"""Data module providing utilities for data extraction, isolation, and normalization.

Example:
    from fbpyutils_db.data import extract, isolate, normalize
    
    # Extract data from a source
    data = extract(source='database')  # Returns extracted dataset
    
    # Isolate specific columns
    isolated_data = isolate(data, columns=['id', 'name'])  # Returns subset with specified columns
    
    # Normalize the isolated data
    normalized_data = normalize(isolated_data)  # Returns normalized dataset with consistent formats
"""