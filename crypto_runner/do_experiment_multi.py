import os
import numpy as np
import pandas as pd
from itertools import product
from crypto_utility import experiments
from crypto_utility.report_data import report_configurations_MultiTarget, report_stockseries_MultiTarget
from crypto_utility.report_data import report_configurations_SingleTarget, report_stockseries_SingleTarget

np.random.seed(0)


# TENSOR_PATH = "../crypto_TensorData"

# Parameters of experiments
# series = os.listdir(DATA_PATH)
# temporal_sequence_considered = [30, 100, 200]
# number_neurons_LSTM = [128, 256]
# Testing_Set = test_set.get_testset("../crypto_testset/from_2016_07_01_until_2017_06_26/test_set.txt")
# features_to_exclude_from_scaling = ['Symbol_1','Symbol_2','Symbol_3','Symbol_4','Symbol_5','Symbol_6','Symbol_7','Symbol_8']

def multi_target(EXPERIMENT, DATA_PATH, TENSOR_DATA_PATH, temporal_sequence, number_neurons, learning_rate,dimension_last_layer,
                 features_to_exclude_from_scaling, testing_set):
    MODELS_PATH="Models"
    RESULT_PATH = "Result"
    REPORT_FOLDER_NAME = "Report"

    # Create Structure of Folder - according to defined path
    os.makedirs(EXPERIMENT, exist_ok=True)

    os.makedirs(TENSOR_DATA_PATH, exist_ok=True)

    os.mkdir(EXPERIMENT + "/" + RESULT_PATH)
    os.mkdir(EXPERIMENT + "/" + MODELS_PATH)

    if "Indicators" in EXPERIMENT:
        s = "horizontal_indicators.csv"
    else:
        s = "horizontal.csv"

    stock_name = s.replace(".csv", "")

    # create a folder for data
    os.makedirs(TENSOR_DATA_PATH + "/" + stock_name, exist_ok=True)
    # create a folder for results
    #os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/")
    data_compliant, features, features_without_date, scaler = experiments.prepare_input_forecasting(
        DATA_PATH + "/" + s,
        features_to_exclude_from_scaling)
    target_indexes_without_date = [features_without_date.index(f) for f in features_without_date if
                                   f.startswith('Close')]
    # TODO --
    # devo leggere i simboli dal dataset per creare le colonne (per ogni criptovaluta) nel file '.csv' predictions
    # una funzione quindi che ritorni una lista con i nomi di ogni valuta, letti dal dataset di partenza
    # name_cryptostock = experiments.getNames(path_data= , features_to_exclude_from_scaling)
    names_crypto = experiments.getNames(DATA_PATH + s, features_to_exclude_from_scaling)

    for temporal, neurons in product(temporal_sequence, number_neurons):
        print(s, "\t", temporal, "\t", neurons)
        dataset_tensor = experiments.fromtemporal_totensor(np.array(data_compliant), temporal,
                                                           TENSOR_DATA_PATH + "/" + stock_name + "/",
                                                           stock_name)

        # Dict for statistics
        predictions_file = {'symbol': [], 'date': []}

        for n in names_crypto:
            predictions_file[n + "_observed_norm"] = []
            predictions_file[n + "_predicted_norm"] = []
            predictions_file[n + "_observed_denorm"] = []
            predictions_file[n + "_predicted_denorm"] = []

        # define a name for this configuration (following folder)
        configuration_name = "LSTM_" + str(neurons) + "_neurons_" + str(temporal) + "_days"
        # Create a folder to save
        # - best model checkpoint
        best_model = "model"
        # - statistics (results)
        statistics = "stats"

        os.mkdir(EXPERIMENT + "/" + MODELS_PATH + "/" + configuration_name)
        os.mkdir(EXPERIMENT + "/" + MODELS_PATH + "/" + configuration_name + "/" + best_model)

        for data_tester in testing_set:
            print("Addestro fino a: ", pd.to_datetime(data_tester))
            train, test = experiments.train_test_split_w_date(features, dataset_tensor, data_tester)
            train = train[:, :, 1:]
            test = test[:, :, 1:]

            x_train, y_train = train[:, :-1, :], train[:, -1, target_indexes_without_date]
            x_test, y_test = test[:, :-1, :], test[:, -1, target_indexes_without_date]

            # Fare il training
            if data_tester == testing_set[0]:
                model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                         learning_rate=learning_rate,
                                                         dropout=0.2,
                                                         epochs=100,
                                                         batch_size=256,
                                                         dimension_last_layer=dimension_last_layer,
                                                         model_path=EXPERIMENT + "/" + MODELS_PATH + "/" + "/" + configuration_name + "/" + best_model + "/")
            else:
                model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                         learning_rate=learning_rate,
                                                         dropout=0.2,
                                                         epochs=100,
                                                         batch_size=256,
                                                         dimension_last_layer=dimension_last_layer,
                                                         model=model,
                                                         model_path=EXPERIMENT + "/" + MODELS_PATH + "/" + "/" + configuration_name + "/" + best_model + "/")

            # Tiriamo fuori la predizione per ogni esempio di test
            test_prediction = model.predict(x_test)
            print("Predico per: ", pd.to_datetime(data_tester))
            print("Ho predetto: ", test_prediction)
            print("Valore Reale: ", y_test)
            print("\n")
            y_test_denorm = scaler.inverse_transform(y_test.reshape(-1, dimension_last_layer))

            test_prediction_denorm = scaler.inverse_transform(test_prediction)

            # Salvo i risultati nei dizionari
            predictions_file['symbol'].append(stock_name)
            predictions_file['date'].append(data_tester)

            # TODO - DEBUGGING
            # print(y_test[0],"\n",test_prediction[0],"\n",y_test_denorm[0],"\n",test_prediction_denorm[0])

            for n, v in zip(names_crypto, y_test[0]):
                predictions_file[n + "_observed_norm"].append(float(v))

            for n, v in zip(names_crypto, test_prediction[0]):
                predictions_file[n + "_predicted_norm"].append(float(v))

            for n, v in zip(names_crypto, y_test_denorm[0]):
                predictions_file[n + "_observed_denorm"].append(float(v))

            for n, v in zip(names_crypto, test_prediction_denorm[0]):
                predictions_file[n + "_predicted_denorm"].append(float(v))



        for n in names_crypto:
            os.makedirs(EXPERIMENT + "/" + RESULT_PATH + "/" + n, exist_ok=True)
            os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + n + "/" + configuration_name)
            os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + n + "/" + configuration_name + "/" + statistics)

            new_pred_file={}

            new_pred_file['symbol']= []
            for i in range (0,len(predictions_file['symbol'])): new_pred_file['symbol'].append(n)
            new_pred_file['date']= predictions_file['date']
            new_pred_file['observed_norm']= predictions_file[n+'_observed_norm']
            new_pred_file['predicted_norm']= predictions_file[n+'_predicted_norm']
            new_pred_file['observed_denorm']= predictions_file[n+'_observed_denorm']
            new_pred_file['predicted_denorm']= predictions_file[n+'_predicted_denorm']

            errors_file = {'symbol': [], 'rmse_norm': [], 'rmse_denorm': []}
            errors_file['symbol'].append(n)
            rmse = experiments.get_RMSE(new_pred_file['observed_norm'],new_pred_file['predicted_norm'])
            rmse_denorm = experiments.get_RMSE(new_pred_file['observed_denorm'], new_pred_file['predicted_denorm'])
            errors_file['rmse_norm'].append(rmse)
            errors_file['rmse_denorm'].append(rmse_denorm)

            pd.DataFrame(data=new_pred_file).to_csv(
                EXPERIMENT + "/" + RESULT_PATH + "/" + n + "/" + configuration_name + "/" + statistics + "/" + 'predictions.csv')
            pd.DataFrame(data=errors_file).to_csv(
                EXPERIMENT + "/" + RESULT_PATH + "/" + n + "/" + configuration_name + "/" + statistics + "/" + 'errors.csv')


    #commentare se non si vuole generare i report alla fine dell'addestramento
    report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence, neurons_used=number_neurons,
                               name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                               name_folder_report=REPORT_FOLDER_NAME, name_output_files="overall_report")

    report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                            name_folder_report=REPORT_FOLDER_NAME,
                            name_files_output="report")
    '''
    report_configurations_MultiTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                                      name_folder_report=REPORT_FOLDER_NAME, name_files_output="overall_report")

    report_stockseries_MultiTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
                                   name_folder_report=REPORT_FOLDER_NAME, name_files_output="report",
                                   original_datapath=DATA_PATH,
                                   features_to_exclude_from_scaling=features_to_exclude_from_scaling)
    '''
    return