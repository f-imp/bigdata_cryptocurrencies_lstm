import os
import pandas as pd
import numpy as np
from math import sqrt


dates_to_use = '../../crypto_testset/from_2016_07_01_until_2017_06_26/test_set.txt'


#PATH="../../crypto_preprocessing/step4_cutdata"
PATH="../../crypto_preprocessing/step2_normalized" #normalized

result_folder="results"
partial_folder="stocks"
final_folder="RMSE"

date=[]

with open(dates_to_use, "r") as f:
    asd=f.read()
    asd=asd.split("'")
    for i in range (1,len(asd)-1,2):
       date.append(asd[i])


try:
    os.mkdir(result_folder)
except OSError:
    print("Creation of the directory %s failed" %  result_folder)
else:
    print("Successfully created the directory %s " % result_folder)

try:
    os.mkdir(os.path.join(result_folder,partial_folder))
except OSError:
    print("Creation of the directory %s failed" %  partial_folder)
else:
    print("Successfully created the directory %s " % partial_folder)

try:
    os.mkdir(os.path.join(result_folder,final_folder))
except OSError:
    print("Creation of the directory %s failed" %  final_folder)
else:
    print("Successfully created the directory %s " % final_folder)



for csv in os.listdir(PATH):
    toWrite = []
    toWrite.append("symbol,date,observed,predicted")
    with open(PATH+"/"+csv , "r") as f:
        for data in date:
            for line in f:
                if line.count(data):
                    line=line.split(",")
                    #toWrite.append(csv.replace(".csv","") + "," + data + "," + line[1] + "," + line[4])
                    toWrite.append(csv.replace(".csv","") + "," + data + "," + line[17] + "," + line[20]) #normalized
                    break
            f.seek(0)

    with open(result_folder+ "/" + partial_folder + "/" + csv, "+w") as d:
        for line in toWrite:
            d.write(line+"\n")

errors=[]


for csv in os.listdir(os.path.join(result_folder,partial_folder)):
    res = pd.read_csv(os.path.join(result_folder,partial_folder,csv))
    error = res['observed'] - res['predicted']
    sq_error = error ** 2
    errors.append(np.mean(sq_error))

with open(os.path.join(result_folder,final_folder,"RMSE.txt"), 'w+') as out:
    final = sqrt(np.mean(errors))
    out.write(str(final))