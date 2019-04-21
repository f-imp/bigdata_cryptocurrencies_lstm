import pandas as pd
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
    return dataset, features_without_date, scaler_target_feature
