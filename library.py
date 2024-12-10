# We can include functions and methods here...
# They could be resuable for other dataset, might be useful...

import os
import pandas as pd

path_to_crime_csv = os.path.join("Datasets_Crime", "state_crime.csv")


def load_crime_df(include_states=False):
    """
    Returns the state_crime data as a DataFrame.

    Args:
        include_states: Whether to include states or only return US totals.

    Returns:
        DataFrame: The loaded crime dataset.
    """
    df = pd.read_csv(path_to_crime_csv)

    # Drop states and only include aggregated data if not otherwise specified
    if not include_states:
        df = df[df["State"].str.contains("United States")].reset_index(drop=True)
    else:
        df = df[~df["State"].str.contains("United States")].reset_index(drop=True)

    return df


print(load_crime_df(include_states=True).groupby("Year")["Data.Population"].sum())
