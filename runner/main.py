import os
from utility import preprocessing
import pandas as pd

# PRE PROCESSING
# ------------------------------------------
# STEP.1: Add Additional Features
# ------------------------------------------
# Listing all available time series
raw_data = "../data/1_original"
stock_series = os.listdir(raw_data)
output_indicators_path = "../code_testing_DARIMUOVEREPOI/1_adding_indicators/"
# Execute over all time series in the folder chosen
# Performs indicators: RSI, SMA, EMA
# Over 14, 30, 60 previous days
lookback = [14, 30, 60]
for each_stock in stock_series:
    name = each_stock.replace(".csv", "")
    file = raw_data + "/" + each_stock
    # preprocessing.generate_indicators(file, "PriceOfLastTransaction", lookback, output_indicators_path, name)
# ------------------------------------------
# STEP.2: Normalize Data
# ------------------------------------------
# Listing time series with indicators
with_indicators_data = "../code_testing_DARIMUOVEREPOI/1_adding_indicators"
with_indicators_stock_series = os.listdir(with_indicators_data)
output_normalized_path = "../code_testing_DARIMUOVEREPOI/2_normalized/"
# Chosen features to exclude in normalizing process
excluded_features = ['stock_id', 'Date']
for each_stock_with_indicators in with_indicators_stock_series:
    name = each_stock_with_indicators.replace("_with_indicators.csv", "")
    file = with_indicators_data + "/" + each_stock_with_indicators
    # preprocessing.normalized(file, excluded_features, output_normalized_path, name)
