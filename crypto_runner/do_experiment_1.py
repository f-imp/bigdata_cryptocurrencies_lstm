# cancellare crypto_expreriment_one prima di runnare

import os
from itertools import product

import numpy as np
import pandas as pd

from crypto_utility import experiments
from crypto_utility.report_data import report_configurations_exp1, report_stockseries_exp1

np.random.seed(0)


# EXPERIMENT = "../crypto_experiment_one"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "crypto_Result"
# DATA_PATH = "../crypto_preprocessing/step2_normalized/"
# REPORT_FOLDER_NAME = "Report"

# Parameters of experiments
# series = os.listdir(DATA_PATH)
# temporal_sequence_considered = [30, 100, 200]
# number_neurons_LSTM = [128, 256]
# Testing_Set = test_set.get_testset("../crypto_testset/from_2017_06_26_until_2017_06_26/test_set.txt")
# features_to_exclude_from_scaling = ['Symbol']
# features_to_exclude_from_scaling = ['stock_id', 'ChangePercentage', 'TradedQuantity', 'TotalTradedVolumeIncludingBlocks']


def single_target(EXPERIMENT, DATA_PATH, TENSOR_DATA_PATH, temporal_sequence, number_neurons,
                  features_to_exclude_from_scaling, testing_set):
    RESULT_PATH = "Result"
    REPORT_FOLDER_NAME = "Report"

    series = os.listdir(DATA_PATH)

    # Create Structure of Folder - according to defined path
    os.mkdir(EXPERIMENT)

    os.makedirs(TENSOR_DATA_PATH, exist_ok=True)

    os.mkdir(EXPERIMENT + "/" + RESULT_PATH)

    for s in series:
        if DATA_PATH == "../crypto_preprocessing/step1_indicators/":
            # stock_name = s.replace("_normalized.csv", "")
            stock_name = s.replace("_with_indicators.csv", "")
        else:
            stock_name = s.replace(".csv", "")
        # for each stock
        # create a folder for data
        os.makedirs(TENSOR_DATA_PATH + "/" + stock_name, exist_ok=True)
        # create a folder for results
        os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name)
        data_compliant, features, features_without_date, scaler = experiments.prepare_input_forecasting(
            DATA_PATH + "/" + s,
            features_to_exclude_from_scaling)
        for temporal, neurons in product(temporal_sequence, number_neurons):
            print(s, "\t", temporal, "\t", neurons)
            dataset_tensor = experiments.fromtemporal_totensor(np.array(data_compliant), temporal,
                                                               TENSOR_DATA_PATH + "/" + stock_name + "/",
                                                               stock_name)
            # Dict for statistics
            predictions_file = {'symbol': [], 'date': [], 'observed_norm': [], 'predicted_norm': [],
                                'observed_denorm': [],
                                'predicted_denorm': []}
            errors_file = {'symbol': [], 'date': [], 'rmse_norm': [], 'rmse_denorm': []}
            # define a name for this configuration (following folder)
            configuration_name = "LSTM_" + str(neurons) + "_neurons_" + str(temporal) + "_days"
            # Create a folder to save
            # - best model checkpoint
            best_model = "model"
            # - statistics (results)
            statistics = "stats"
            os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name)
            os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + best_model)
            os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + statistics)
            for data_tester in testing_set:
                train, test = experiments.train_test_split_w_date(features, dataset_tensor, data_tester)
                train = train[:, :, 1:]
                test = test[:, :, 1:]

                x_train, y_train = train[:, :-1, :], train[:, -1, features_without_date.index('Close')]
                x_test, y_test = test[:, :-1, :], test[:, -1, features_without_date.index('Close')]

                # Fare il training
                if data_tester == testing_set[0]:
                    model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                             dropout=0.2,
                                                             epochs=100,
                                                             batch_size=256,
                                                             dimension_last_layer=1,
                                                             model_path=EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + best_model + "/")
                else:
                    model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                             dropout=0.2,
                                                             epochs=100,
                                                             batch_size=256, dimension_last_layer=1, model=model,
                                                             model_path=EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + best_model + "/")
                # Tiriamo fuori la predizione per ogni esempio di test
                test_prediction = model.predict(x_test)
                rmse = experiments.get_RMSE(y_test, test_prediction)
                y_test_denorm = scaler.inverse_transform(y_test.reshape(-1, 1))

                test_prediction_denorm = scaler.inverse_transform(test_prediction)
                rmse_denorm = experiments.get_RMSE(y_test_denorm, test_prediction_denorm)

                y_test = float(y_test)
                test_prediction = float(test_prediction)
                y_test_denorm = float(y_test_denorm)
                test_prediction_denorm = float(test_prediction_denorm)

                # Salvo i risultati nei dizionari
                predictions_file['symbol'].append(stock_name)
                predictions_file['date'].append(data_tester)
                predictions_file['observed_norm'].append(y_test)
                predictions_file['predicted_norm'].append(test_prediction)
                predictions_file['observed_denorm'].append(y_test_denorm)
                predictions_file['predicted_denorm'].append(test_prediction_denorm)

                errors_file['symbol'].append(stock_name)
                errors_file['date'].append(data_tester)
                errors_file['rmse_norm'].append(rmse)
                errors_file['rmse_denorm'].append(rmse_denorm)
            pd.DataFrame(data=predictions_file).to_csv(
                EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + statistics + "/" + 'predictions.csv')
            pd.DataFrame(data=errors_file).to_csv(
                EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + statistics + "/" + 'errors.csv')

    report_configurations_exp1(temporal_sequence_used=temporal_sequence, neurons_used=number_neurons,
                               name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                               name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

    report_stockseries_exp1(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                            name_folder_report=REPORT_FOLDER_NAME,
                            name_files_output="report")

    return
