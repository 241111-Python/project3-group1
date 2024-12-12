'''
Plan:
1. retrieve the data from the csv files(json)
2. change headers and data to one formatt(YYYY)
3. filter data by choosen attributes
4. grouping data by common headers, sort data asc, desc
5. calculate avg of values or count()
6. find correlation fo each year
7. print correlation in table format
8. plotting correlation

'''
import pandas as pd
import re
import matplotlib.pyplot as plt

#load csv
df1 = pd.read_csv('C:/Users/15717/Desktop/project3/data/data.csv')
df2 = pd.read_csv('C:/Users/15717/Desktop/project3/data/pop_and_net_migration.csv')

#re for find pattern
date_patterns = re.compile(r'(date|year)', re.IGNORECASE)

# rename date|year columns to 'Year/Date'
def change_column_header(cols):
    changed = []
    for item in cols:
        if date_patterns.search(item):
            changed.append('Year/Date') 
        else:
            changed.append(item)
    return changed


df1.columns = change_column_header(df1.columns)
df2.columns = change_column_header(df2.columns)


def date_to_year_format(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column], format='%Y', errors='coerce')
    df[date_column] = df[date_column].dt.year
    return df

def check_format_date_column(df):
    if 'Year/Date' in df.columns:
        df = date_to_year_format(df, 'Year/Date')
    return df

df1 = check_format_date_column(df1)
df2 = check_format_date_column(df2)

# print(df1['Year/Date'].head())  
# print(df2['Year/Date'].head())

# calculate count, grouped by 'Year/Date'
def calculate_count(df, attribute):
    if attribute in df.columns:
        df_grouped = df.groupby('Year/Date')[attribute].count().reset_index()
        return df_grouped
    else:
        print('No attribute in dataframe', attribute)

# calculate average, grouped by 'Year/Date'
def calculate_avg(df, attribute):
    if attribute in df.columns:
        df_grouped = df.groupby('Year/Date')[attribute].mean().reset_index()
        return df_grouped
    else:
        print('No attribute in dataframe', attribute)


def count_string_data(df, group_col, value_col, string):
    if df[value_col].iloc[0].startswith("[") and df[value_col].iloc[0].endswith("]"):  
        df[value_col] = df[value_col].apply(eval)  
        df_filter = df[df[value_col].apply(lambda value: string in value)]
    else:
        df_filter = df[df[value_col] == string]

    
    grouped_by = df_filter.groupby(group_col).size().reset_index(name=string)
    return grouped_by

# print(count_string_data(df1, "Year/Date", "Stars", "Brad Pitt"))
# print(calculate_avg(df2, 'net_migration'))



df1_to_merge = count_string_data(df1, "Year/Date", "Stars", "Brad Pitt")
df2_to_merge = calculate_avg(df2, 'net_migration')


merged_df = pd.merge(df1_to_merge, df2_to_merge, on="Year/Date", how="outer")
#filling to 0
merged_df.fillna(0, inplace=True)



correlation_coefficient = merged_df["Brad Pitt"].corr(merged_df["net_migration"])
# correlation2 = merged_df[['Brad Pitt', 'net_migration']].corr()
# print(correlation)

print(f"Correlation coefficient: {correlation_coefficient}")


#Conclusions based on correlation coefficient

conclusion = ''

if correlation_coefficient > 0.7:
        conclusion = "Strong positive correlation."
elif 0.3 <= correlation_coefficient <= 0.7:
        conclusion = "Moderate positive correlation."
elif 0 <= correlation_coefficient < 0.3:
        conclusion = "Weak positive correlation."
elif -0.3 <= correlation_coefficient < 0:
        conclusion = "Weak negative correlation."
elif -0.7 <= correlation_coefficient < -0.3:
        conclusion = "Moderate negative correlation."
elif correlation_coefficient < -0.7:
        conclusion = "Strong negative correlation."
else:
        conclusion = "No discernible correlation."

print(f"Conclusion: {conclusion}")

def plotting(merged_df, attr1, attr2,color1,color2):
    years = merged_df['Year/Date']
    attribute1 = merged_df[attr1]
    attribute2 = merged_df[attr2]
    label1 = attr1.replace('_', '').capitalize()
    label2 = attr2.replace('_', '').capitalize()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('Year')
    ax1.set_ylabel(label1, color=color1)
    ax1.plot(years, attribute1, label=label1, color=color1, marker='o', linestyle='-')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2, color=color2)
    ax2.plot(years, attribute2, label=label2, color=color2,marker='o', linestyle='-')
    ax2.tick_params(axis='y', labelcolor=color2)
    fig.suptitle(f'{label1} vs. {label2}')
    fig.tight_layout() 

    plt.savefig(f'{attr1}_vs_{attr2}.png')
    plt.show()
    
plotting(merged_df,'Brad Pitt','net_migration','green','red')