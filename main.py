import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import seaborn as sns


def date_to_year_format(df, date_column):
    # df[date_column] = pd.to_datetime(df[date_column], format='%Y', errors='coerce')

    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    df[date_column] = df[date_column].dt.year
    return df


# check if 'Year/Date' column  convert it to year format
def check_format_date_column(df):
    df["Year/Date"] = df["Year/Date"].astype(str)
    if "Year/Date" in df.columns:
        df = date_to_year_format(df, "Year/Date")
    return df


date_patterns = re.compile(r"(date|year)", re.IGNORECASE)


def change_column_header(colomns):
    changed = []
    for item in colomns:
        if date_patterns.search(item) and "Year/Date" not in changed:
            changed.append("Year/Date")
            # break
        else:
            changed.append(item)
    return changed


# Read two datasets
dataset_1 = pd.read_csv(
    "./Datasets_CU/state_crime.csv",
)
dataset_2 = pd.read_csv(
    "./datasets_CU_/MVA_Vehicle_Sales_Counts_by_Month_for_Calendar_Year_2002_through_December_2023.csv",
)

dataset_1 = dataset_1.drop(
    [
        "State",
        # "Data.Population",
        # "Data.Rates.Property.All",
        # "Data.Rates.Property.Burglary",
        # "Data.Rates.Property.Larceny",
        # "Data.Rates.Property.Motor",
        # "Data.Rates.Violent.All",
        # "Data.Rates.Violent.Assault",
        "Data.Rates.Violent.Murder",
        "Data.Rates.Violent.Rape",
        "Data.Rates.Violent.Robbery",
        "Data.Totals.Property.All",
        "Data.Totals.Property.Burglary",
        "Data.Totals.Property.Larceny",
        "Data.Totals.Property.Motor",
        "Data.Totals.Violent.All",
        "Data.Totals.Violent.Assault",
        "Data.Totals.Violent.Murder",
        "Data.Totals.Violent.Rape",
        "Data.Totals.Violent.Robbery",
    ],
    axis=1,
)
dataset_2 = dataset_2.drop(["Month "], axis=1)

# create two dataframe for both datasets
df1 = pd.DataFrame(dataset_1)
df2 = pd.DataFrame(dataset_2)

df1.dropna(inplace=True)
df2.dropna(inplace=True)
# Rename columns
df1.columns = change_column_header(df1.columns)
df2.columns = change_column_header(df2.columns)

# Check date and format to YYYY
df1 = check_format_date_column(df1)
df2 = check_format_date_column(df2)

df1.rename(columns={"Data.Rates.Property.Burglary": "Burglary_Rate"}, inplace=True)
df2.rename(columns={"Total Sales Used": "Total_Sales_Used_Car"}, inplace=True)

# df1 = df1[df1["Year/Date"] >= 2009]
# df1 = df1[df1["Year/Date"] <= 2018]

# df2 = df2[df2["Year/Date"] >= 2009]
# df2 = df2[df2["Year/Date"] <= 2018]

merged_df = df1.merge(df2, "inner")
merged_df = merged_df.groupby("Year/Date").mean()
correlation_matrix = merged_df.corr()

sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()
