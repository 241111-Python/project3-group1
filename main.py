import pandas as pd
import matplotlib.pyplot as plt
import library

# some input statements we could use
# if not necessary, comments them out
path_1 = input("Enter the path to dataset 1: ")
path_2 = input("Enter the path to dataset 2: ")

index_col_1 = input("Enter the index name for dataset 1: ")
index_col_2 = input("Enter the index name for dataset 2: ")

# Read two datasets
dataset_1 = pd.read_csv(path_1, index_col=index_col_1)
dataset_2 = pd.read_csv(path_2, index_col=index_col_2)

# create two dataframe for both datasets
df_1 = pd.DataFrame(dataset_1)
df_2 = pd.DataFrame(dataset_2)

print(df_1)
print(df_2)

# This is a just a base code to get started. Change/modify to fit your datasets.
# Good luck!
