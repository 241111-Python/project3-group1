import os
import pandas as pd
import matplotlib.pyplot as plt
import library
import argparse

# Argument parsing and setup
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--stocks",
    type=str,
    help="Path to folder of stock data in CSV format",
)
parser.add_argument(
    "-r",
    "--rate",
    type=str,
    help="Crime rate to analyze against",
)
args = parser.parse_args()


figures = "correlation-graphs"
stocks = os.path.join(*["Datasets_Stock", "sp500", "csv"])
crime_rates = ["Data.Rates.Property.All", "Data.Rates.Violent.All"]
crime_rate = "Data.Rates.Total.All"

if args.stocks:
    stocks = args.stocks
stock_source = list(filter(None, stocks.split(os.sep)))[-2].upper()

if args.rate:
    crime_rate = args.rate


def get_data_corr(file):
    df_s = pd.read_csv(
        file,
        usecols=["Date", "Adjusted Close"],
    )

    # Format stock data to yearly avg
    df_s["Year"] = pd.to_numeric(df_s["Date"].str[-4:])
    df_s = df_s.drop("Date", axis=1).groupby("Year").mean()

    # Check data integrity
    n = len(df_s)
    if n < 40:
        return None, None

    # Combine crime rates
    df_c["Data.Rates.Total.All"] = df_c[crime_rates[0]] + df_c[crime_rates[1]]

    # Merge
    merged_df = pd.merge(df_c, df_s, on="Year")

    # Get stats
    attr1 = crime_rate
    attr2 = "Adjusted Close"
    correlation = merged_df[attr1].corr(merged_df[attr2])

    return merged_df, correlation


# Load datasets
df_c = library.load_crime_df()
corrs = []

for file in os.scandir(stocks):
    df, corr = get_data_corr(file)

    if corr is None:
        continue

    corrs.append((corr, file))

# Setup plotting
attr1 = crime_rate
attr2 = "Adjusted Close"
color1 = "Red"
color2 = "Blue"
type = ["P", "N"]
corrs = sorted(corrs, key=lambda x: x[0])

for n, i in enumerate([corrs[-1], corrs[0]]):

    merged_df, correlation = get_data_corr(i[1])

    years = merged_df["Year"]
    attribute1 = merged_df[attr1]
    attribute2 = merged_df[attr2]
    label1 = f"US {crime_rate.split(".")[-2]} Crime Rate"
    label2 = i[1].name.split(".")[0]

    # Plot and save fig
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Year")
    ax1.set_ylabel(label1 + " (per 100,000 population)", color=color1)
    ax1.plot(years, attribute1, label=label1, color=color1, marker=None, linestyle="-")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax2 = ax1.twinx()
    ax2.set_ylabel(label2 + " (avg. adjusted closing price in USD)", color=color2)
    ax2.plot(years, attribute2, label=label2, color=color2, marker=None, linestyle="-")
    ax2.tick_params(axis="y", labelcolor=color2)
    fig.suptitle(f"{label1} vs. {label2} ({stock_source})\nr = {round(correlation, 2)}")
    fig.tight_layout()

    plt.savefig(
        os.path.join(figures, f"{type[n]}_{attr1}_vs_{stock_source}_{label2}.png")
    )

# Print out all correlations
with open(os.path.join(figures, f"info_{stock_source}.txt"), "w+") as file:
    file.write(f"{stock_source} / {crime_rate}\n\nTop 5 negative:\n")
    for c in corrs[:5]:
        file.write(f"{c[1].name.split(".")[0]}: {round(c[0], 2)}\n")
    file.write("\nTop 5 positive:\n")
    for c in corrs[-5:]:
        file.write(f"{c[1].name.split(".")[0]}: {round(c[0], 2)}\n")
