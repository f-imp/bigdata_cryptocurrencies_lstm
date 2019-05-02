import os
from crypto_utility import test_set

name_folder = "crypto_testset"
try:
    os.mkdir("../" + name_folder)
except OSError:
    print("Creation of the directory %s failed" % name_folder)
else:
    print("Successfully created the directory %s " % name_folder)
#start_date = '2016-06-26'
start_date = '2017-06-26'
end_date = '2017-06-26'
start_date_format_folder = start_date.replace("-", "_")
end_date_format_folder = end_date.replace("-", "_")
name_folder_test = "from_" + start_date_format_folder + "_until_" + end_date_format_folder
try:
    os.mkdir("../" + name_folder + "/" + name_folder_test)
except OSError:
    print("Creation of the directory %s failed" % name_folder_test)
else:
    print("Successfully created the directory %s " % name_folder_test)
path_original_data = "../crypto_data/data/"
original_files = os.listdir(path_original_data)
output_path = "../" + name_folder + "/" + name_folder_test + "/"
#how_much_entries = 30
how_much_entries = 1
filename = "test_set"
print(path_original_data)
print(original_files[0])
test_set.generate_testset(path_original_data, original_files[0], start_date, end_date, how_much_entries, output_path,
                          filename)
