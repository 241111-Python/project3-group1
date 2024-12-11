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
crime_rate = ["Data.Rates.Property.All", "Data.Rates.Violent.All"][1]

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

    # Merge
    merged_df = pd.merge(df_c, df_s, on="Year")

    # Get stats
    attr1 = crime_rate
    attr2 = "Adjusted Close"
    correlation = merged_df[attr1].corr(merged_df[attr2])

    return merged_df, correlation


# Load datasets
df_c = library.load_crime_df()

min_corr = [10, None]
max_corr = [-10, None]

for file in os.scandir(stocks):
    df, corr = get_data_corr(file)

    if corr is None:
        continue

    if corr > max_corr[0]:
        max_corr[0] = corr
        max_corr[1] = file
    if corr < min_corr[0]:
        min_corr[0] = corr
        min_corr[1] = file

# Setup plotting
attr1 = crime_rate
attr2 = "Adjusted Close"
color1 = "Red"
color2 = "Blue"
type = ["P", "N"]

for n, i in enumerate([max_corr, min_corr]):

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
