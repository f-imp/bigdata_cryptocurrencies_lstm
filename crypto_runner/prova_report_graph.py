import os

# EXPERIMENT ONE
# ------------------------------------------------------------------------------------------------------------------------
from itertools import product

import numpy
import pandas as pd

import matplotlib.pyplot as plt
from crypto_utility.report_data import report_configurations_SingleTarget, report_stockseries_SingleTarget, \
    report_configurations_MultiTarget, report_stockseries_MultiTarget

# EXPERIMENT = "../SingleTarget_Data"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "Result"
# DATA_PATH = "../crypto_preprocessing/step2_normalized/"
# REPORT_FOLDER_NAME = "Report"
#
# temporal_sequence_considered = [30, 100, 200]
# number_neurons_LSTM = [128, 256]
#
# report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence_considered,
#                                    neurons_used=number_neurons_LSTM,
#                                    name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                    name_folder_report=REPORT_FOLDER_NAME, name_output_files="report_all_configurations")
#
# report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                 name_folder_report=REPORT_FOLDER_NAME,
#                                 name_files_output="report_single_stock")
#
# # EXPERIMENT TWO
# # ------------------------------------------------------------------------------------------------------------------------
#
# EXPERIMENT = "../SingleTarget_Data_with_Indicators"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "Result"
# DATA_PATH = "../crypto_preprocessing/step3_alldata/"
# REPORT_FOLDER_NAME = "Report"
#
# temporal_sequence_considered = [30, 100, 200]
#
# report_configurations_SingleTarget(temporal_sequence_used=temporal_sequence_considered,
#                                    neurons_used=number_neurons_LSTM,
#                                    name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                    name_folder_report=REPORT_FOLDER_NAME, name_output_files="report_all_configurations")
#
# report_stockseries_SingleTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                 name_folder_report=REPORT_FOLDER_NAME,
#                                 name_files_output="report_single_stock")

# EXPERIMENT THREE
# ------------------------------------------------------------------------------------------------------------------------
# EXPERIMENT = "../MultiTarget_Data"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "Result"
# DATA_PATH = "../crypto_preprocessing/step5_horizontal/"
# MULTI_features_to_exclude_from_scaling = ['Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6',
#                                           'Symbol_7', 'Symbol_8']
# REPORT_FOLDER_NAME = "Report"
#
# report_configurations_MultiTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                   name_folder_report=REPORT_FOLDER_NAME, name_files_output="report_all_configurations")
#
# report_stockseries_MultiTarget(name_folder_experiment=EXPERIMENT,
#                                name_folder_result_experiment=RESULT_PATH,
#                                name_folder_report=REPORT_FOLDER_NAME, name_files_output="report",
#                                original_datapath=DATA_PATH,
#                                features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling)
#
# # EXPERIMENT FOUR
# # ------------------------------------------------------------------------------------------------------------------------
# EXPERIMENT = "../MultiTarget_Data_with_Indicators"
# TENSOR_PATH = "../crypto_TensorData"
# RESULT_PATH = "Result"
# DATA_PATH = "../crypto_preprocessing/step5_horizontal/"
# REPORT_FOLDER_NAME = "Report"
#
# report_configurations_MultiTarget(name_folder_experiment=EXPERIMENT, name_folder_result_experiment=RESULT_PATH,
#                                   name_folder_report=REPORT_FOLDER_NAME, name_files_output="report_all_configurations")
#
# report_stockseries_MultiTarget(name_folder_experiment=EXPERIMENT,
#                                name_folder_result_experiment=RESULT_PATH,
#                                name_folder_report=REPORT_FOLDER_NAME, name_files_output="report",
#                                original_datapath=DATA_PATH,
#                                features_to_exclude_from_scaling=MULTI_features_to_exclude_from_scaling)


