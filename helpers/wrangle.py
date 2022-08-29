"""Helper function for data wrangling"""
import numpy as np
import pandas as pd
from category_encoders import OneHotEncoder


NEXT_YEAR = 2023

def clean_data(df, threshold: int=None):
    """Clean dataset and add some composite features"""
    # Drop all releases prior to threshold, and any with a future release_year
    if threshold:
        df = df.loc[df.release_year > threshold]
    df = df.loc[df.release_year < NEXT_YEAR]
    
    # Drop NA equivalent values for release year and weight
    df = df.loc[df.release_year != 0]
    df = df.loc[df.weight != 0]
    
    # Remove extreme outliers
    df = df.loc[df.max_players < 200]
    df = df.loc[df.max_playtime < 1000]

    # Set booleans as int
    df.kickstarter = df.kickstarter.astype(int)
    
    return df


def add_composite_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered features to dataframe

    Args:
        df (pd.DataFrame): DataFrame to feature engineer

    Returns:
        DataFrame with engineered features
    """
    
    # Need to remove 'future' entries to prevent div/0 errors
    df = df.loc[df.release_year < NEXT_YEAR].copy()
    
    # Copies per year (since release) metric
    # Calculate age of game as 'next year' minus release year, so that games
    # just released in the current calendar year are counted as being 1 year
    # old and avoiding division by 0
    df['copies_per_year'] = (df.owned_copies /
                             (NEXT_YEAR - df.release_year)).astype(int)

    # Calculate the unadjusted popularity of a game
    # Since the bayes_rating is pulling the ratings to 5.5 from either
    # direction, we can assume that anything with a higher rating is viewed
    # positively, and anything lower negatively! Multiply that by the
    # total_ratings for a magnitude, and it appears we have a pretty good
    # metric for how positively or negatively the game is generally viewed!
    df['popularity'] = ((df.bayes_rating - 5.5) * df.total_ratings)

    def adjust_pop(n):
        """Adjust the popularity metric to a smaller scale using the natural log"""
        # Add 1 to the absolute value to keep all resulting numbers positive,
        # with a lower bound of 0
        ap = np.log(np.abs(n) + 1)
        
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
    mechanic = mechanic.lower()
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