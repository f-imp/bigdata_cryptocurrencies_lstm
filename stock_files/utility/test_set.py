# We are sure that all stocks series are observed until 15th of January 2019 (2019-01-15)
# Due to it's useful create a function that takes the starting and ending date
# and "number_samples" entries choosed randomly
import pandas as pd
import random
import ast
import numpy as np

np.random.seed(0)


def generate_testset(path_data, filename, start, end, number_samples, output_path, filename_output):
    data = pd.read_csv(path_data + filename, sep=';')
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    data = data.sort_values('Date', ascending=False)
    dates_taken = data[(data['Date'] >= start) & (data['Date'] <= end)]['Date']
    dates_taken = list(dates_taken.map(lambda d: d.strftime("%Y-%m-%d")))
    test_set = random.sample(dates_taken, number_samples)
    with open(output_path + filename_output + ".txt", 'w') as file:
        file.write(str(test_set))
    return


def get_testset(path_file):
    with open(path_file) as td:
        file_test_set = td.read()
    test_set = ast.literal_eval(file_test_set)
    test_set = np.array(pd.to_datetime(test_set, yearfirst=True))
    return test_set
