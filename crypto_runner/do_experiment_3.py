#cancellare crypto_expreriment_three prima di runnare


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from itertools import product
from crypto_utility import test_set, experiments

np.random.seed(0)


EXPERIMENT = "../crypto_experiment_three"
TENSOR_PATH = "../crypto_TensorData"
RESULT_PATH = "crypto_Result"
DATA_PATH = "../crypto_preprocessing/step5_horizontal/"
REPORT_FOLDER_NAME = "Report"

# Parameters of experiments
series = os.listdir(DATA_PATH)
temporal_sequence_considered = [30, 100, 200]
number_neurons_LSTM = [32,64,128, 256, 512, 1024]
Testing_Set = test_set.get_testset("../crypto_testset/from_2017_06_26_until_2017_06_26/test_set.txt")
features_to_exclude_from_scaling = ['Symbol_1','Symbol_2','Symbol_3','Symbol_4','Symbol_5','Symbol_6','Symbol_7','Symbol_8','Symbol_9','Symbol_10']

# Create Structure of Folder - according to defined path
os.mkdir(EXPERIMENT)

os.makedirs(TENSOR_PATH, exist_ok=True)

os.mkdir(EXPERIMENT + "/" + RESULT_PATH)

for s in series:
    stock_name = s.replace(".csv", "")
    # for each stock
    # create a folder for data
    os.makedirs(TENSOR_PATH + "/" + stock_name, exist_ok=True)
    # create a folder for results
    os.mkdir(EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name)
    data_compliant, features, features_without_date, scaler = experiments.prepare_input_forecasting(DATA_PATH + "/" + s,
                                                                                                    features_to_exclude_from_scaling)
    target_indexes_without_date = [features_without_date.index(f) for f in features_without_date if
                                   f.startswith('Close')]
    for temporal, neurons in product(temporal_sequence_considered, number_neurons_LSTM):
        dataset_tensor = experiments.fromtemporal_totensor(np.array(data_compliant), temporal,
                                                           TENSOR_PATH + "/" + stock_name + "/",
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
        for data_tester in Testing_Set:
            train, test = experiments.train_test_split_w_date(features, dataset_tensor, data_tester)
            train = train[:, :, 1:]
            test = test[:, :, 1:]

            x_train, y_train = train[:, :-1, :], train[:, -1, target_indexes_without_date]
            x_test, y_test = test[:, :-1, :], test[:, -1, target_indexes_without_date]

            # Fare il training
            if data_tester == Testing_Set[0]:
                model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                         dropout=0.2,
                                                         epochs=100,
                                                         batch_size=256,
                                                         dimension_last_layer=10,
                                                         model_path=EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + best_model + "/")
            else:
                model, history = experiments.train_model(x_train, y_train, x_test, y_test, lstm_neurons=neurons,
                                                         dropout=0.2,
                                                         epochs=100,
                                                         batch_size=256, dimension_last_layer=10, model=model,
                                                         model_path=EXPERIMENT + "/" + RESULT_PATH + "/" + stock_name + "/" + configuration_name + "/" + best_model + "/")

            # Tiriamo fuori la predizione per ogni esempio di test
            test_prediction = model.predict(x_test)
            rmse = experiments.get_RMSE(y_test, test_prediction)
            y_test_denorm = scaler.inverse_transform(y_test.reshape(-1,10))

            test_prediction_denorm = scaler.inverse_transform(test_prediction)
            rmse_denorm = experiments.get_RMSE(y_test_denorm, test_prediction_denorm)
            '''
            y_test = float(y_test)
            test_prediction = float(test_prediction)
            y_test_denorm = float(y_test_denorm)
            test_prediction_denorm = float(test_prediction_denorm)
            '''

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


def seq_matrix_mult(data, window, csv_name):
    path = 'data/supervised_style/'
    os.makedirs(path, exist_ok=True)

    print(data[0, 0])
    try:
        print(path + csv_name.replace('.csv','') + '_ts' + str(window)+ '.npy')
        z = np.load(path + csv_name.replace('.csv','') + '_ts' + str(window)+ '.npy')
        return z
    except FileNotFoundError as e:
        print('Versione supervisionata del dataset non trovata, creazione in corso...')
        z = np.zeros((1, window, data.shape[1]))
        for i in range(data.shape[0] - window + 1):
            z = np.append(z, data[i:i+window, :].reshape(1, window, data.shape[1]), axis=0)
        z = z[1:, :]
        np.save(path + csv_name.replace('.csv','') + '_ts' + str(window), z)
        return z

