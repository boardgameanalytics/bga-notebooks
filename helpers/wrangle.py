"""Helper function for data wrangling"""
import numpy as np
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
    
    # Feature engineering
    df = add_composite_features(df)

    return df


def add_composite_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered features to dataframe

    Args:
        df (pd.DataFrame): DataFrame to feature engineer

    Returns:
        DataFrame with engineered features
    """
    next_year = 2023
    
    # Copies per year (since release) metric
    # Calculate age of game as 'next year' minus release year, so that games
    # just released in the current calendar year are counted as being 1 year
    # old and avoiding division by 0
    df['copies_per_year'] = (df.owned_copies /
                             (next_year - df.release_year)).astype(int)

    # Calculate the unadjusted popularity of a game
    # Since the bayes_rating is pulling the ratings to 5.5 from either
    # direction, we can assume that anything with a higher rating is viewed
    # positively, and anything lower negatively! Multiply that by the
    # total_ratings for a magnitude, and it appears we have a pretty good
    # metric for how positively or negatively the game is generally viewed!
    df['popularity'] = ((df.bayes_rating - 5.5) * df.total_ratings)

    # Adjust the popularity metric to a smaller scale using the natural log
    def adjust_pop(n):
        # Keep scale centered at zero, return 0 before taking log
        if n == 0:
            return 0
        # Multiply the absolute value to move all values above 1 to
        # keep results positive
        ap = np.log(np.abs(n) * 100)
        # Keep the sign of the unadjusted number
        if n < 0:
            ap *= -1
        return ap
    # Save the adjusted metric as a separate column
    df['popularity_adj'] = df.popularity.apply(adjust_pop)

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