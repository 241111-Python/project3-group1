import pandas as pd
import re
import matplotlib.pyplot as plt
import os


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
date_patterns = re.compile(r'(date|year)', re.IGNORECASE)

# rename date|year columns to 'Year/Date'
def change_column_header(colomns):
    changed = []
    for item in colomns:
        if date_patterns.search(item):
            changed.append('Year/Date') 
        else:
            changed.append(item)
    return changed

# convert date to year format
def date_to_year_format(df, date_column):
    # df[date_column] = pd.to_datetime(df[date_column], format='%Y', errors='coerce')
    

    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    df[date_column] = df[date_column].dt.year
    return df

# check if 'Year/Date' column  convert it to year format
def check_format_date_column(df):
    df['Year/Date'] = df['Year/Date'].astype(str)
    if 'Year/Date' in df.columns:
        df = date_to_year_format(df, 'Year/Date')
    return df
# calculate average, grouped by group_col='Year/Date' in call, can be used for other
def count_string_data(df, group_col, value_col, string):
    if df[value_col].iloc[0].startswith("[") and df[value_col].iloc[0].endswith("]"):  
        df[value_col] = df[value_col].apply(eval)
        df_filter = df[df[value_col].apply(lambda value: string in value)]
    else:
        df_filter = df[df[value_col] == string]
    grouped_by = df_filter.groupby(group_col).size().reset_index(name=string)
    return grouped_by

# calculate average, grouped by 'Year/Date'
def calculate_avg(df, attribute):
    return df.groupby('Year/Date')[attribute].mean().reset_index()

# calculate sum, grouped by 'Year/Date'
def calculate_sum(df, attribute):
    return df.groupby('Year/Date')[attribute].sum().reset_index()

# calculate count, grouped by 'Year/Date'
def calculate_count(df, attribute):
    return df.groupby('Year/Date')[attribute].count().reset_index()

# conclusion correlation between two attributes
def corr_conclusions(correlation_coefficient):
    if correlation_coefficient > 0.7:
        return "Strong positive correlation."
    elif 0.3 <= correlation_coefficient <= 0.7:
        return "Moderate positive correlation."
    elif 0 <= correlation_coefficient < 0.3:
        return "Weak positive correlation."
    elif -0.3 <= correlation_coefficient < 0:
        return "Weak negative correlation."
    elif -0.7 <= correlation_coefficient < -0.3:
        return "Moderate negative correlation."
    elif correlation_coefficient < -0.7:
        return "Strong negative correlation."
    else:
        return "No discernible correlation."

# Plotting
def plotting(merged_df, attr1, attr2, color1, color2, correlation_coefficient):
    years = merged_df['Year/Date']
    attribute1 = merged_df[attr1]
    attribute2 = merged_df[attr2]
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('Year')
    ax1.set_ylabel(attr1, color=color1)
    ax1.plot(years, attribute1, label=attr1, color=color1, marker='o', linestyle='-')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    ax2.set_ylabel(attr2, color=color2)
    ax2.plot(years, attribute2, label=attr2, color=color2, marker='o', linestyle='-')
    ax2.tick_params(axis='y', labelcolor=color2)
    fig.suptitle(f'{attr1} vs. {attr2}\n{corr_conclusions(correlation_coefficient)}')
    # plt.savefig(f'{attr1}_vs_{attr2}.png')
    output_dir = 'correlation-graphs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f'{attr1}_vs_{attr2}.png')
    plt.savefig(file_path)
    plt.show()

# First message
print("Data correlation tool!")

# Load data
path1 = input("Enter the path to dataset 1: ")
path2 = input("Enter the path to dataset 2: ")
df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

# Rename columns
df1.columns = change_column_header(df1.columns)
df2.columns = change_column_header(df2.columns)

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
print(merged_df)
# correlation
correlation_coefficient = merged_df[attribute1].corr(merged_df[attribute2])

# plotting
print(f"\nCorrelation coefficient: {correlation_coefficient}")
print(corr_conclusions(correlation_coefficient))
plotting(merged_df, attribute1, attribute2, 'blue', 'red', correlation_coefficient)
