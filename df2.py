import pandas as pd
from library import load_crime_df
import matplotlib.pyplot as plt
import seaborn as sn

df = load_crime_df(usecols=["State", "Year", "Data.Totals.Violent.All", "Data.Rates.Violent.All", "Data.Totals.Property.All", "Data.Rates.Property.All"])
df2 = pd.read_csv("Datasets_DF/US_Election_dataset_v1.csv")

#Merge and prep data
merged = df.merge(df2, how="left", on="Year")
merged.rename(columns=lambda x: x.strip(), inplace=True)
merged['Election_Year'] = merged['Year'] % 4 == 0
merged['Winning_Party'] = merged['Winning_Party'].map({'D': 1, 'R': 0})
print(merged)

democratic = merged[merged['Winning_Party'] == 1]
republican = merged[merged['Winning_Party'] == 0]

violent_data = [democratic['Data.Rates.Violent.All'], republican['Data.Rates.Violent.All']]
property_data = [democratic['Data.Rates.Property.All'], republican['Data.Rates.Violent.All']]

# Create the boxplots
plt.boxplot(violent_data, labels=['Democratic', 'Republican'])
plt.title('Violent Crime Rates by Winning Party')
plt.ylabel('Violent Crime Rate (per 100k perople)')
plt.xlabel('Winning Party')
plt.show()

plt.boxplot(property_data, labels=['Democratic', 'Republican'])
plt.title('Property Crime Rates by Winning Party')
plt.ylabel('Property Crime Rates (per 100k perople)')
plt.xlabel('Winning Party')
plt.show()

election_years = merged[merged['Election_Year'] == True]
election_results = election_years[['Year', 'Winning_Party']]


# Heatmaps for correlation matrices
corr = merged[['Data.Rates.Violent.All', 'Data.Rates.Property.All', 'Winning_Party']].corr()
print(corr)
plt.show()
dataplot = sn.heatmap(corr, cmap="YlGnBu", annot=True)
plt.show()

import seaborn as sn
import matplotlib.pyplot as plt

# Calculate correlation matrix
corr2 = merged[['Data.Rates.Violent.All', 'Data.Rates.Property.All', 'Election_Year', 'Winning_Party']].corr()

# Create heatmap
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
dataplot = sn.heatmap(
    corr2,
    cmap="YlGnBu",
    annot=True,
    fmt=".2f",
    cbar=False,
    xticklabels=corr2.columns,
    yticklabels=corr2.columns
)

# Rotate axis labels for better visibility
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)

# Display the plot
plt.title("Correlation Heatmap", fontsize=14)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))

# Plot the violent crime rates line
plt.plot(merged['Year'], merged['Data.Rates.Violent.All'], color='gray', alpha=0.5, label='Violent Crime Rates', linewidth=2)

# Separate the data by party
democratic_years = merged[merged['Winning_Party'] == 1]
republican_years = merged[merged['Winning_Party'] == 0]

# Add separate lines for Democratic and Republican years
plt.scatter(democratic_years['Year'], democratic_years['Data.Rates.Violent.All'], color='blue', label='Democratic', zorder=5)
plt.scatter(republican_years['Year'], republican_years['Data.Rates.Violent.All'], color='red', label='Republican', zorder=5)

# Highlight election years with a distinct marker
plt.scatter(election_years['Year'], election_years['Data.Rates.Violent.All'], color='black', label='Election Year', marker='o', edgecolor='yellow', zorder=6)

# Add labels, legend, and title
plt.title('Violent Crime Rates Over Time with Presidential Results')
plt.xlabel('Year')
plt.ylabel('Violent Crime Rate (per 100k perople)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

plt.figure(figsize=(10, 6))

# Plot the property crime rates line
plt.plot(merged['Year'], merged['Data.Rates.Property.All'], color='gray', alpha=0.5, label='Property Crime Rates', linewidth=2)

# Separate the data by party
democratic_years = merged[merged['Winning_Party'] == 1]
republican_years = merged[merged['Winning_Party'] == 0]

# Add separate points for Democratic and Republican years
plt.scatter(democratic_years['Year'], democratic_years['Data.Rates.Property.All'], color='blue', label='Democratic', zorder=5)
plt.scatter(republican_years['Year'], republican_years['Data.Rates.Property.All'], color='red', label='Republican', zorder=5)

# Highlight election years with a distinct marker
plt.scatter(election_years['Year'], election_years['Data.Rates.Property.All'], color='black', label='Election Year', marker='o', edgecolor='yellow', zorder=6)

# Add labels, legend, and title
plt.title('Property Crime Rates Over Time with Presidential Results')
plt.xlabel('Year')
plt.ylabel('Property Crime Rate (per 100k people)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()




