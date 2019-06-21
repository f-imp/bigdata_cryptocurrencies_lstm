from crypto_runner.do_experiment_single import single_target
from crypto_runner.do_experiment_multi import multi_target
from crypto_utility import test_set,experiments,tensor_data
from crypto_runner import do_preprocessing,build_testset_dates
from crypto_utility.report_data import report_configurations_SingleTarget, report_stockseries_SingleTarget
from crypto_utility.report_data import report_configurations_MultiTarget, report_stockseries_MultiTarget

import warnings

warnings.filterwarnings("ignore")

#
# # -------- SETUP ----------------------------------------------------------------------------
#Generate test set (only needed to run once)
#build_testset_dates.run()

#set the day to use to cut the data (the first day to use in training, should be the first day of the cryptocurrency with less entry)
first_day ="2015-03-30" #Top8 Nem first day
cryptocurrenciesSymbols=["BTC","XRP","LTC","XLM","XMR","DASH","XEM","DOGE"] #Top8

#first_day = "2014-09-03" #Top5 Stellar first day
#cryptocurrenciesSymbols=["BTC","LTC","XLM","DASH","DOGE"] #Top5

#Preprocess dataset data (Relaunch preprocessing if data changes)
do_preprocessing.run(first_day,cryptocurrenciesSymbols)

#
# # -------- PARAMETERS ----------------------------------------------------------------------------
#LSTM Parameters
temporal_sequence_considered = [30, 100, 200]
number_neurons_LSTM = [128, 256]
learning_rate=0.001 #Top8
#learning_rate=0.0001 #Top5


#
# # -------- DATA ----------------------------------------------------------------------------
#Data location for experiments [ST,ST-i,MT,MT-i]
DATA_PATHS=["../crypto_preprocessing/step4_cutdata/","../crypto_preprocessing/step4_cutdata_indicators/","../crypto_preprocessing/step5_horizontal/","../crypto_preprocessing/step5_horizontal/"]

#Indicate the features that will be excluded from the scaling operations
SINGLE_features_to_exclude_from_scaling = ['Symbol']
MULTI_features_to_exclude_from_scaling = ['Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6', 'Symbol_7', 'Symbol_8'] #Top8
#MULTI_features_to_exclude_from_scaling = ['Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5'] #Top5

#set dimension for last layer in multitarget
dimension_last_layer=8 #Top8
#dimension_last_layer=5 #Top5

#
# # -------- TENSORS ----------------------------------------------------------------------------
#Tensor location
TENSOR_PATH = "../crypto_TensorData"

#Generate tensors based on preprocessed data (Relaunch if data changes)
#Top8 and Top5 use different Tensors be sure to use the right ones
#tensor_data.generate(DATA_PATHS[:-1], TENSOR_PATH, temporal_sequence_considered, SINGLE_features_to_exclude_from_scaling, MULTI_features_to_exclude_from_scaling)

#
# # -------- TEST SET ----------------------------------------------------------------------------
#Retrieve test set
TEST_SET = test_set.get_testset("../crypto_testset/from_2016_07_01_until_2017_06_26/test_set.txt")




#
# # ------------------------------------ EXPERIMENTS ------------------------------------
#EXPERIMENT ONE = single target (ST)
#EXPERIMENT TWO = single target with indicators (ST-i)
#EXPERIMENT THREE = multi target (MT)
#EXPERIMENT FOUR = multi target with indicators (MT-i)

#It is possible to run them all but sometimes the RAM becomes full (some kind of memory leak) and execution becomes slow as hell
#So we suggests to run one experiment at a time commenting the others
#Also delete previous results and their folder before running

#
# # ------------------------------------ EXPERIMENT ONE (single + basic) ------------------------------------
EXPERIMENT_ONE = "../SingleTarget_Data"
DATA_PATH_ONE = DATA_PATHS[0]
print(EXPERIMENT_ONE)
single_target(EXPERIMENT=EXPERIMENT_ONE, DATA_PATH=DATA_PATH_ONE, TENSOR_DATA_PATH=TENSOR_PATH,
               temporal_sequence=temporal_sequence_considered,
               number_neurons=number_neurons_LSTM, learning_rate=learning_rate,
               features_to_exclude_from_scaling=SINGLE_features_to_exclude_from_scaling, testing_set=TEST_SET)




#
# # ------------------------------------ EXPERIMENT TWO (single + indicators) ------------------------------------
EXPERIMENT_TWO = "../SingleTarget_Data_with_Indicators"
DATA_PATH_TWO = DATA_PATHS[1]
print(EXPERIMENT_TWO)
single_target(EXPERIMENT=EXPERIMENT_TWO, DATA_PATH=DATA_PATH_TWO, TENSOR_DATA_PATH=TENSOR_PATH,
               temporal_sequence=temporal_sequence_considered,
               number_neurons=number_neurons_LSTM, learning_rate=learning_rate,
               features_to_exclude_from_scaling=SINGLE_features_to_exclude_from_scaling, testing_set=TEST_SET)


                        