'''
stock_id = 'horizontal'
csv_name = stock_id + '.csv'
df = pd.read_csv('data/'+csv_name, sep=',', decimal='.')
df = df.fillna(0)
df['DateTime'] = pd.to_datetime(df['DateTime'], dayfirst=True)
df.sort_values('DateTime', inplace=True)

features = df.columns
to_exclude = ['Symbol']
#to_exclude = ['stock_id', 'ChangePercentage', 'TradedQuantity', 'TotalTradedVolumeIncludingBlocks']
excluded_features = [f for f in features if f.startswith(tuple(to_exclude))]
features = [f for f in features if f not in excluded_features]
features_without_date = [f for f in features if f != 'DateTime']
dataset = df[features]
target_indexes_without_date = [features_without_date.index(f) for f in features_without_date if f.startswith('Close')]

target_stock_names =  df.loc[0, [f for f in df.columns if f.startswith('stock_id')]]

scaler = MinMaxScaler()
scaler_target_feature = MinMaxScaler()

scaler.fit(dataset.loc[:, dataset.columns != 'DateTime'])
scaler_target_feature.fit(dataset.loc[:, [col for col in dataset.columns if col.startswith('Close')]])

dataset.loc[:, dataset.columns != 'DateTime'] = scaler.transform(dataset.loc[:, dataset.columns != 'DateTime'])

ts_params = [30, 100, 200]
lstm_neur_params = [128, 256]
for ts, lstm_n in product(ts_params,  lstm_neur_params):
    print('lstm_neurons', lstm_n, 'timesequence', ts)
    config_path = 'results-S3/{}/ts{}_lstm_neurons{}/'.format(stock_id, ts, lstm_n)

    timesequence = ts
    dataset_supervised_style = seq_matrix_mult(np.array(dataset),timesequence, csv_name=csv_name)
    print(dataset_supervised_style.shape)

    predictions_file = {'stock_id':[], 'date':[], 'observed_norm':[], 'predicted_norm':[], 'observed_denorm':[],
                        'predicted_denorm':[]}
    errors_file = {'stock_id':[], 'date':[], 'rmse_norm': [], 'rmse_denorm':[]}
    for td in test_dates:
        train, test = train_test_split_w_date(dataset_supervised_style, td)
        # Rimuovo la prima componente della terza dimensione che contiene la data, non normalizzabile e utilizzabile per il training
        train = train[:, :, 1:]
        test = test[:, :, 1:]

        #print(train.shape)
        #print(test.shape)

        x_train, y_train = train[:, :-1, :], train[:, -1, target_indexes_without_date]
        x_test, y_test = test[:, :-1, :], test[:, -1, target_indexes_without_date]

        # Fare il training
        if td == test_dates[0]:
            model, history = train_model(x_train, y_train, x_test, y_test, lstm_neurons=lstm_n, dropout=0.2, epochs=100,
                                            batch_size=256, model_path=config_path)
        else:
            model, history = train_model(x_train, y_train, x_test, y_test, lstm_neurons=lstm_n, dropout=0.2, epochs=100,
                                            batch_size=256, model=model, model_path=config_path)


        # Tiriamo fuori la predizione per ogni esempio di test
        test_prediction = model.predict(x_test)
        rmse = get_RMSE(y_test, test_prediction)
        y_test_denorm = scaler_target_feature.inverse_transform(y_test.reshape(-1,))
        test_prediction_denorm =  scaler_target_feature.inverse_transform(test_prediction)
        rmse_denorm = get_RMSE(y_test_denorm, test_prediction_denorm)

        # Scrivo su file i risultati
        predictions_file['stock_id'].append(stock_id + str(target_stock_names))
        predictions_file['date'].append(td)
        predictions_file['observed_norm'].append(y_test)
        predictions_file['predicted_norm'].append(test_prediction)
        predictions_file['observed_denorm'].append(y_test_denorm)
        predictions_file['predicted_denorm'].append(test_prediction_denorm)

        errors_file['stock_id'].append(stock_id)
        errors_file['date'].append(td)
        errors_file['rmse_norm'].append(rmse)
        errors_file['rmse_denorm'].append(rmse_denorm)

    os.makedirs(config_path, exist_ok=True)
    pd.DataFrame(data = predictions_file).to_csv(config_path+'predictions.csv')
    pd.DataFrame(data = errors_file).to_csv(config_path+'errors.csv')
'''


