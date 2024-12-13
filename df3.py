import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from library import load_crime_df

df = pd.read_csv("Datasets_Crime/state_crime.csv", usecols=["State", "Year", "Data.Rates.Property.All", "Data.Rates.Violent.All"])
df2 = pd.read_csv("Datasets_DF/vgsales.csv")

df2 = df2[(df2["Year"] <= 2014)].groupby("Year", as_index=False)["NA_Sales"].sum()

df = df[df["State"] == "United States"]

merged = df.merge(df2, how="inner", on="Year")
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
ax2.plot(merged["Year"], merged["NA_Sales"], label="Video Games Sold in NA (in millions of copies sold)", color="green", marker="o")
ax2.set_ylabel("Video Games Sold in NA (in millions of copies sold)", fontsize=12)
ax2.tick_params(axis="y", labelcolor="green")
ax2.legend(loc="upper right")

# Add title and grid
plt.title("US Crime Rates and NA Games Sales Over Time\nr=-0.84 for violent crime\nr=-0.74 for property crime", fontsize=14)
ax1.grid(True, linestyle="--", alpha=0.7)

plt.show()

corr = merged.corr(numeric_only=True)
print(corr)

sn.heatmap(corr, cmap="YlGnBu", annot=True)
plt.title("Crime Rates and NA Games Sales Correlation", fontsize=14)
plt.show()

