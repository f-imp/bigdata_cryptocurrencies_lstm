import math
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
import pandas as pd
import os
from statsmodels.tsa.api import VAR
import warnings

warnings.filterwarnings("ignore")

# # Utility functions
def str_to_datetime(inp_dt):
    # return dt.strptime(inp_dt, '%Y-%m-%d')
    return dt.strptime(inp_dt, '%d/%m/%y')

def str_to_datetime2(inp_dt):
    return dt.strptime(inp_dt, '%Y-%m-%d')

def datetime_to_str(inp_dt):
    return inp_dt.strftime('%Y-%m-%d')
    # return inp_dt.strftime('%d/%m/%y')

def datetime_to_str2(inp_dt):
    return inp_dt.strftime('%d/%m/%y')

def scale_data(old_val, old_min, old_max, new_min, new_max):
    return float((((old_val - old_min)/(old_max - old_min)) * (new_max - new_min)) + new_min)

# def check_date_exist(dt_to_check):
#     return True if dt_to_check in timeframe_list_dt else False
def check_date_exist(dt_to_check):
    return True # modificare becera che non controlla la data da testare

#timeframe_list = ['2016-03-08', '2016-10-05', '2016-04-13', '2016-10-20', '2016-07-28', '2017-04-06', '2017-11-07', '2016-02-23', '2016-08-02', '2017-07-31', '2017-07-19', '2016-10-04', '2017-07-18', '2017-06-30', '2016-11-03', '2017-03-29', '2017-04-21', '2016-05-23', '2016-10-14', '2017-10-05', '2016-02-11', '2016-05-18', '2017-02-06', '2017-01-23', '2017-04-05', '2017-03-14', '2016-12-27', '2016-01-15', '2017-06-08', '2017-04-28', '2016-01-28', '2016-01-19', '2016-05-19', '2016-02-24', '2016-06-17', '2016-05-27', '2017-07-06', '2016-03-01', '2016-02-09', '2016-07-20', '2016-11-14', '2017-02-21', '2017-06-20', '2017-03-16', '2017-02-02', '2016-02-02', '2016-06-30', '2017-05-16', '2017-10-23', '2017-06-28', '2016-08-05', '2017-03-09', '2016-06-20', '2016-11-28', '2016-11-04', '2017-05-10', '2016-07-18', '2017-02-07', '2016-04-04', '2017-04-20', '2016-03-04', '2016-04-25', '2016-11-16', '2016-03-22', '2017-01-20', '2016-09-27', '2017-11-02', '2017-05-15', '2016-12-28', '2017-01-31', '2017-08-08', '2017-02-01', '2016-07-27', '2016-02-29', '2016-10-25', '2016-02-17', '2016-03-09', '2016-01-13', '2016-12-29', '2016-04-11', '2017-02-24', '2016-01-08', '2017-05-11', '2017-04-10', '2017-03-10', '2017-05-26', '2016-09-09', '2017-08-14', '2016-02-22', '2017-09-01', '2016-03-30', '2017-08-25', '2017-03-23', '2017-06-07', '2016-07-14', '2016-07-08', '2017-03-20', '2017-03-13', '2016-12-30', '2017-09-07', '2016-09-19', '2017-09-14', '2016-09-23', '2017-03-03', '2017-01-05', '2017-07-21', '2017-06-02', '2017-08-18', '2017-03-27', '2017-02-17', '2016-11-02', '2017-06-16', '2017-01-25', '2017-09-18', '2016-12-15', '2016-07-11', '2017-10-30', '2017-02-13', '2016-04-12', '2017-03-28', '2017-10-31', '2016-11-18', '2016-06-06', '2016-01-29', '2016-05-12', '2017-05-03', '2016-11-29', '2017-01-10', '2017-09-27', '2017-02-23', '2016-04-22', '2016-01-07', '2016-03-21', '2016-02-16', '2017-05-31', '2016-10-27', '2016-06-16', '2017-01-24', '2017-07-07', '2016-12-23', '2017-02-14', '2016-01-27', '2016-07-05', '2016-06-24', '2017-06-01', '2017-09-19', '2017-01-06', '2016-07-25', '2017-02-08', '2017-08-01', '2016-12-20', '2016-10-31', '2016-08-15', '2016-01-25', '2016-06-01', '2016-05-25', '2016-08-10', '2017-06-12', '2017-10-27', '2016-03-11', '2016-09-16', '2016-10-06', '2017-09-11', '2016-06-28', '2016-11-21', '2016-02-25', '2016-12-02', '2017-05-04', '2017-01-19', '2016-05-06', '2017-09-28', '2017-08-17', '2016-08-26', '2016-08-16', '2016-03-07', '2017-08-24', '2017-02-10', '2016-04-15', '2016-01-20', '2016-09-15', '2016-08-01', '2017-06-29', '2016-08-25', '2017-01-30', '2016-03-29', '2017-08-22', '2016-03-24', '2016-12-21', '2016-03-10', '2016-11-17', '2016-12-07', '2017-06-23', '2017-08-03', '2017-03-06', '2017-06-21', '2016-01-05', '2017-02-16', '2016-04-21', '2017-01-12', '2017-03-08', '2017-09-06', '2017-01-04', '2016-05-10', '2017-07-17', '2016-08-11', '2017-08-04', '2017-02-03', '2017-05-25', '2017-08-23', '2017-10-25', '2016-07-21', '2017-05-17', '2017-07-14', '2016-12-12', '2016-07-22', '2016-09-22', '2016-09-08', '2016-02-10', '2016-08-31', '2017-02-22', '2017-10-24', '2016-01-21', '2016-08-24', '2016-09-26', '2017-11-06', '2017-03-22', '2017-08-10', '2016-07-12', '2016-02-12', '2016-10-17', '2016-10-18', '2016-06-29', '2017-05-23', '2016-06-21', '2016-09-06', '2017-10-16', '2017-03-17', '2017-04-18', '2017-11-08', '2017-07-27', '2017-03-24', '2016-09-30', '2017-04-11', '2017-10-06', '2017-08-29', '2016-02-19', '2016-06-09', '2017-10-18', '2016-11-22', '2016-03-17', '2017-06-06', '2016-03-14', '2017-06-26', '2017-10-13', '2016-05-13', '2016-04-18', '2016-03-15', '2017-04-17', '2016-04-29', '2017-06-09', '2017-01-18', '2017-09-21', '2016-07-15', '2016-10-07', '2016-12-13', '2017-05-22', '2016-04-28', '2016-09-02', '2016-06-27', '2017-06-22', '2016-08-17', '2017-04-25', '2016-11-30', '2017-10-26', '2017-05-19', '2017-05-05', '2017-04-24', '2016-03-02', '2017-09-12', '2016-02-18', '2017-07-12', '2017-08-02', '2017-01-09', '2017-03-30', '2017-05-18', '2017-03-02', '2017-05-30', '2016-05-02', '2016-08-30', '2016-06-07', '2016-08-29', '2016-07-19', '2016-09-07', '2016-12-05', '2017-10-20', '2016-02-01', '2016-05-26', '2016-09-28', '2016-07-29', '2017-02-28', '2016-06-10', '2016-06-23', '2016-12-14', '2016-10-24', '2017-02-27', '2016-10-13', '2017-05-12', '2016-10-11', '2016-09-14', '2017-01-17', '2017-04-12', '2016-05-24', '2017-09-08', '2017-06-14', '2017-01-26', '2017-08-28', '2017-06-05', '2017-04-03', '2017-10-10', '2016-02-04', '2017-08-21', '2017-05-24', '2017-05-09', '2017-09-15', '2017-09-29', '2017-03-01', '2016-09-01', '2016-12-08', '2016-10-21', '2017-07-25', '2017-08-30', '2016-04-07', '2016-08-03', '2017-06-19', '2016-02-26', '2017-07-05', '2016-05-05', '2016-07-01', '2017-07-28', '2017-09-05', '2016-08-18', '2017-09-13', '2016-05-09', '2016-06-08', '2016-11-23', '2017-04-19', '2017-10-19', '2016-07-26', '2017-07-10', '2016-07-07', '2016-11-15', '2017-11-01', '2016-09-20', '2017-10-03', '2016-03-23', '2017-10-17', '2016-05-11', '2017-10-12', '2016-02-08', '2016-06-13', '2017-09-20', '2017-02-09', '2016-12-22', '2016-05-04', '2016-12-19', '2017-04-04', '2017-05-01', '2017-08-07', '2016-05-03', '2016-10-19', '2017-10-09', '2016-08-04', '2016-12-16', '2016-11-11', '2017-01-03', '2016-11-08', '2016-05-16', '2016-01-14', '2016-05-31', '2017-10-04', '2016-11-09', '2017-03-15', '2016-04-26', '2016-06-03', '2016-01-06', '2017-03-31', '2016-09-21', '2017-09-26', '2016-04-20', '2016-10-12', '2017-01-13', '2017-10-02', '2016-05-20', '2017-03-07', '2016-12-09', '2016-04-05', '2016-06-22', '2016-04-19', '2016-01-26', '2016-10-03', '2017-08-31', '2017-04-26', '2016-05-17', '2016-06-02', '2017-07-20', '2017-07-24', '2016-04-08', '2017-11-03', '2016-06-14', '2016-10-26', '2016-10-10', '2016-12-01', '2017-06-13', '2016-08-12', '2016-10-28', '2016-04-27', '2016-09-13', '2016-11-07', '2017-04-13', '2016-02-05', '2017-01-11', '2017-09-22', '2017-06-15', '2017-10-11', '2016-07-06', '2016-03-28', '2016-01-11', '2017-07-13', '2016-07-13', '2017-01-27', '2016-08-08', '2017-07-03', '2016-04-14', '2017-08-09', '2016-01-12', '2016-03-16', '2016-08-09', '2016-11-10', '2016-09-29', '2017-08-16', '2016-12-06', '2016-11-01', '2016-02-03', '2017-03-21', '2016-01-22', '2017-02-15', '2016-04-01', '2016-03-03', '2017-06-27', '2016-11-25', '2017-09-25', '2017-07-11', '2017-05-02', '2016-08-22', '2017-08-11', '2016-04-06', '2017-04-27', '2017-05-08', '2016-03-18', '2017-04-07', '2016-08-23', '2016-01-04', '2017-08-15', '2016-09-12', '2017-07-26', '2016-08-19', '2016-03-31', '2016-06-15']
def get_test_dates(path):
    import ast
    with open(path) as td:
        test_dates = td.read()
    test_dates = ast.literal_eval(test_dates)
    #test_dates = np.array(pd.to_datetime(test_dates, yearfirst=True))
    return test_dates

