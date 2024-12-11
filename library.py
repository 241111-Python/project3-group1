# We can include functions and methods here...
# They could be resuable for other dataset, might be useful...

import os
import pandas as pd
import matplotlib.pyplot as plt
import os
path_to_crime_csv = os.path.join("Datasets_Crime", "state_crime.csv")


# To-Do: Can handle any necessary pre-processing here
# or add arguments to return only crime rates or only counts, if useful
def load_crime_df():
    df = pd.read_csv(path_to_crime_csv)

    return df

# date_patterns = re.compile(r'(date|year)', re.IGNORECASE)

def change_column_header(colomns,date_patterns):
    changed = []
    for item in colomns:
        if date_patterns.search(item) and 'Year/Date' not in changed:
            changed.append('Year/Date') 
            # break  
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