# percorso = "../SingleTarget_Data/Result/XMR/LSTM_128_neurons_30_days/stats/predictions.csv"
# prediction_file = pd.read_csv(percorso)
# print(prediction_file)
# date = numpy.array(prediction_file["date"])
# predict = numpy.array(prediction_file["predicted_norm"])
# real = numpy.array(prediction_file["observed_norm"])
#
# print(len(date))


# Single
# per ogni stock - configurazioni


# 8 file csv (1 per ogni stock)
# nome stock | Data | exp_name | Neurons | days | Reale | Predetto

# os.makedirs("../FINAL/", exist_ok=True)
# dizionario = {"cryptostock_name": [], "date": [], "model": [], "neurons": [], "days": [],
#               "real_value": [],
#               "predicted_value": []}
stocks_data_path = "../crypto_preprocessing/step0_data/"
#
# # Lista nomi stocks
stocks_name = []
for name in os.listdir(stocks_data_path):
    stocks_name.append(name.replace(".csv", ""))
#
# # Lista Cartelle esperimenti
exp_performed = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators", "MultiTarget_Data",
                 "MultiTarget_Data_with_Indicators"]


# # per ogni stock
# #   per ogni cartella exp - Result
# #       se ST:
# #           apro predictions.csv
# #           salvo nel dizionario tutti i valori
# #       se MT:
# #           apro predictions.csv
# #           salvo nel dizionario i valori (colonna dello stock esaminato)
#
#
# for e in exp_performed:
#     print(e)
#     if "SingleTarget" in e:
#         x = 1
#         stocks_folders = os.listdir("../" + e + "/Result/")
#         for each_folder in stocks_folders:
#             print(each_folder)
#             configurations_tested = os.listdir("../" + e + "/Result/" + each_folder + "/")
#             for each_conf in configurations_tested:
#                 print(each_conf)
#                 nn = each_conf.split("_")[1]
#                 dd = each_conf.split("_")[3]
#                 print("..lettura..")
#                 if "with_Indicators" in e:
#                     s = each_folder.replace("_with_indicators", "")
#                 else:
#                     s = each_folder
#                 predictions_file = pd.read_csv(
#                     "../" + e + "/Result/" + each_folder + "/" + each_conf + "/stats/predictions.csv")
#                 for d, r, p in zip(predictions_file["date"], predictions_file["observed_norm"],
#                                    predictions_file["predicted_norm"]):
#                     dizionario["cryptostock_name"].append(str(s))
#                     dizionario["date"].append(d)
#                     dizionario["model"].append(str(e))
#                     dizionario["neurons"].append(int(nn))
#                     dizionario["days"].append(int(dd))
#                     dizionario["real_value"].append(float(r))
#                     dizionario["predicted_value"].append(float(p))
#     elif "MultiTarget" in e:
#         x = 1
#         configurations_tested = os.listdir("../" + e + "/Result/")
#         for each_conf in configurations_tested:
#             print(each_conf)
#             nn = each_conf.split("_")[1]
#             dd = each_conf.split("_")[3]
#             for s in stocks_name:
#                 print(s)
#                 predictions_file = pd.read_csv(
#                     "../" + e + "/Result/" + each_conf + "/stats/predictions.csv")
#                 for d, r, p in zip(predictions_file["date"], predictions_file[str(s) + "_observed_norm"],
#                                    predictions_file[str(s) + "_predicted_norm"]):
#                     dizionario["cryptostock_name"].append(str(s))
#                     dizionario["date"].append(d)
#                     dizionario["model"].append(str(e))
#                     dizionario["neurons"].append(int(nn))
#                     dizionario["days"].append(int(dd))
#                     dizionario["real_value"].append(float(r))
#                     dizionario["predicted_value"].append(float(p))
# pd.DataFrame(dizionario).to_csv("../FINAL/all.csv", index_label=False, index=False)

# data_final = pd.read_csv("../FINAL/all.csv")
# print(data_final.shape)
# btc = data_final[data_final["cryptostock_name"] == "BTC"]
# print("DOGE ->", btc.shape, "\t", type(btc))
# v2 = btc[(btc["neurons"] == 128) & (btc["model"] == "SingleTarget_Data")]
# print("V2-> ", v2.shape)
# print(v2)


