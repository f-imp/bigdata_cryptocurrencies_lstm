import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas
from scipy import stats
from scipy.stats import pearsonr


def plot_bargraph(title, category, values, x_label, y_label):
    # this is for plotting purpose
    index = np.arange(len(category))
    plt.figure(1, figsize=[6, 3.5], dpi=120, facecolor='w', edgecolor='black')
    plt.bar(index, values)
    plt.xlabel(x_label, fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.xticks(index, category, fontsize=10, rotation=90)
    plt.title(title)
    plt.show();


def plot_functiongraph(title, x, y, label_x, label_y, label_legend):
    plt.plot(x, y, label=label_legend)
    # naming the x axis
    plt.xlabel(label_x)
    # naming the y axis
    plt.ylabel(label_y)
    # giving a title to my graph
    plt.title(title)

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()
    return


def plot_boxnotch_univariateanalysis(data, features_name):
    fig2 = plt.figure(2, figsize=[10, 4.5], dpi=95, facecolor='w', edgecolor='black')
    numero_features = len(data)
    d = []
    for f in range(0, numero_features, 1):
        d.append(list(data[f]))
    plt.boxplot(d, notch=True)
    plt.title(f)
    fig2.show()
    return


def plot_correlationbtw2V(title, data1, data2, righe, colonne, indice, cm):
    plt.subplot(righe, colonne, indice)
    plt.plot(data1, data2, cm)
    # plt.tight_layout()
    plt.subplots_adjust(left=-0.2, right=0.8, top=0.8, bottom=-0.5)
    plt.title(title)
    return


def distinct(lista):
    distinct_lista = []
    map(lambda x: not x in distinct_lista and distinct_lista.append(x), lista)
    return distinct_lista


def get_dict_fromOutcome(y):
    cls = distinct(y)
    cls.sort()
    d = {}
    for e in cls:
        d[e] = 0
    for e in y:
        d[e] = d[e] + 1
    return d


# Usually useful with CATEGORICAL FEATURES => Univariate Analysis
def categorical_plot(title, y, x_label, y_label):
    d = get_dict_fromOutcome(y)
    axisx = []
    axisy = []
    for elm in d.keys():
        axisx.append(elm)
    for elm in d.values():
        axisy.append(elm)
    plot_bargraph(title, axisx, axisy, x_label, y_label)
    return


def info_univariate(data, features_name):
    d = np.array(data)
    data_t = np.transpose(d)
    for f in range(0, len(data_t), 1):
        ds = sorted(data_t[f])
        moda = stats.mode(ds)
        # print('Feature: {}:\nMAX: --> {}\nMIN:  --> {}\nAVG:  --> {}\nMODE:  --> V:{} --> {}\nMed  --> {}\n'.format(
        #     features_name[f], np.max(data_t[f]),
        #     np.min(data_t[f]),
        #     round(np.mean(data_t[f]), 1),
        #     moda[0], moda[1],
        #     np.median(ds)))
    plot_boxnotch_univariateanalysis(data_t, features_name)
    return


def info_bivariate(data, features_name):
    thre = 0.4
    d = np.array(data)
    data_t = np.transpose(d)
    el = np.arange(0, len(data_t))
    combo_index = list(itertools.product(el, repeat=2))
    fig3 = plt.figure(1, figsize=[100, 70], dpi=30, facecolor='w', edgecolor='black')
    i = 1
    for e in combo_index:
        ind1 = e.__getitem__(0)
        ind2 = e.__getitem__(1)
        c, t = pearsonr(data_t[ind1], data_t[ind2])

        titolo = '\n{} - {}\nP: --> {}'.format(features_name[ind1], features_name[ind2], round(c, 2))
        print(titolo)
    #     if c < thre and c > -thre:
    #         plot_correlationbtw2V(titolo, data_t[ind1], data_t[ind2], len(data_t), len(data_t), i, 'r*')
    #     else:
    #         plot_correlationbtw2V(titolo, data_t[ind1], data_t[ind2], len(data_t), len(data_t), i, 'g.')
    #     i = i + 1
    # # fig3.show()
    # plt.show()
    return


dataframe = pandas.read_csv("../crypto_preprocessing/step5_horizontal/horizontal.csv", delimiter=',',
                            header=0)
# data := lista di dati (ciascuna entry è a sua volta una lista)
data = dataframe.values

# X := lista di dati (ciascuna entry è l'insieme delle sole features di ciascuna entry)
a = dataframe.drop(
    columns=["DateTime", 'Symbol_1', 'Symbol_2', 'Symbol_3', 'Symbol_4', 'Symbol_5', 'Symbol_6', 'Symbol_7',
             'Symbol_8'])
print(a)
dd = a.values
col_name = a.columns.values
print(np.shape(data), "\n", col_name)
info_bivariate(dd, col_name)
