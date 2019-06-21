import numpy as np
import pandas as pd
from keras import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM, Dropout, Dense
from keras.optimizers import Adam
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler


def prepare_input_forecasting(path_series, features_to_exclude):
    data = pd.read_csv(path_series, sep=',')
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    features = data.columns
    # print(features)
    features = [f for f in features if f not in features_to_exclude]
    # print(features)
    features_without_date = [f for f in features if f != 'DateTime']
    dataset = data[features]
    scaler = MinMaxScaler()
    scaler_target_feature = MinMaxScaler()
    scaler.fit(dataset.loc[:, dataset.columns != 'DateTime'])
    # scaler_target_feature.fit(dataset.values[:, features.index('Close')].reshape(-1, 1))
    scaler_target_feature.fit(dataset.loc[:, [col for col in dataset.columns if col.startswith('Close')]])
    dataset.loc[:, dataset.columns != 'DateTime'] = scaler.transform(dataset.loc[:, dataset.columns != 'DateTime'])
    return dataset, features, features_without_date, scaler_target_feature


def fromtemporal_totensor(dataset, window_considered, output_path, output_name):
    try:
        z = np.load(output_path + "/crypto_TensorFormat_" + output_name + "_" + str(window_considered) + '.npy')
        print('Versione Tensor LSTM trovata!')
        # print("\n--- LETTO PRE-ESISTENTE\n", z, "\n---\n")
        return z
    except FileNotFoundError as e:
        print('Versione Tensor LSTM dei dati non trovata, creazione in corso...')
        # 1 array
        # con "window_considered" righe
        # "dataset.shape[1]" colonne
        z = np.zeros((1, window_considered, dataset.shape[1]))
        # per i che varia
        # da 0 fino
        # al (totale - finestra + 1)        ]
        for i in range(dataset.shape[0] - window_considered + 1):
            if i%int((dataset.shape[0] - window_considered + 1)/10)==0: print(str(int((i/(dataset.shape[0] - window_considered + 1))*100)) + "%")
            # aggiungo ad una copia di (z)
            z = np.append(z, dataset[i:i + window_considered, :].reshape(1, window_considered, dataset.shape[1]),
                          axis=0)
        output_path += "/crypto_"
        name_tensor = 'TensorFormat_' + output_name + '_' + str(window_considered)
        np.save(str(output_path + name_tensor), z[1:,:])
        # print("\n--- CREATO\n", z, "\n---\n")
        # print("\n--- LETTO\n", z[1:, :], "\n---\n")
        return z


def train_test_split_w_date(features, dataset_tensor_version, single_date):
    train = []
    test = []

    for sample in dataset_tensor_version:
        candidate = sample[-1, features.index('DateTime')]
        # print(candidate)
        candidate = pd.to_datetime(candidate)
        if candidate == pd.to_datetime(single_date):
            test.append(sample)
            # print('candidate', candidate, '--> test', single_date)
        elif candidate > pd.to_datetime(single_date):
            pass
        else:
            # print('candidate', candidate, '--> TRAIN', single_date)
            train.append(sample)

    return np.array(train), np.array(test)


def train_model(x_train, y_train, x_test, y_test, lstm_neurons, learning_rate, dropout, epochs, batch_size, dimension_last_layer,
                model_path='', model=None):
    callbacks = [
        # Early stopping sul train o validation set? pperche qui sara' allenato su un solo esempio di test,
        # quindi converrebbe controllare la train_loss (loss)
        EarlyStopping(monitor='loss', patience=4),
        ModelCheckpoint(
            # lo stesso qui, modificato il monitor da val_loss a loss (?)
            monitor='loss', save_best_only=True,
            filepath=model_path + 'lstm_neur{}-do{}-ep{}-bs{}.h5'.format(
                lstm_neurons, dropout, epochs, batch_size))
    ]
    if model is None:
        model = Sequential()
        model.add(LSTM(lstm_neurons, input_shape=(x_train.shape[1], x_train.shape[2])))
        model.add(Dropout(dropout))
        model.add(Dense(dimension_last_layer))
        adam=Adam(lr=learning_rate)
        model.compile(loss='mean_squared_error', optimizer=adam, metrics=['acc', 'mae'])

    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                        verbose=0, shuffle=False, callbacks=callbacks)
    return model, history


def get_RMSE(y, prediction):
    return np.math.sqrt(mean_squared_error(y, prediction))

# TODO - hard constraint
def getNames(path_data, name_columns):
    dataset = pd.read_csv(path_data, sep=',')
    names = []
    for n in name_columns:
        if str(dataset[n][0]) == "USD":
            names.append("BTC")
        else:
            names.append(dataset[n][0])
    return names