def plot_graphs(input_data, list_crypto, list_model, list_neurons, list_days, output_path):
    data = pd.read_csv(input_data)

    for name, neurons, days in product(list_crypto, list_neurons, list_days):
        data_cutted = data[(data["cryptostock_name"] == name) & (data["neurons"] == neurons) & (data["days"] == days)]
        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        max_values = []
        labels = []
        for (m, i) in zip(list_model, range(0, len(list_model), 1)):
            data_cutted_model_oriented = data_cutted[data["model"] == m]
            if (i == 0):
                ax.plot(range(0, len(data_cutted_model_oriented["date"]), 1),
                        data_cutted_model_oriented["real_value"])
                max_values.append(max(data_cutted_model_oriented["real_value"]))
                labels.append("REAL")
            ax.plot(range(0, len(data_cutted_model_oriented["date"]), 1),
                    data_cutted_model_oriented["predicted_value"])
            max_values.append(max(data_cutted_model_oriented["predicted_value"]))
            labels.append("PREDICTED_" + str(m))
        max_abs = max(max_values)
        plt.title(str(name) + " - #Neurons:" + str(neurons) + " - Previous days:" + str(days))
        plt.xticks(numpy.arange(12), data_cutted_model_oriented["date"], rotation=65)
        plt.yticks(numpy.arange(0.0, max_abs, (max_abs / 100 * 5)))
        plt.ylabel('Value')
        plt.legend(labels, loc=4)
        plt.grid()
        fig.tight_layout()
        name_fig = str(name) + "_" + str(neurons) + "_" + str(days)
        fig.savefig(output_path + name_fig + ".png")

    # for crypto in list_crypto:
    #     data_cut2 = data[data["cryptostock_name"] == crypto]
    #     for m in list_model:
    #         data_cut3 = data_cut2[data_cut2["model"] == m]
    #         for nn in list_neurons:
    #             data_cut4 = data_cut3[data_cut3["neurons"] == nn]
    #             for dd in list_days:
    #                 data_cut5 = data_cut4[data_cut4["days"] == dd]
    #                 # print(data_cut5)
    #                 fig = plt.figure(figsize=(18, 12))
    #                 line_chart_p = plt.plot(range(0, len(data_cut5["date"]), 1), data_cut5["predicted_value"])
    #                 line_chart_r = plt.plot(range(0, len(data_cut5["date"]), 1), data_cut5["real_value"])
    #                 plt.title(crypto + " " + str(m) + "\n" + "[" + str(nn) + "#Hidden Neurons \n" + str(
    #                     dd) + "Previous Days considered]")
    #                 plt.xlabel('Test Date')
    #                 max1 = max(data_cut5["predicted_value"])
    #                 max2 = max(data_cut5["real_value"])
    #                 maximum = max(max1, max2)
    #                 plt.xticks(numpy.arange(12), data_cut5["date"], rotation=65)
    #                 plt.yticks(numpy.arange(0.0, maximum, 0.05))
    #                 plt.ylabel('Value')
    #                 plt.legend(['prediction', 'real'], loc=4)
    #                 plt.grid()
    #                 fig.tight_layout()
    #                 # plt.show()
    #                 name_fig = str(crypto) + "_" + str(m) + "_" + str(nn) + "_" + str(dd)
    #                 fig.savefig(output_path + name_fig + ".png")
    return


lista_single = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators"]
lista_multi = ["MultiTarget_Data", "MultiTarget_Data_with_Indicators"]
lista_without = ["SingleTarget_Data", "MultiTarget_Data"]
lista_with = ["SingleTarget_Data_with_Indicators", "MultiTarget_Data_with_Indicators"]
l_crypto = ["BTC"]
l_nn = [256]
l_dd = [30, 200]
plot_graphs("../FINAL/all.csv", l_crypto, lista_with, l_nn, l_dd, "../FINAL/")
