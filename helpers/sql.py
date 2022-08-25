"""SQL helper functions"""

from pathlib import Path
import pandas as pd

def query(filepath, conn) -> pd.DataFrame:
    """Load SQL query from .sql file

    Args:
        filename (Path): SQL file location
        conn (Engine): SQLAlchemy engine or connection str to connect with

    Returns:
        Pandas DataFrame from the pandas.read_sql_query function running the
        given sql query.
    """
    # Convert filepath to Path if passed as string
    if isinstance(filepath, str):
        filepath = Path(filepath)

    with filepath.open(mode='r') as file:
        query = file.read()
    
    return pd.read_sql_query(query, conn)
