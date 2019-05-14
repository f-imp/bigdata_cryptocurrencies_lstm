from crypto_runner.do_experiment_1 import single_target
from crypto_runner.do_experiment_3 import multi_target
from crypto_utility import test_set
from crypto_runner import do_preprocessing

import warnings

warnings.filterwarnings("ignore")

do_preprocessing.run()

# -------- PARAMETERS ----------------------------------------------------------------------------
temporal_sequence_considered = [30, 100, 200]
number_neurons_LSTM = [128, 256]
TENSOR_PATH = "../crypto_TensorData"
TEST_SET = test_set.get_testset("../crypto_testset/from_2017_06_26_until_2017_06_26/test_set.txt")
SINGLE_features_to_exclude_from_scaling = ['Symbol']
MULTI_features_to_exclude_from_scaling = ['Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6',
                                          'Symbol_7', 'Symbol_8', 'Symbol_9', 'Symbol_10']
# ------------------------------------------------------------------------------------------------


# ------------------------------------ EXPERIMENT ONE (single + basic) ------------------------------------
EXPERIMENT_ONE = "../SingleTarget_Data"
DATA_PATH_ONE = "../crypto_preprocessing/step0_data/"
print(EXPERIMENT_ONE)
single_target(EXPERIMENT=EXPERIMENT_ONE, DATA_PATH=DATA_PATH_ONE, TENSOR_DATA_PATH=TENSOR_PATH,
              temporal_sequence=temporal_sequence_considered,
              number_neurons=number_neurons_LSTM,
              features_to_exclude_from_scaling=SINGLE_features_to_exclude_from_scaling, testing_set=TEST_SET)

# ------------------------------------ EXPERIMENT TWO (single + indicators) ------------------------------------
EXPERIMENT_TWO = "../SingleTarget_Data_with_Indicators"
DATA_PATH_TWO = "../crypto_preprocessing/step1_indicators/"
print(EXPERIMENT_TWO)
single_target(EXPERIMENT=EXPERIMENT_TWO, DATA_PATH=DATA_PATH_TWO, TENSOR_DATA_PATH=TENSOR_PATH,
              temporal_sequence=temporal_sequence_considered,
              number_neurons=number_neurons_LSTM,
              features_to_exclude_from_scaling=SINGLE_features_to_exclude_from_scaling, testing_set=TEST_SET)

# ------------------------------------ EXPERIMENT THREE (multi + basic) ------------------------------------
EXPERIMENT_THREE = "../MultiTarget_Data"
DATA_PATH_THREE = "../crypto_preprocessing/step5_horizontal/"
print(EXPERIMENT_THREE)
multi_target(EXPERIMENT=EXPERIMENT_THREE, DATA_PATH=DATA_PATH_THREE, TENSOR_DATA_PATH=TENSOR_PATH,
             temporal_sequence=temporal_sequence_considered,
             number_neurons=number_neurons_LSTM,
             features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling, testing_set=TEST_SET)

# ------------------------------------ EXPERIMENT FOUR (multi + indicators) ------------------------------------
EXPERIMENT_FOUR = "../MultiTarget_Data_with_Indicators"
DATA_PATH_FOUR = "../crypto_preprocessing/step5_horizontal/"
print(EXPERIMENT_FOUR)
multi_target(EXPERIMENT=EXPERIMENT_FOUR, DATA_PATH=DATA_PATH_FOUR, TENSOR_DATA_PATH=TENSOR_PATH,
             temporal_sequence=temporal_sequence_considered,
              number_neurons=number_neurons_LSTM,
              features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling, testing_set=TEST_SET)
