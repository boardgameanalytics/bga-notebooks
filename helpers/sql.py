"""SQL helper functions"""

import pandas as pd

def sql_query(filename: str, conn: str) -> pd.DataFrame:
    """Load SQL query from .sql file

    Args:
        filename (str): SQL file location
        conn (str): SQLAlchemy engine to connect with

    Returns:
        pd.DataFrame
    """
    # Open and read the file as a single buffer
    with open(filename, 'r') as file:
        query = file.read()
    
    return pd.read_sql_query(query, conn)
