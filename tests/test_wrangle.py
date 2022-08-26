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
