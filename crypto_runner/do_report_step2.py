import os
from itertools import product

import numpy
import pandas as pd
import matplotlib.pyplot as plt


def plot_graphs(input_data, list_crypto, list_model, list_neurons, list_days, output_path):
    data = pd.read_csv(input_data)

    for name, neurons, days in product(list_crypto, list_neurons, list_days):
        data_cutted = data[(data["cryptostock_name"] == name) & (data["neurons"] == neurons) & (data["days"] == days)]
        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111)
        # max_values = []
        labels = []
        for (m, i) in zip(list_model, range(0, len(list_model), 1)):
            data_cutted_model_oriented = data_cutted[data["model"] == m]
            if (i == 0):
                ax.plot(range(0, len(data_cutted_model_oriented["date"]), 1),
                        data_cutted_model_oriented["real_value"])
                # max_values.append(max(data_cutted_model_oriented["real_value"]))
                labels.append("REAL")
            ax.plot(range(0, len(data_cutted_model_oriented["date"]), 1),
                    data_cutted_model_oriented["predicted_value"])
            # max_values.append(max(data_cutted_model_oriented["predicted_value"]))
            labels.append("PREDICTED_" + str(m))
        # max_abs = max(max_values)
        plt.title(str(name) + " - #Neurons:" + str(neurons) + " - Previous days:" + str(days))
        plt.xticks(numpy.arange(12), data_cutted_model_oriented["date"], rotation=65)
        # plt.yticks(numpy.arange(0.0, max_abs, (max_abs / 100 * 5)))
        plt.ylabel('Value')
        plt.legend(labels, loc=4)
        plt.grid()
        fig.tight_layout()
        name_fig = str(name) + "_" + str(neurons) + "_" + str(days)
        fig.savefig(output_path + name_fig + ".png")
    return


# os.makedirs("../FINAL/", exist_ok=True)
#
# stocks_data_path = "../crypto_preprocessing/step0_data/"
# #
# # # Lista nomi stocks
# stocks_name = []
# for name in os.listdir(stocks_data_path):
#     stocks_name.append(name.replace(".csv", ""))
#
exp_name = ["top5Result", "top8Result"]
#
# # # Lista Cartelle esperimenti
# exp_performed = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators", "MultiTarget_Data",
#                  "MultiTarget_Data_with_Indicators"]
#
# # per ogni stock
# #   per ogni cartella exp - Result
# #       se ST:
# #           apro predictions.csv
# #           salvo nel dizionario tutti i valori
# #       se MT:
# #           apro predictions.csv
# #           salvo nel dizionario i valori (colonna dello stock esaminato)
#
# for n in exp_name:
#     dizionario = {"cryptostock_name": [], "date": [], "model": [], "neurons": [], "days": [],
#                   "real_value": [],
#                   "predicted_value": []}
#     print(n)
#     for e in exp_performed:
#         print(e)
#         # if "SingleTarget" in e:
#         x = 1
#         stocks_folders = os.listdir("../" + n + "/" + e + "/Result/")
#         for each_folder in stocks_folders:
#             print(each_folder)
#             configurations_tested = os.listdir("../" + n + "/" + e + "/Result/" + each_folder + "/")
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
#                     "../" + n + "/" + e + "/Result/" + each_folder + "/" + each_conf + "/stats/predictions.csv")
#                 for d, r, p in zip(predictions_file["date"], predictions_file["observed_norm"],
#                                    predictions_file["predicted_norm"]):
#                     dizionario["cryptostock_name"].append(str(s))
#                     dizionario["date"].append(d)
#                     dizionario["model"].append(str(e))
#                     dizionario["neurons"].append(int(nn))
#                     dizionario["days"].append(int(dd))
#                     dizionario["real_value"].append(float(r))
#                     dizionario["predicted_value"].append(float(p))
#         # elif "MultiTarget" in e:
#         #     x = 1
#         #     configurations_tested = os.listdir("../" + e + "/Result/")
#         #     for each_conf in configurations_tested:
#         #         print(each_conf)
#         #         nn = each_conf.split("_")[1]
#         #         dd = each_conf.split("_")[3]
#         #         for s in stocks_name:
#         #             print(s)
#         #             predictions_file = pd.read_csv(
#         #                 "../" + e + "/Result/" + each_conf + "/stats/predictions.csv")
#         #             for d, r, p in zip(predictions_file["date"], predictions_file[str(s) + "_observed_norm"],
#         #                                predictions_file[str(s) + "_predicted_norm"]):
#         #                 dizionario["cryptostock_name"].append(str(s))
#         #                 dizionario["date"].append(d)
#         #                 dizionario["model"].append(str(e))
#         #                 dizionario["neurons"].append(int(nn))
#         #                 dizionario["days"].append(int(dd))
#         #                 dizionario["real_value"].append(float(r))
#         #                 dizionario["predicted_value"].append(float(p))
#     pd.DataFrame(dizionario).to_csv("../FINAL/all_" + n + ".csv", index_label=False, index=False)

