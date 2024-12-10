import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Datasets_Crime/state_crime.csv", usecols=["Year", "Data.Population", "Data.Rates.Property.All", "Data.Rates.Violent.All"])

# Merge with the election dataset
df2 = pd.read_csv("Datasets_DF/US_Election_dataset_v1.csv")
merged = df.merge(df2, how="left", on="Year")
merged.rename(columns=lambda x: x.strip(), inplace=True)

merged['Election_Year'] = merged['Year'] % 4 == 0

merged['Winning_Party_Numerical'] = merged['Winning_Party'].map({' D': 1, ' R': 0})

print(merged['Winning_Party'].unique())
print(merged.head(15))

corr = merged[['Data.Rates.Violent.All', 'Winning_Party_Numerical', ]].corr()
print(corr)

democratic = merged[merged['Winning_Party_Numerical'] == 1]
republican = merged[merged['Winning_Party_Numerical'] == 0]

data_to_plot = [democratic['Data.Rates.Violent.All'], republican['Data.Rates.Violent.All']]

# Create the boxplot
# plt.boxplot(data_to_plot, labels=['Democratic', 'Republican'])
# plt.title('Violent Crime Rates by Winning Party')
# plt.ylabel('Violent Crime Rates')
# plt.xlabel('Winning_Party')
# plt.show()

plt.figure(figsize=(10, 6))  # Adjust figure size as needed

plt.plot(x='Year', y='Data.Rates.Violent.All', kind='line', label='Democratic', color='blue')
plt.plot(x='Year', y='Data.Rates.Violent.All', kind='line', label='Republican', color='red')

plt.title('Violent Crime Rates by Winning Party Over Time')
plt.xlabel('Year')
plt.ylabel('Violent Crime Rates')
plt.legend()  
plt.grid(True) 
plt.show()
