"""Helper function for data wrangling"""
import pandas as pd
from category_encoders import OneHotEncoder


def wrangle(df):
    """Clean dataset and add some composite features"""
    release_yr_threshold = 1950
    next_year = 2023
    # Drop all releases prior to threshold, and any with a future release_year
    df = df.loc[(df.release_year > release_yr_threshold) &
                (df.release_year < next_year)]
    
    # Set booleans as int
    df.kickstarter = df.kickstarter.astype(int)
    
    # Copies per year (since release) metric
    # Calculate age of game as 'next year' minus release year, so that games
    # just released in the current calendar year are counted as being 1 year
    # old and avoiding division by 0
    df['copies_per_year'] = (df.owned_copies /
                             (next_year - df.release_year)).astype(int)

    return df


def encode_class(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Encode game classifications with OHE and groupby game

    Args:
        df (DataFrame): Relational dataframe to encode
        name (str): Name of new columns

    Returns:
        Encoded dataframe
    """
    ohe = OneHotEncoder(cols=name, return_df=True, use_cat_names=True)
    return ohe.fit_transform(df).groupby(df.index.values).agg(max)


def reduce_mechanics(mechanic: str) -> str:
    """Combine similiar mechanics to reduce total number of mechanic types"""
    if 'action' in mechanic:
        return 'action'
    elif 'auction' in mechanic:
        return 'auction'
    elif 'worker-placement' in mechanic:
        return 'worker-placement'
    elif 'turn-order' in mechanic:
        return 'turn-order'
    else:
        return mechanic