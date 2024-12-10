import os
import pandas as pd
import matplotlib.pyplot as plt
import library

figures = "correlation-graphs"
stock = "AAPL"

# Load datasets
df_c = library.load_crime_df()
df_s = pd.read_csv(
    os.path.join("Datasets_Stock", "sp500", "csv", f"{stock}.csv"),
    usecols=["Date", "Adjusted Close"],
)

# Format stock data to yearly avg
df_s["Year"] = pd.to_numeric(df_s["Date"].str[-4:])
df_s = df_s.drop("Date", axis=1).groupby("Year").mean()

# Merge
merged_df = pd.merge(df_c, df_s, on="Year")

# Plot
attr1 = "Data.Rates.Property.All"
attr2 = "Adjusted Close"
color1 = "Red"
color2 = "Blue"

years = merged_df["Year"]
attribute1 = merged_df[attr1]
attribute2 = merged_df[attr2]
label1 = "US Crime Rate"
label2 = stock
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_xlabel("Year")
ax1.set_ylabel(label1 + " (per 100,000 population)", color=color1)
ax1.plot(years, attribute1, label=label1, color=color1, marker=None, linestyle="-")
ax1.tick_params(axis="y", labelcolor=color1)
ax2 = ax1.twinx()
ax2.set_ylabel(label2+ " (avg. adjusted closing price)", color=color2)
ax2.plot(years, attribute2, label=label2, color=color2, marker=None, linestyle="-")
ax2.tick_params(axis="y", labelcolor=color2)
fig.suptitle(f"{label1} vs. {label2}")
fig.tight_layout()

plt.savefig(os.path.join(figures, f"{attr1}_vs_{stock}.png"))
