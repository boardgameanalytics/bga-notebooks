"""Helper function for data wrangling"""
import pandas as pd
from category_encoders import OneHotEncoder


# Helper function for encoding game classifications
def encode_class(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Encode game classifications with OHE and groupby game

    Args:
        df (DataFrame): Relational dataframe to encode
        name (str): Name of new columns

    Returns:
        Encoded dataframe
    """
    ohe = OneHotEncoder(cols=name, return_df=True)
    return ohe.fit_transform(df).groupby('game_id').agg(max)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe

    Args:
        df (DataFrame): df to clean

    Returns:
        Cleaned dataframe
    """
    # Cutoff releases before 1970
    df = df.loc[df['release_year'] > 1950]

    return df
