import os
import numpy as np
from crypto_utility import experiments

def generate(DATA_PATHS, TENSOR_PATH, temporal_sequence_considered, SingleFeaturesToExclude, MultiFeaturesToExclude):
    for path in DATA_PATHS:
        series = os.listdir(path)
        for s in series:
            stock_name = s.replace(".csv", "")
            os.makedirs(TENSOR_PATH + "/" + stock_name, exist_ok=True)

            if "horizontal" not in path:
                features_to_exclude_from_scaling = SingleFeaturesToExclude
            else:
                features_to_exclude_from_scaling = MultiFeaturesToExclude

            data_compliant, features, features_without_date, scaler = experiments.prepare_input_forecasting(
                    path + "/" + s,
                    features_to_exclude_from_scaling)
            for temporal in temporal_sequence_considered:
                print(s, "\t", temporal)
                experiments.fromtemporal_totensor(np.array(data_compliant), temporal,
                                                                       TENSOR_PATH + "/" + stock_name + "/",
                                                                       stock_name)