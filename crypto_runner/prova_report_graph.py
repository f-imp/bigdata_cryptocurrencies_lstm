import os

from crypto_utility.report_data import report_configurations_exp1, report_stockseries_exp1, report_configurations_exp2, \
    report_configurations_exp3

# EXPERIMENT ONE
# ------------------------------------------------------------------------------------------------------------------------
# EXPERIMENT = "../crypto_experiment_one"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "crypto_Result"
# DATA_PATH = "../crypto_preprocessing/step2_normalized/"
# REPORT_FOLDER_NAME = "Report"

# temporal_sequence_considered = [30, 100, 200]
# number_neurons_LSTM = [128, 256]

# report_configurations_exp1(temporal_sequence_used=temporal_sequence_considered, neurons_used=number_neurons_LSTM,
#                       name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                       name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")
#
# report_stockseries_exp1(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                    name_folder_report=REPORT_FOLDER_NAME,
#                    name_files_output="report")

# EXPERIMENT TWO
# ------------------------------------------------------------------------------------------------------------------------

# EXPERIMENT = "../crypto_experiment_two"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "crypto_Result"
# DATA_PATH = "../crypto_preprocessing/step3_alldata/"
# REPORT_FOLDER_NAME = "Report"
#
# temporal_sequence_considered = [30, 60, 100]
#
# report_configurations_exp2(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                            name_folder_report=REPORT_FOLDER_NAME, name_files_output="overall_report")

# EXPERIMENT THREE
# ------------------------------------------------------------------------------------------------------------------------
EXPERIMENT = "../crypto_experiment_three"
TENSOR_PATH = "../crypto_TensorData"
RESULT_PATH = "crypto_Result"
DATA_PATH = "../crypto_preprocessing/step5_horizontal/"
REPORT_FOLDER_NAME = "Report"


report_configurations_exp3(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                           name_folder_report=REPORT_FOLDER_NAME, name_files_output="overall_report")
