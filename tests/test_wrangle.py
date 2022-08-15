"""Pytests for wrangle.py"""

import pandas as pd
from helpers.wrangle import encode_class, clean_data

def test_encode_class() -> None:
    """Test for encode_class()
    Input:
        Dataframe with game_id column, name to label to columns with
    Expected output:
        All columns (except game_id) are OHE and grouped by game_id
    """
    in_df = pd.DataFrame({
        'game_id': [0, 1, 1, 1, 2, 2],
        'mechanic': ['dice', 'auction', 'hand-management', 'bluffing', 'hand-management', 'dice']
    })
    out_df = encode_class(in_df, 'mechanic')
    assert isinstance(out_df, pd.DataFrame), 'Did not return a pandas DataFrame'
    assert out_df.shape == (3, 4), 'Incorrectly shaped DataFrame returned'


def test_clean_data() -> None:
    """Test for clean_data()
    Input:
        DataFrame with (int) 'release_year' column
    Expected output:
        Given DataFrame with all release_year's prior to 1951 removed.
    """
    in_df = pd.DataFrame({
        'id': [0, 1, 2, 3, 4, 5, 6],
        'title': ['title1', 'title2', 'title3', 'title4', 'unknown', 'title6', 'ancient'],
        'release_year': [2020, 2002, 1969, 1950, 0, 1458, -2300]
    })
    out_df = clean_data(in_df)
    assert isinstance(out_df, pd.DataFrame), 'Did not return a pandas DataFrame'
    assert out_df.shape == (3, 3), 'Incorrectly shaped DataFrame returned'
    assert (out_df['release_year'] <= 1950).sum() == 0, 'Returned pre-1951 game'
