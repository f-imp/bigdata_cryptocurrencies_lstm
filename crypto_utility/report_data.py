import itertools
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from crypto_utility.experiments import get_RMSE


def report_configurations_exp1(temporal_sequence_used, neurons_used, name_folder_experiment,
                               name_folder_result_experiment, name_folder_report, name_output_files):
    kind_of_report = "configurations_oriented"
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/", exist_ok=True)
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/", exist_ok=True)

    stock_series = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/")

    overall_report = {'model': [], 'mean_rmse_norm': [], 'mean_rmse_denorm': []}
    for ts, n in itertools.product(temporal_sequence_used, neurons_used):
        configuration = "LSTM_{}_neurons_{}_days".format(n, ts)
        model_report = {'stock_names': [], 'rmse_list_norm': [], 'rmse_list_denorm': []}
        for s in stock_series:
            errors_file = pd.read_csv(
                name_folder_experiment + "/" + name_folder_result_experiment + "/" + s + "/" + configuration + "/stats/errors.csv",
                index_col=0, sep=',')
            model_report['stock_names'].append(s)
            model_report['rmse_list_norm'].append(errors_file["rmse_norm"])
            model_report['rmse_list_denorm'].append(errors_file["rmse_denorm"])
        os.makedirs(
            name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + configuration + "/",
            exist_ok=True)
        average_rmse_normalized = np.mean(model_report['rmse_list_norm'])
        average_rmse_denormalized = np.mean(model_report['rmse_list_denorm'])
        configuration_report = {"Average_RMSE_norm": [], "Average_RMSE_denorm": []}
        configuration_report["Average_RMSE_norm"].append(average_rmse_normalized)
        configuration_report["Average_RMSE_denorm"].append(average_rmse_denormalized)
        pd.DataFrame(configuration_report).to_csv(
            name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + configuration + "/report.csv")
        overall_report['model'].append(configuration)
        overall_report['mean_rmse_norm'].append(average_rmse_normalized)
        overall_report['mean_rmse_denorm'].append(average_rmse_denormalized)
    pd.DataFrame(overall_report).to_csv(
        name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + name_output_files + ".csv")
    plot_report(
        path_file=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + name_output_files + ".csv",
        x_data="model", column_of_data="mean_rmse_norm", label_for_values_column="RMSE (Average)",
        label_x="Configurations", title_img="Average RMSE - Configurations Oriented",
        destination=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/",
        name_file_output="singletarget_bargraph_RMSE_configurations_oriented")
    return


def report_stockseries_exp1(name_folder_experiment, name_folder_result_experiment, name_folder_report,
                            name_files_output):
    kind_of_report = "stockseries_oriented"
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/", exist_ok=True)
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/", exist_ok=True)

    stock_series = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/")
    # for each stock series:
    for s in stock_series:
        STOCK_FOLDER_PATH = name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + s + "/"
        os.makedirs(STOCK_FOLDER_PATH, exist_ok=True)
        single_series_report_dict = {'configuration': [], 'RMSE_normalized': [], 'RMSE_denormalized': []}
        configuration_used = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/" + s + "/")
        configuration_used.sort(reverse=True)
        # for each configuration:
        for c in configuration_used:
            # save name of configuration in dictionary
            single_series_report_dict['configuration'].append(c)
            # read 'predictions.csv' file
            errors_file = pd.read_csv(
                name_folder_experiment + "/" + name_folder_result_experiment + "/" + s + "/" + c + "/stats/errors.csv")
            # perform RMSE_norm and save in dictionary
            #TODO: ERRORE CANNOT CONVERT CLASS TO FLOAT perchè è un array non un singolo valore, manca la media di regola
            single_series_report_dict['RMSE_normalized'].append(float(errors_file["rmse_norm"]))
            # print(float(errors_file['rmse_norm']))
            # perform RMSE_denorm and save in dictionary
            single_series_report_dict['RMSE_denormalized'].append(float(errors_file["rmse_denorm"]))
        # save as '.csv' the dictionary in STOCK_FOLDER_PATH
        pd.DataFrame(single_series_report_dict).to_csv(
            name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + s + "/" + name_files_output + ".csv")
        plot_report(
            path_file=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + s + "/" + name_files_output + ".csv",
            x_data="configuration", column_of_data="RMSE_normalized", label_for_values_column="RMSE (Average)",
            label_x="Configurations", title_img="Average RMSE - " + str(s),
            destination=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + s + "/",
            name_file_output="singletarget_bargraph_RMSE_" + str(s))
    return


# Da sistemare ----- WORK IN PROGRESS -------
def plot_report(path_file, x_data, column_of_data, label_for_values_column, label_x, title_img, destination,
                name_file_output):
    report_csv = pd.read_csv(path_file, header=0)
    configurations = report_csv[x_data]
    mean_rmse_normalized = report_csv[column_of_data]
    index = np.arange(len(configurations))
    f = plt.figure()
    plt.bar(index, mean_rmse_normalized)
    plt.ylabel(label_for_values_column, fontsize=10)
    plt.xlabel(label_x, fontsize=10)
    # plt.hlines(np.min(mean_rmse_normalized), 0, len(configurations), linestyles='-', colors='red', linewidth=2, label="Min value")
    # plt.hlines(np.max(mean_rmse_normalized), 0, len(configurations), linestyles='-', colors='red', linewidth=2, label=str(round(np.max(mean_rmse_normalized),4)))
    plt.xticks(index, configurations, fontsize=7, rotation=90)
    plt.title(title_img)
    f.savefig(destination + name_file_output, bbox_inches='tight', pad_inches=0)
    # plt.show()
    return