#timeframe_list_dt = [str_to_datetime(elem) for elem in timeframe_list]

out_path = 'results/'
partial_folder="predictions"
final_folder="RMSE"


try:
    os.mkdir(out_path)
except OSError:
    print("Creation of the directory %s failed" % out_path)
else:
    print("Successfully created the directory %s " % out_path)

try:
    os.mkdir(os.path.join(out_path,partial_folder))
except OSError:
    print("Creation of the directory %s failed" % partial_folder)
else:
    print("Successfully created the directory %s " % partial_folder)

try:
    os.mkdir(os.path.join(out_path,final_folder))
except OSError:
    print("Creation of the directory %s failed" % final_folder)
else:
    print("Successfully created the directory %s " % final_folder)

dates_to_use = get_test_dates('../../crypto_testset/from_2016_07_01_until_2017_06_26/test_set.txt')

csv="../../crypto_preprocessing/step5_horizontal/horizontal.csv"


stock_df = pd.read_csv(csv, sep=',', decimal='.', header=0)
stock_df['DateTime'] = stock_df['DateTime'].apply(lambda x: str_to_datetime2(x))
stock_df.set_index('DateTime', inplace=True)
stock_df.sort_index(inplace=True)

print(stock_df.columns)
print(stock_df.index)
features = stock_df.columns
features = [f for f in features if f.startswith('Close')]
new_model = stock_df[features]
new_model = new_model.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
print(new_model.head())
print('features:', len(features))
print('sono:', features)




