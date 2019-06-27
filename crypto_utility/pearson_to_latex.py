import itertools
import os

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def pearson_correlation(data, features_name, threshold):
    table = "\\begin{center} \n \\begin{tabular}{|c|"
    for i in enumerate(features_name):
        table += "c|"
    table += "}\n\hline\n - & "
    for i, f in enumerate(features_name):
        table += str(f).replace("_", "")
        if (i == len(features_name) - 1):
            table += " \\\\"
        else:
            table += " & "
    d = np.array(data)
    data_t = np.transpose(d)
    table += "\n\hline\hline\n"
    for i, feat1 in enumerate(features_name):
        table += str(feat1).replace("_", "") + " & "
        for j, feat2 in enumerate(features_name):
            c, t = pearsonr(data_t[i], data_t[j])
            if (c < threshold and c > -threshold):
                table += "\\textcolor{red}{\\textbf{" + str(round(c, 2)) + "}}"
            else:
                table += str(round(c, 2))
            if (j == len(features_name) - 1):
                table += " \\\\\n \hline \n"
            else:
                table += " & "
    table += "\end{tabular}\n \end{center}"
    # print(table)
    # thre = 0.4
    # d = np.array(data)
    # data_t = np.transpose(d)
    # el = np.arange(0, len(data_t))
    # combo_index = list(itertools.product(el, repeat=2))
    # # print(combo_index)
    # for e in combo_index:
    #     ind1 = e.__getitem__(0)
    #     ind2 = e.__getitem__(1)
    #     c, t = pearsonr(data_t[ind1], data_t[ind2])
    #
    #     titolo = '\n{} - {}\nP: --> {}'.format(features_name[ind1], features_name[ind2], round(c, 2))
    #     # print(titolo)
    return table


features_to_remove_single = ["DateTime", "Symbol"]
features_to_remove_multi = ["DateTime", 'Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6',
                            'Symbol_7',
                            'Symbol_8']

folder_refers = {"single": ["../crypto_preprocessing/step0_data/", features_to_remove_single],
                 "single_indicators": ["../crypto_preprocessing/step1_indicators/", features_to_remove_single],
                 "multi": ["../crypto_preprocessing/step5_horizontal/", features_to_remove_multi]}

pathfolder = "../Pearson_table_latex/"
os.makedirs(pathfolder, exist_ok=False)
for k, v in folder_refers.items():
    files = os.listdir(v[0])
    for each_csv in files:
        dataframe_all = pd.read_csv(v[0] + each_csv, delimiter=',', header=0)
        data_all = dataframe_all.values  # per controllare la dimensione - se non dovessi trovarmi
        print("All data -> ", np.shape(data_all))
        dataframe = dataframe_all.drop(columns=v[1])
        data = dataframe.values
        columns_name = dataframe.columns.values
        print("After reduction -> ", np.shape(data))
        pearson_correlation_table_latex = pearson_correlation(data=data, features_name=columns_name, threshold=0.4)
        with open(pathfolder + each_csv.replace(".csv", ""), "w") as fs:
            fs.write(pearson_correlation_table_latex)

#
# dataframe = pd.read_csv("../crypto_preprocessing/step5_horizontal/horizontal.csv", delimiter=',', header=0)
# data = dataframe.values
#
# a = dataframe.drop(
#     columns=["DateTime", 'Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6', 'Symbol_7',
#              'Symbol_8'])
# d = a.values
# col_name = a.columns.values
# print(np.shape(data), "\n", col_name)
# t = pearson_correlation(data=d, features_name=col_name)
# with open("../multi.txt", "w") as fs:
#     fs.write(t)
