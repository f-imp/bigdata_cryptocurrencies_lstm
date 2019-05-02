import os

from crypto_utility import preprocessing

# PRE PROCESSING
# Set the name of folder in which save all intermediate results
name_folder = "crypto_preprocessing"
try:
    os.mkdir("../" + name_folder)
except OSError:
    print("Creation of the directory %s failed" % name_folder)
else:
    print("Successfully created the directory %s " % name_folder)
# ------------------------------------------
# STEP.1: Add Additional Features
# ------------------------------------------
# Listing all available time series (original data)
raw_data = "../crypto_data/data"
stock_series = os.listdir(raw_data)
folder_step_one = "step1_indicators"
try:
    os.mkdir("../" + name_folder + "/" + folder_step_one)
except OSError:
    print("Creation of the directory %s failed" % folder_step_one)
else:
    print("Successfully created the directory %s " % folder_step_one)
output_indicators_path = "../" + name_folder + "/" + folder_step_one + "/"
# Execute over all time series in the folder chosen
# Performs indicators: RSI, SMA, EMA
# Over 14, 30, 60 previous days
lookback = [14, 30, 60]
for each_stock in stock_series:
    name = each_stock.replace(".csv", "")
    file = raw_data + "/" + each_stock
    preprocessing.generate_indicators(file, "Close", lookback, output_indicators_path, name)
# ------------------------------------------
# STEP.2: Normalize Data
# ------------------------------------------
# Listing time series with indicators
with_indicators_data = "../" + name_folder + "/" + folder_step_one + "/"
with_indicators_stock_series = os.listdir(with_indicators_data)
folder_step_two = "step2_normalized"
try:
    os.mkdir("../" + name_folder + "/" + folder_step_two)
except OSError:
    print("Creation of the directory %s failed" % folder_step_two)
else:
    print("Successfully created the directory %s " % folder_step_two)
output_normalized_path = "../" + name_folder + "/" + folder_step_two + "/"
# Chosen features to exclude in normalizing process
excluded_features = ['DateTime', 'Symbol']
for each_stock_with_indicators in with_indicators_stock_series:
    name = each_stock_with_indicators.replace("_with_indicators.csv", "")
    file = with_indicators_data + "/" + each_stock_with_indicators
    preprocessing.normalized(file, excluded_features, output_normalized_path, name)
