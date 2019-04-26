import numpy as np
import pandas as pd
from keras import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM, Dropout, Dense
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler


def prepare_input_forecasting(path_series_with_indicators, features_to_exclude):
    data = pd.read_csv(path_series_with_indicators, sep=',')
    data['Date'] = pd.to_datetime(data['Date'])
    features = data.columns
    features = [f for f in features if f not in features_to_exclude]
    features_without_date = [f for f in features if f != 'Date']
    dataset = data[features]
    scaler = MinMaxScaler()
    scaler_target_feature = MinMaxScaler()
    scaler.fit(dataset.loc[:, dataset.columns != 'Date'])
    scaler_target_feature.fit(dataset.values[:, features.index('PriceOfLastTransaction')].reshape(-1, 1))
    dataset.loc[:, dataset.columns != 'Date'] = scaler.transform(dataset.loc[:, dataset.columns != 'Date'])
    return dataset, features, features_without_date, scaler_target_feature


def fromtemporal_totensor(dataset, window_considered, output_path, output_name):
    try:
        print('Versione supervisionata trovata!')
        z = np.load(output_path + "/TensorFormat_" + output_name + "_" + str(window_considered) + '.npy')
        return z
    except FileNotFoundError as e:
        print('Versione supervisionata del dataset non trovata, creazione in corso...')
        z = np.zeros((1, window_considered, dataset.shape[1]))
        for i in range(dataset.shape[0] - window_considered + 1):
            z = np.append(z, dataset[i:i + window_considered, :].reshape(1, window_considered, dataset.shape[1]),
                          axis=0)
        output_path += "/"
        name_tensor = 'TensorFormat_' + output_name + '_' + str(window_considered)
        np.save(str(output_path + name_tensor), z)
        return z[1:, :]


def train_test_split_w_date(features, dataset_tensor_version, single_date):
    train = []
    test = []

    for sample in dataset_tensor_version:
        candidate = sample[-1, features.index('Date')]
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


def train_model(x_train, y_train, x_test, y_test, lstm_neurons, dropout, epochs, batch_size, model_path='', model=None):
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
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc', 'mae'])
        history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                            verbose=1, shuffle=False, callbacks=callbacks)
    else:
        history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
                            verbose=1, shuffle=False, callbacks=callbacks)
    return model, history


def get_RMSE(y, prediction):
    return np.math.sqrt(mean_squared_error(y, prediction))
