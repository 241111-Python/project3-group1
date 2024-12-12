import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import library

figures = "correlation-graphs"
data = "Datasets_Consumption"
crime_rate = ["Data.Totals.Property.All", "Data.Totals.Violent.All"]

# Load datasets
df_ps = pd.read_excel(
    os.path.join(data, "FoodImports.xlsx"), sheet_name="FoodVolume", header=3
)
df_c = library.load_crime_df(include_states=False)

# Clean
df_ps.rename(columns={df_ps.columns[1]: "Product"}, inplace=True)
df_ps.drop(columns=df_ps.columns[:1], inplace=True)

# Format
df_ps = pd.melt(
    df_ps,
    id_vars="Product",
    var_name="Year",
    value_vars=[str(y) for y in range(1999, 2023)],
).dropna()
df_ps = df_ps.pivot(index="Year", columns="Product", values="value").reset_index()
df_ps["Year"] = df_ps["Year"].astype(int)
df_ps.columns = [
    re.sub(r"[0-9/]", "", c).strip() for c in df_ps.columns.values.tolist()
]

df_c["Data.Totals.Total.All"] = df_c[crime_rate[0]] + df_c[crime_rate[1]]
df_c.drop(df_c.columns[df_c.columns.str.contains("Rate|Rape")], axis=1, inplace=True)

# Merge
merged_df = pd.merge(df_ps, df_c, on="Year")

# Plot heatmap
ax = sns.heatmap(
    merged_df.corr(numeric_only=True).iloc[1:14, 16:], annot=True, fmt=".2f", cbar=False
)
ax.set_xticklabels(
    ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor"
)

plt.title("US Total Crimes vs Food Import Volume (1999-2019)")
plt.tight_layout()
plt.savefig(os.path.join(figures, "Crime_vs_food_imports.png"))

# Setup plotting
attr1 = "Data.Totals.Violent.Murder"
attr2 = "Dairy"
color1 = "Red"
color2 = "Blue"

years = merged_df["Year"]
attribute1 = merged_df[attr1]
attribute2 = merged_df[attr2]
label1 = f"US {attr1.split(".")[-1]}s"
label2 = f"{attr2} Imports"
correlation = merged_df[attr1].corr(merged_df[attr2])

# Plot and save fig
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_xlabel("Year")
ax1.set_ylabel(label1, color=color1)
ax1.plot(years, attribute1, label=label1, color=color1, marker=None, linestyle="-")
ax1.tick_params(axis="y", labelcolor=color1)
ax2 = ax1.twinx()
ax2.set_ylabel(label2 + " (1000s of Tons)", color=color2)
ax2.plot(years, attribute2, label=label2, color=color2, marker=None, linestyle="-")
ax2.tick_params(axis="y", labelcolor=color2)
fig.suptitle(f"{label1} vs. {label2}\nr = {round(correlation, 2)}")
fig.tight_layout()

plt.savefig(os.path.join(figures, f"{attr1}_vs_{attr2}.png"))
