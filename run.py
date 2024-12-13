import pandas as pd
import re
import matplotlib.pyplot as plt
import os
from library import *

#Get numeric choice
def get_choice(options, prompt):
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#re for find pattern
date_pattern = re.compile(r'(date|year)', re.IGNORECASE)

#Enter to the program
print("Data correlation tool!")

# Load data
path1 = input("Enter the path to dataset 1: ")
path2 = input("Enter the path to dataset 2: ")
# df1 = pd.read_csv(path1)
# df2 = pd.read_csv(path2)
df1 = pd.read_csv(path1, encoding="ISO-8859-1")
df2 = pd.read_csv(path2, encoding="ISO-8859-1")

# Rename columns
df1.columns = change_column_header(df1.columns,date_pattern)
df2.columns = change_column_header(df2.columns,date_pattern)

# Check date and format to YYYY
df1 = check_format_date_column(df1)
df2 = check_format_date_column(df2)
print(df1.head())
print(df2.head())

#Choose the column Dataset 1
print("\nChoose the column to analyze in Dataset 1:")
attribute1 = get_choice(df1.columns, "Columns in Dataset 1:")
print("attribute1",attribute1)

#Choose the column Dataset 2
print("\nChoose the column to analyze in Dataset 2:")
attribute2 = get_choice(df2.columns, "Columns in Dataset 2:")
print("attribute2",attribute2)

# assign value if string data in colomn
value1 = attribute1
value2 = attribute2

# operations
methods = ["Count string data", "Average for numerical", "Sum for numerical", "Count for numerical"]
operation = get_choice(methods, "Choose an operation dataset1:")
df1_appl = None

# Apply function to df1
if operation == "Count string data":
    value1 = input(f"Enter the string to count {attribute1}: ")
    df1_appl = count_string_data(df1, "Year/Date", attribute1, value1)
elif operation == "Average for numerical":
    df1_appl = calculate_avg(df1, attribute1)
elif operation == "Sum for numerical":
    df1_appl = calculate_sum(df1, attribute1)
elif operation == "Count for numerical":
    df1_appl = calculate_count(df1, attribute1)

print(df1_appl)

# Apply function to df2
operation = get_choice(methods, "Choose an operation dataset2:")
df2_appl = None
if operation == "Count string data":
    value2 = input(f"Enter the string to count {attribute2}: ")
    df2_appl = count_string_data(df2, "Year/Date", attribute2, value2)
elif operation == "Average for numerical":
    df2_appl = calculate_avg(df2, attribute2)
elif operation == "Sum for numerical":
    df2_appl = calculate_sum(df2, attribute2)
elif operation == "Count for numerical":
    df2_appl = calculate_count(df2, attribute2)

print(df2_appl)
#merge dataframes
merged_df = pd.merge(df1_appl, df2_appl, on="Year/Date", how="outer")
print(merged_df)

#if by applying string value to change the column name and iteract in merged_df
attribute1 = value1
attribute2 = value2

merged_df.fillna(0, inplace=True)

print("\nMerged DataFrame:")
print(merged_df)

# filtering data to get specific data frame
min_year_df1 = merged_df[merged_df[attribute1] != 0]["Year/Date"].min()
max_year_df1 = merged_df[merged_df[attribute1] != 0]['Year/Date'].max()
min_year_df2 = merged_df[merged_df[attribute2] != 0]["Year/Date"].min()
max_year_df2 = merged_df[merged_df[attribute2] != 0]["Year/Date"].max()

#definition min and max year in df
min_year = max(min_year_df1,min_year_df2)
max_year = max(max_year_df1,max_year_df2)

#filter
filtered_df = merged_df[(merged_df["Year/Date"] >= min_year) & (merged_df["Year/Date"] <= max_year)]

print(f"\nFiltered DataFrame (Years {min_year}-{max_year}):")
print(filtered_df)

# correlation
correlation_coefficient = filtered_df[attribute1].corr(filtered_df[attribute2])

# plotting
print(f"\nCorrelation coefficient: {correlation_coefficient}")
print(corr_conclusions(correlation_coefficient))
plotting(filtered_df, attribute1, attribute2, "blue", "red", correlation_coefficient)