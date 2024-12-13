from library import load_crime_df
import pandas as pd
import re
import matplotlib.pyplot as plt
import os

path_to_climate_change = os.path.join("Datasets_Alexi", "ClimateChange.csv")
path_to_temperature_change = os.path.join("Datasets_Alexi", "GlobalLandTemperatures.csv")
path_to_pollution_set = os.path.join("Datasets_Alexi", "Pollution.csv")

# Read csv files
pollutionDf = pd.read_csv(path_to_pollution_set) 
crimeDf = load_crime_df(False)
climateDf = pd.read_csv(path_to_climate_change)
temperatureDf = pd.read_csv(path_to_temperature_change)
climateDf = climateDf.rename(columns={'Year': 'dt','Avg Temperature (°C)': 'AverageTemperature'})

# Just conversion
def conversion_datetime_to_year(df, column):
    df = df.copy()
    df[column] = pd.to_datetime(df[column], format='%Y-%m-%d')
    df = df[df[column] >= '1960-01-01']
    df[column] = df[column].dt.year
    df.dropna(axis=0, how='any', inplace=True)
    return df

# get mean temp
def get_mean_of_dataset(df):
    df = df.groupby('dt').mean()
    return df

# Gets Total Violent Rates, Chrimes 
def get_violent_rates_and_total(df):
    df = df[['Year', 'Data.Rates.Violent.All', 'Data.Totals.Violent.All', 'Data.Totals.Property.Burglary']]
    df = df.rename(columns={'Data.Rates.Violent.All': 'Violent Crime Rate', 
                        'Data.Totals.Violent.All': 'Total Violent Crimes',
                        'Data.Totals.Property.Burglary': 'Total Burglaries'})
    return df

# max year of data from crimes is 2019
def set_max_year(df):
    df = df[(df['dt'] <= 2019)]
    return df

def line_graph(df, plotType, title, xlabel, ylabel, columnOne="", columnTwo="", graphGrid=True, correlation=0):
    # Line plot and Scatter Plot
    df[columnOne].plot(figsize=(10,5), marker='o', linestyle='-', color='b')
    plt.title(title) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel) 
    plt.grid(graphGrid)
    plt.show()

def scatter_graph(df):
    fig, ax1 = plt.subplots()
    # Scatter plot for Total Violent Crimes
    ax1.scatter(df["Year"], df["Total Violent Crimes"], color='red', label='Total Violent Crimes')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Total Violent Crimes", color="red")
    ax1.tick_params(axis='y', labelcolor='red')

    # Create a second y-axis for Temperature
    ax2 = ax1.twinx()
    ax2.scatter(df["Year"], df["Temperature"], color='blue', label='Temperature')
    ax2.set_ylabel("Temperature (°F)", color="blue")
    ax2.tick_params(axis='y', labelcolor='blue')

    # Title and legend
    plt.title("Impact of Temperature on Total Violent Crimes")
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.85))

    # Save or show the plot
    plt.savefig("dual_axis_scatter.png", dpi=300, bbox_inches='tight')
    plt.show()

def dual_axis_graph(df, title, xlabel, ylabel, col1, col2, col3, location="upper left", measurement=""):
    fig, axis1 = plt.subplots()

    # y-axis 1
    axis1.patch.set_facecolor('#f0f0f0')
    axis1.patch.set_alpha(0.8)
    axis1.set_xlabel(ylabel, fontsize=18)
    axis1.set_ylabel(xlabel, fontsize=18)
    line1, = axis1.plot(df[col1], df[col2], '-', color='blue', label=xlabel, linewidth=0.8)
    axis1.spines['top'].set_color('000000') 
    axis1.spines['bottom'].set_color('000000')
    axis1.spines['left'].set_color('000000')
    axis1.spines['right'].set_color('000000')

    # y-axis 2
    axis2 = axis1.twinx()
    axis2.set_ylabel(f'{col3} {measurement}', color='red', fontsize=18)
    line2, = axis2.plot(df[col1], df[col3], '-', color='red', label=f'{col3} {measurement}', linewidth=0.8)
    axis2.tick_params(axis='y', labelcolor='red')

    # Calculate correlation
    correlation = df[col2].corr(df[col3])

    # title
    plt.title(title + f'\n r = {correlation:.2f}', fontsize=20)

    # legends
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    axis1.legend(lines, labels, loc=location)

    # layout options
    output_dir = 'correlation-graphs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    path = os.path.join(output_dir, f"{title}.png")
    fig.tight_layout()  # So that no clipping occurs
    plt.savefig(path, dpi=400, bbox_inches='tight')

    plt.show()

# dataframes filtering/sorting
climateDf = climateDf[['dt', 'AverageTemperature', 'Rainfall (mm)', 'Extreme Weather Events']]
temperatureDf = conversion_datetime_to_year(temperatureDf, 'dt')
temperatureDf = temperatureDf[['dt', 'AverageTemperature']]
temperatureDf = get_mean_of_dataset(temperatureDf)
temperatureDf.reset_index(inplace=True)
weatherDf = get_mean_of_dataset(climateDf)
weatherDf.reset_index(inplace=True)
weatherDf = weatherDf.rename(columns={'dt': 'Year'})
climateDf = climateDf[(climateDf['dt'] >= 2014) & (climateDf['dt'] <= 2019)]
climateDf = get_mean_of_dataset(climateDf)
climateDf.reset_index(inplace=True)
climateDf = pd.concat([temperatureDf, climateDf[['dt','AverageTemperature']]], ignore_index=True)
climateDf = climateDf.rename(columns={'dt': 'Year', 'AverageTemperature': 'Temperature'})
crimeDf = get_violent_rates_and_total(crimeDf)
crimeAndTemp = climateDf.merge(crimeDf, on='Year', how='inner')
weatherDf = weatherDf.merge(crimeDf, on='Year', how='inner')

# df, title, xlabel, ylabel, col1, col2, col3
dual_axis_graph(crimeAndTemp, "Impact of Temperature on Total Violent Crimes", 
                'Temperature (°C)', 'Years', 'Year',
                'Temperature', 'Total Violent Crimes')

dual_axis_graph(weatherDf, "Rainfall Trends and Their Effect on Violent Crime Rates", 
                'Rainfall (mm)', 'Years', 'Year',
                'Rainfall (mm)', 'Violent Crime Rate', location='upper center', measurement='(per 100,000 people)')

dual_axis_graph(weatherDf, "Burglary Trends During Extreme Weather Events", 
                'Extreme Weather Events', 'Years', 'Year',
                'Extreme Weather Events', 'Total Burglaries', location='lower left')