#                        
# # ------------------------------------ EXPERIMENT THREE (multi + basic) ------------------------------------
EXPERIMENT_THREE = "../MultiTarget_Data"
DATA_PATH_THREE = DATA_PATHS[2]
print(EXPERIMENT_THREE)
multi_target(EXPERIMENT=EXPERIMENT_THREE, DATA_PATH=DATA_PATH_THREE, TENSOR_DATA_PATH=TENSOR_PATH,
             temporal_sequence=temporal_sequence_considered,
             number_neurons=number_neurons_LSTM, learning_rate=learning_rate, dimension_last_layer=dimension_last_layer,
             features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling, testing_set=TEST_SET)



#
# # ------------------------------------ EXPERIMENT FOUR (multi + indicators) ------------------------------------


EXPERIMENT_FOUR = "../MultiTarget_Data_with_Indicators"
DATA_PATH_FOUR = DATA_PATHS[3]
print(EXPERIMENT_FOUR)
multi_target(EXPERIMENT=EXPERIMENT_FOUR, DATA_PATH=DATA_PATH_FOUR, TENSOR_DATA_PATH=TENSOR_PATH,
             temporal_sequence=temporal_sequence_considered,
             number_neurons=number_neurons_LSTM, learning_rate=learning_rate, dimension_last_layer=dimension_last_layer,
             features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling, testing_set=TEST_SET)



'''
#Utili in caso si voglia addestare le configurazioni a pezzi e quindi generare i grafici in un secondo momento e non alla fine dei singoli esperimenti
#Generazione report esterna per Experiment One
EXPERIMENT_ONE = "../SingleTarget_Data"
RESULT_PATH = "Result"
REPORT_FOLDER_NAME ="Report"
report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence_considered, neurons_used=number_neurons_LSTM,
                           name_folder_experiment=EXPERIMENT_ONE, name_folder_result_experiment=RESULT_PATH,
                           name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT_ONE, name_folder_result_experiment=RESULT_PATH,
                        name_folder_report=REPORT_FOLDER_NAME,
                        name_files_output="report")



EXPERIMENT_TWO = "../SingleTarget_Data_with_Indicators"

#Generazione report esterna per Experiment Two
RESULT_PATH = "Result"
REPORT_FOLDER_NAME ="Report"
report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence_considered, neurons_used=number_neurons_LSTM,
                           name_folder_experiment=EXPERIMENT_TWO, name_folder_result_experiment=RESULT_PATH,
                           name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT_TWO, name_folder_result_experiment=RESULT_PATH,
                        name_folder_report=REPORT_FOLDER_NAME,
                        name_files_output="report")


EXPERIMENT_THREE = "../MultiTarget_Data"
cryptocurrenciesSymbols=["BTC","XRP","LTC","XLM","XMR","DASH","XEM","DOGE"]

RESULT_PATH = "Result"
REPORT_FOLDER_NAME ="Report"

report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence_considered, neurons_used=number_neurons_LSTM,
                           name_folder_experiment=EXPERIMENT_THREE, name_folder_result_experiment=RESULT_PATH,
                           name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT_THREE, name_folder_result_experiment=RESULT_PATH,
                        name_folder_report=REPORT_FOLDER_NAME,
                        name_files_output="report")





report_configurations_MultiTarget(name_folder_experiment=EXPERIMENT_THREE, name_folder_result_experiment=RESULT_PATH,
                                  name_folder_report=REPORT_FOLDER_NAME, name_files_output="overall_report")

report_stockseries_MultiTarget(name_folder_experiment=EXPERIMENT_THREE, name_folder_result_experiment=RESULT_PATH,
                               name_folder_report=REPORT_FOLDER_NAME, name_files_output="report", original_datapath=DATA_PATHS[2],
                               features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling)

EXPERIMENT_FOUR = "../MultiTarget_Data_with_Indicators"

#Generazione report esterna per Experiment Two
RESULT_PATH = "Result"
REPORT_FOLDER_NAME ="Report"


report_configurations_MultiTarget(name_folder_experiment=EXPERIMENT_FOUR, name_folder_result_experiment=RESULT_PATH,
                                  name_folder_report=REPORT_FOLDER_NAME, name_files_output="overall_report")

report_stockseries_MultiTarget(name_folder_experiment=EXPERIMENT_FOUR, name_folder_result_experiment=RESULT_PATH,
                               name_folder_report=REPORT_FOLDER_NAME, name_files_output="report", original_datapath=DATA_PATHS[2],
                               features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling)
'''