"""Pytests for sql.py module"""

import os
import sqlite3
import pandas as pd
from helpers.sql import query

def _setup(db_filepath: str, sql_filepath: str):
    '''Create SQL query file
    Args:
        db_filepath (str): Location of database file
        sql_filepath (str): Location of query file
    '''
    query = 'SELECT * FROM test_table LIMIT 2;'
    
    with open(sql_filepath, 'w') as file:
        file.write(query)
    
    with sqlite3.connect(db_filepath) as conn:
        pd.DataFrame({
            'id': [0, 1, 2, 3, 4],
            'titles': ['title1', 't2', 't3', 't4', 't5']
            }).to_sql('test_table', conn, index=None)
   

def _teardown(db_file: str, sql_file: str) -> None:
    '''cleanup test files
    Args:
        db_file (str): location of db file
        sql_file (str): location of sql query file
    '''
    os.remove(db_file)
    os.remove(sql_file)


def test_sql_query() -> None:
    """Test for sql_query"""
    # Setup
    db_filepath = 'test_db.sqlite'
    sql_filepath = 'test_query.sql'
    _setup(db_filepath, sql_filepath)
    
    # Test
    with sqlite3.connect(db_filepath) as conn:
        out_df = query(sql_filepath, conn)
    
    # Verify
    assert isinstance(out_df, pd.DataFrame), 'Did not return DataFrame'
    assert out_df.shape == (2, 2), 'Incorrectly shaped DataFrame returned'
    
    # Teardown
    _teardown(db_filepath, sql_filepath)
