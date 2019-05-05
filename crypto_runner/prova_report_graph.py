from crypto_utility.report_data import report_configurations, report_stockseries

EXPERIMENT = "../crypto_experiment_one"
TENSOR_PATH = "../crypto_TensorData"
RESULT_PATH = "crypto_Result"
DATA_PATH = "../crypto_preprocessing/step2_normalized/"
REPORT_FOLDER_NAME = "Report"

temporal_sequence_considered = [30, 100, 200]
number_neurons_LSTM = [128, 256]

report_configurations(temporal_sequence_used=temporal_sequence_considered, neurons_used=number_neurons_LSTM,
                      name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                      name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

report_stockseries(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                   name_folder_report=REPORT_FOLDER_NAME,
                   name_files_output="report")
