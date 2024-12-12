#!/bin/bash
source .env/bin/activate

declare -a arr=("sp500" "nyse" "nasdaq")

for i in "${arr[@]}"; do
    python stock_data.py -s Datasets_Stock/"$i"/csv/
done