for date_pred in dates_to_use:

    try:
        test_tf = str_to_datetime2(date_pred)
        train_tf = test_tf - timedelta(days=1)

        if not check_date_exist(train_tf):
            train_tf = train_tf - timedelta(days=1)

            if not check_date_exist(train_tf):
                train_tf = train_tf - timedelta(days=1)

                if not check_date_exist(train_tf):
                    print('Error while trying yo get train/test timeframe.')
                    continue

        print('Last Train day: {}'.format(datetime_to_str(train_tf)))
        print('Test day: {}'.format(date_pred))

        train_model = new_model[:train_tf]
        train_model.fillna(0, inplace=True)
        y_test = new_model[test_tf:test_tf].values[0]

        model = VAR(train_model)
        results = model.fit(maxlags=3, ic='aic')
        lag_order = results.k_ar
        y_predicted = results.forecast(train_model.values[-lag_order:], 1)[0]

        os.makedirs(out_path, exist_ok=True)
        with open(os.path.join(out_path,partial_folder,'var_model_norm_{}.csv'.format(date_pred)), 'w') as vf:
            vf.write('Real,Predicted\n')
            for k in range(len(y_test)):
                vf.write('{},{}\n'.format(y_test[k], y_predicted[k]))


    except Exception as e:
        print('Error, possible cause: {}'.format(e))


errors=[]

for csv in os.listdir(os.path.join(out_path,partial_folder)):
    res = pd.read_csv(os.path.join(out_path,partial_folder,csv))
    error = res['Real'] - res['Predicted']
    sq_error = error ** 2
    errors.append(np.mean(sq_error))



with open(os.path.join(out_path,final_folder,"RMSE.txt"), 'w+') as out:
    final = math.sqrt(np.mean(errors))
    out.write(str(final))