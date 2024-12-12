import os
import pandas as pd
import matplotlib.pyplot as plt
import library

figures = "correlation-graphs"
emissions = "Datasets_Emissions"
crime_rate = ["Data.Rates.Property.All", "Data.Rates.Violent.All"]

# Load datasets
df_e = pd.read_excel(os.path.join(emissions, "table4.xlsx"), header=4)
df_c = library.load_crime_df(include_states=True)

# Clean
df_e = df_e.iloc[:-1, :-4]
df_e = df_e.melt(id_vars=["State"])
df_e.columns = ["State", "Year", "CO2"]

df_c["Data.Rates.Total.All"] = df_c[crime_rate[0]] + df_c[crime_rate[1]]
df_c = df_c[["Year", "State", "Data.Rates.Total.All"]]

# Merge
merged_df = pd.merge(df_e, df_c, on=["Year", "State"])

# Get correlations
# print(merged_df.corr(numeric_only=True))

co2c = merged_df.groupby("State").corr(numeric_only=True)["CO2"]
co2c = co2c.reset_index(level=[0, 1])
co2c = (
    co2c[co2c["level_1"] == "Data.Rates.Total.All"]
    .sort_values(by="CO2")
    .reset_index(drop=True)
)


# Setup plotting
attr1 = "Data.Rates.Total.All"
attr2 = "CO2"
color1 = "Red"
color2 = "Blue"
for s in [co2c.loc[0], co2c.loc[50]]:
    df = merged_df[merged_df["State"] == s["State"]]

    years = df["Year"]
    attribute1 = df[attr1]
    attribute2 = df[attr2]
    label1 = f"{s["State"]} {attr1.split(".")[-2]} Crime Rate"
    label2 = f"{attr2} Emissions per Capita"

    # Plot and save fig
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Year")
    ax1.set_ylabel(label1 + " (per 100,000 population)", color=color1)
    ax1.plot(years, attribute1, label=label1, color=color1, marker=None, linestyle="-")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2 + " (Tons)", color=color2)
    ax2.plot(years, attribute2, label=label2, color=color2, marker=None, linestyle="-")
    ax2.tick_params(axis="y", labelcolor=color2)
    fig.suptitle(f"{label1} vs. {label2}\nr = {round(s['CO2'], 2)}")
    fig.tight_layout()

    plt.savefig(os.path.join(figures, f"{s["State"]}_{attr1}_vs_{attr2}.png"))
