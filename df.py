import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Datasets_Crime/state_crime.csv", usecols=["Year", "Data.Population", "Data.Rates.Property.All", "Data.Rates.Violent.All"])

# Merge with the election dataset
df2 = pd.read_csv("Datasets_DF/US_Election_dataset_v1.csv")
merged = df.merge(df2, how="left", on="Year")
merged.rename(columns=lambda x: x.strip(), inplace=True)

# Add a new column to identify election years (presidential election years)
merged['Election_Year'] = merged['Year'] % 4 == 0

# Print the updated DataFrame
print(merged[['Year', 'Election_Year']].head())

print(merged[['Data.Rates.Violent.All', 'Winning_Party']].isnull().sum())

# Plot the boxplot for violent crime rates by winning party
# sns.boxplot(data=merged, x='Winning_Party', y='Data.Rates.Violent.All')
# plt.title('Violent Crime Rates by Winning Party')
# plt.show()

# Separate data by party
democratic = merged[merged['Winning_Party'] == 'D']
republican = merged[merged['Winning_Party'] == 'R']

# Prepare data for boxplot
data_to_plot = [democratic['Data.Rates.Violent.All'], republican['Data.Rates.Violent.All']]

# Create the boxplot
plt.boxplot(data_to_plot, labels=['Democratic', 'Republican'])
plt.title('Violent Crime Rates by Winning Party')
plt.ylabel('Violent Crime Rates')
plt.xlabel('Winning_Party')
plt.show()
