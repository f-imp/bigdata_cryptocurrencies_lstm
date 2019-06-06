import os
from dateutil.parser import parse
from crypto_utility import test_set

def run():
    start_date = parse('2016-07-01')
    end_date = parse('2017-06-26')


    name_folder = "crypto_testset"
    name_folder_test = "from_" + str(start_date.date()).replace("-", "_") + "_until_" + str(end_date.date()).replace("-", "_")

    try:
        os.mkdir("../" + name_folder)
    except OSError:
        print("Creation of the directory %s failed" % name_folder)
    else:
        print("Successfully created the directory %s " % name_folder)

    try:
        os.mkdir("../" + name_folder + "/" + name_folder_test)
    except OSError:
        print("Creation of the directory %s failed" % name_folder_test)
    else:
        print("Successfully created the directory %s " % name_folder_test)


    output_path = "../" + name_folder + "/" + name_folder_test + "/"
    filename = "test_set"

    test_set.generate_testset(start_date,end_date,output_path,filename)