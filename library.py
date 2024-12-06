# We can include functions and methods here...
# They could be resuable for other dataset, might be useful...

import os
import pandas as pd

path_to_crime_csv = os.path.join("Datasets_Crime", "state_crime.csv")


# To-Do: Can handle any necessary pre-processing here
# or add arguments to return only crime rates or only counts, if useful
def load_crime_df():
    df = pd.read_csv(path_to_crime_csv)

    return df