# for name in exp_name:
#     data_final = pd.read_csv("../FINAL/all_" + name + ".csv")
#     print(data_final.shape)
# btc = data_final[data_final["cryptostock_name"] == "BTC"]
# print("DOGE ->", btc.shape, "\t", type(btc))
# v2 = btc[(btc["neurons"] == 128) & (btc["model"] == "SingleTarget_Data")]
# print("V2-> ", v2.shape)
# print(v2)


# lista_single = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators"]
# lista_multi = ["MultiTarget_Data", "MultiTarget_Data_with_Indicators"]
# lista_without = ["SingleTarget_Data", "MultiTarget_Data"]
# lista_with = ["SingleTarget_Data_with_Indicators", "MultiTarget_Data_with_Indicators"]
# lista_all = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators", "MultiTarget_Data",
#              "MultiTarget_Data_with_Indicators"]

lista_single = ["SingleTarget_Data"]
lista_multi = ["MultiTarget_Data"]
lista_single_ind = ["SingleTarget_Data_with_Indicators"]
lista_multi_ind = ["MultiTarget_Data_with_Indicators"]
lista_all = ["SingleTarget_Data", "SingleTarget_Data_with_Indicators", "MultiTarget_Data",
             "MultiTarget_Data_with_Indicators"]

dizionario_report_linechart = {"single": lista_single, "single_ind": lista_single_ind, "multi": lista_multi,
                               "multi_ind": lista_multi_ind}

# dizionario_report_linechart_v2 = {"all": lista_all}
#
# dizionario_report_linechart_v3 = {"Single": "SingleTarget_Data",
#                                   "SingleIndicators": "SingleTarget_Data_with_Indicators", "Multi": "MultiTarget_Data",
#                                   "MultiIndicators": "MultiTarget_Data_with_Indicators"}

top8 = ["BTC", "XRP", "LTC", "XLM", "XMR", "DASH", "XEM", "DOGE"]  # Top8
top5 = ["BTC", "LTC", "XLM", "DASH", "DOGE"]  # Top5

l_nn = [128, 256]
l_dd = [30, 100, 200]

for name in exp_name:
    print(name)
    data_final = pd.read_csv("../FINAL/all_" + name + ".csv")
    print(data_final.shape)
    os.makedirs("../FINAL/" + name + "/", exist_ok=True)
    if "5" in name:
        for k, v in dizionario_report_linechart.items():
            print(k, "\t\t", v)
            os.makedirs("../FINAL/" + name + "/" + k + "/", exist_ok=False)
            plot_graphs("../FINAL/all_" + name + ".csv", top5, v, l_nn, l_dd,
                        "../FINAL/" + name + "/" + k + "/")
    elif "8" in name:
        for k, v in dizionario_report_linechart.items():
            print(k, "\t\t", v)
            os.makedirs("../FINAL/" + name + "/" + k + "/", exist_ok=False)
            plot_graphs("../FINAL/all_" + name + ".csv", top8, v, l_nn, l_dd,
                        "../FINAL/" + name + "/" + k + "/")
