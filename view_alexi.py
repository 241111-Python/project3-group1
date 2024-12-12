from library import load_crime_df
import pandas as pd
import re
import matplotlib.pyplot as plt
import os

path_to_climate_change = os.path.join("Datasets_Alexi", "ClimateChange.csv")
path_to_temperature_change = os.path.join("Datasets_Alexi", "GlobalLandTemperatures.csv")

crimeDf = load_crime_df(False)
climateDf = pd.read_csv(path_to_climate_change)
temperatureDf = pd.read_csv(path_to_temperature_change)
climateDf = climateDf.rename(columns={'Year': 'dt','Avg Temperature (°C)': 'AverageTemperature'})

def conversion_datetime_to_year(df):
    df = df.copy()
    df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')
    df = df[df['dt'] >= '1960-01-01']
    df['dt'] = df['dt'].dt.year
    df.dropna(axis=0, how='any', inplace=True)
    return df

def get_temperature_from_datasets(df):
    df = df.groupby('dt')['AverageTemperature'].mean().reset_index()
    return df

def get_violent_rates_and_total(df):
    df = df[['Year', 'Data.Rates.Violent.All', 'Data.Totals.Violent.All']]
    df = df.rename(columns={'Data.Rates.Violent.All': 'Violent Crime Rate', 
                        'Data.Totals.Violent.All': 'Total Violent Crimes'})
    return df

def plot_graph(df, plotType, title, xlabel, ylabel, columnOne="", columnTwo="", graphGrid=True, correlation=0):
    # df.set_index('Year',  inplace=True)
    if plotType == 'l':
        df[columnOne].plot(figsize=(10,5), marker='o', linestyle='-', color='b')
    elif plotType == 's':
        plt.scatter(df[columnOne], df[columnTwo], color='b', marker='o')

    plt.title(title) 
    plt.xlabel(xlabel)
    plt.ylabel(ylabel) 
    plt.grid(graphGrid)
    plt.show()

# formats to only grab year 
temperatureDf = conversion_datetime_to_year(temperatureDf)
temperatureDf = get_temperature_from_datasets(temperatureDf)
climateDf = climateDf[(climateDf['dt'] >= 2014) & (climateDf['dt'] <= 2019)]
climateDf = get_temperature_from_datasets(climateDf)
climateCombinedDf = pd.concat([temperatureDf, climateDf], ignore_index=True)
climateCombinedDf = climateCombinedDf.rename(columns={'dt': 'Year', 'AverageTemperature': 'Temperature'})
crimeDf = get_violent_rates_and_total(crimeDf)
crimeAndTemp =  pd.concat([climateCombinedDf, crimeDf], axis=1)

# line_plot(climateCombinedDf, 'Temperature over Time', 'Temperature','Year')
corrTempCrimes = crimeAndTemp['Temperature'].corr(crimeAndTemp['Violent Crime Rate'])

print(crimeAndTemp)
print(corrTempCrimes)

# df, plotType, title, xlabel, ylabel, columnOne="", columnTwo="", graphGrid=True, correlation=0
plot_graph(crimeAndTemp, 's', 'Impact of Temperature on Total Violent Crimes',
         'Average Temperature (°C)','Total Violent Crimes', columnOne='Temperature', columnTwo='Violent Crime Rate',
         correlation=corrTempCrimes )

