import os
from itertools import product

from utility import test_set
from utility import experiments

path_data_with_indicators = "../preprocessing/step2_normalized/"
files = os.listdir(path_data_with_indicators)

# Input Experiment
set_of_data_tester = test_set.get_testset("../testset_generated/from_2018_10_01_until_2019_01_15/test_set.txt")
to_exclude = ['stock_id', 'ChangePercentage', 'TradedQuantity', 'TotalTradedVolumeIncludingBlocks']
temporal_sequence_considered = [30, 100, 200]
number_neurons = [128, 256]

# Perform Experiment (single or multiple)
# NB: in order to perform different experiments with the same parameters every time
# easily use a for (loop structure)
for f in files[0:1]:
    data_compliant, features_considered, scaler = experiments.prepare_input_forecasting(path_data_with_indicators + f,
                                                                                        to_exclude)
    for temporal, neurons in product(temporal_sequence_considered, number_neurons):
        print(temporal, "\t", neurons)
