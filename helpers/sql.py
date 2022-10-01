"""SQL helper functions"""

from pathlib import Path
import pandas as pd
from sqlalchemy.engine import Engine


def query(filepath: Path, conn: Engine) -> pd.DataFrame:
    """Load SQL query from .sql file

    Args:
        filepath (Path): SQL file location
        conn (Engine): SQLAlchemy engine or connection str to connect with

    Returns:
        Pandas DataFrame from the pandas.read_sql_query function running the
        given sql query.
    """
    # Convert filepath to Path if passed as string
    if isinstance(filepath, str):
        filepath = Path(filepath)

    with filepath.open(mode='r') as file:
        sql_query = file.read()
    
    return pd.read_sql_query(sql_query, conn)