def report_configurations_exp2(name_folder_experiment, name_folder_result_experiment, name_folder_report,
                               name_files_output):
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/", exist_ok=True)

    versions_dataset = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/")

    for v in versions_dataset:
        print(v)
        os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + v + "/", exist_ok=True)
        dizionario_report_totale = {"configuration": [], "Average_RMSE_norm": [], "Average_RMSE_denorm": []}
        confs = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/" + v)
        confs.sort(reverse=True)
        for c in confs:
            print(c)
            errors_data = pd.read_csv(
                name_folder_experiment + "/" + name_folder_result_experiment + "/" + v + "/" + c + "/stats/errors.csv")
            dizionario_report_totale["configuration"].append(c)
            dizionario_report_totale["Average_RMSE_norm"].append(float(errors_data["rmse_norm"]))
            dizionario_report_totale["Average_RMSE_denorm"].append(float(errors_data["rmse_denorm"]))
        pd.DataFrame(dizionario_report_totale).to_csv(
            name_folder_experiment + "/" + name_folder_report + "/" + v + "/" + name_files_output + ".csv")
        plot_report(
            path_file=name_folder_experiment + "/" + name_folder_report + "/" + v + "/" + name_files_output + ".csv",
            x_data="configuration", column_of_data="Average_RMSE_norm", label_for_values_column="RMSE (Average)",
            label_x="Configurations", title_img="Average RMSE - Configurations Oriented",
            destination=name_folder_experiment + "/" + name_folder_report + "/" + v + "/",
            name_file_output="bargraph_RMSE_configurations_oriented")
    return


def report_configurations_exp3(name_folder_experiment, name_folder_result_experiment, name_folder_report,
                               name_files_output):
    kind_of_report = "configurations_oriented"
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/", exist_ok=True)
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/", exist_ok=True)

    # if "Indicators" in name_folder_experiment:
    #     name_folder_result_experiment += "/horizontal_indicators"
    # else:
    #     name_folder_result_experiment += "/horizontal"

    confs = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/")
    confs.sort(reverse=True)
    dizionario_report_totale = {"configuration": [], "Average_RMSE_norm": [], "Average_RMSE_denorm": []}
    for c in confs:
        errors_data = pd.read_csv(
            name_folder_experiment + "/" + name_folder_result_experiment + "/" + c + "/stats/errors.csv")
        dizionario_report_totale["configuration"].append(c)
        dizionario_report_totale["Average_RMSE_norm"].append(float(errors_data["rmse_norm"]))
        dizionario_report_totale["Average_RMSE_denorm"].append(float(errors_data["rmse_denorm"]))

    pd.DataFrame(dizionario_report_totale).to_csv(
        name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + name_files_output + ".csv")
    plot_report(
        path_file=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + name_files_output + ".csv",
        x_data="configuration", column_of_data="Average_RMSE_norm", label_for_values_column="RMSE (Average)",
        label_x="Configurations", title_img="Average RMSE - Configurations Oriented",
        destination=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/",
        name_file_output="multitarget_bargraph_RMSE_configurations_oriented")
    return


def report_stockseries_exp3(names_series, name_folder_experiment, name_folder_result_experiment,
                            name_folder_report, name_files_output):
    kind_of_report = "stockseries_oriented"
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/", exist_ok=True)
    os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/", exist_ok=True)

    for n in names_series:
        os.makedirs(name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + n, exist_ok=True)
        dizionario_report_totale = {"configuration": [], "RMSE_normalized": [], "RMSE_denormalized": []}
        confs = os.listdir(name_folder_experiment + "/" + name_folder_result_experiment + "/")
        print(name_folder_experiment + "/" + name_folder_result_experiment + "/")
        confs.sort(reverse=True)
        for c in confs:
            dizionario_report_totale["configuration"].append(c)
            predictions_file = pd.read_csv(
                name_folder_experiment + "/" + name_folder_result_experiment + "/" + c + "/stats/predictions.csv",
                sep=',')
            # calcolare Average_RMSE_norm per la criptovaluta di nome n
            # print(float(predictions_file[n + "_observed_norm"]), "\t", type(predictions_file[n + "_observed_norm"]))
            RMSE_norm = get_RMSE(np.array(predictions_file[n + "_observed_norm"]),
                                 np.array(predictions_file[n + "_predicted_norm"]))
            # calcolare Average_RMSE_denorm per la criptovaluta di nome n
            RMSE_denorm = get_RMSE(np.array(predictions_file[n + "_observed_denorm"]),
                                   np.array(predictions_file[n + "_predicted_denorm"]))
            dizionario_report_totale["RMSE_normalized"].append(float(RMSE_norm))
            dizionario_report_totale["RMSE_denormalized"].append(float(RMSE_denorm))
        pd.DataFrame(dizionario_report_totale).to_csv(
            name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + n + "/" + name_files_output + ".csv")
        plot_report(
            path_file=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + n + "/" + name_files_output + ".csv",
            x_data="configuration", column_of_data="RMSE_normalized", label_for_values_column="RMSE",
            label_x="Configurations", title_img="MultiTarget: RMSE - " + str(n),
            destination=name_folder_experiment + "/" + name_folder_report + "/" + kind_of_report + "/" + n + "/",
            name_file_output="multitarget_bargraph_RMSE_" + str(n))
    return
