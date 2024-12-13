import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

# Load and preprocess data
df = pd.read_csv("Datasets_Crime/state_crime.csv", usecols=["State", "Year", "Data.Rates.Property.All", "Data.Rates.Violent.All"])
df = df[df["State"] == "United States"]
df2 = pd.read_csv("Datasets_DF/broadband-penetration-by-country.csv")
df2 = df2[df2["Code"] == "USA"]

# Merge and clean data
merged = df.merge(df2, how="inner", on="Year")
merged.rename(columns=lambda x: x.strip(), inplace=True)

print(merged)

# Create the figure and first y-axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot crime rates on the first y-axis
ax1.plot(merged["Year"], merged["Data.Rates.Property.All"], label="Property Crime Rate", color="blue", marker="o")
ax1.plot(merged["Year"], merged["Data.Rates.Violent.All"], label="Violent Crime Rate", color="red", marker="o")
ax1.set_ylabel("Crime Rate (per 100k people)", fontsize=12)
ax1.set_xlabel("Year", fontsize=12)
ax1.tick_params(axis="y", labelcolor="black")
ax1.legend(loc="upper left")

# Create the second y-axis
ax2 = ax1.twinx()
ax2.plot(merged["Year"], merged["Fixed broadband subscriptions (per 100 people)"], label="Broadband Subscriptions (per 100 people)", color="green", marker="o")
ax2.set_ylabel("Broadband Subscriptions (per 100 people)", fontsize=12)
ax2.tick_params(axis="y", labelcolor="green")
ax2.legend(loc="upper right")

# Add title and grid
plt.title("Crime Rates and Broadband Subscriptions Over Time\nr=-0.93 for violent crime and property crime", fontsize=14)
ax1.grid(True, linestyle="--", alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

corr = merged.corr(numeric_only=True)
print(corr)

plt.title("Crime Rates and Broadband Subscriptions Correlation", fontsize=14)
dataplot = sn.heatmap(corr, cmap="YlGnBu", annot=True)
plt.show()


