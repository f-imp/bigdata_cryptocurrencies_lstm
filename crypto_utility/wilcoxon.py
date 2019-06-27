import scipy.stats as ss

PATHS=["SingleTarget_Data","SingleTarget_Data_with_Indicators","MultiTarget_Data","MultiTarget_Data_with_Indicators"]

from pathlib import Path

target="RMSE_normalized"
target_index=-1
config="configuration"
config_index=-1

neuroni=[128,256]
days=[30,100,200]

COINS=["BTC","DASH","DOGE","LTC","XEM","XLM","XMR","XRP"]

#COINS=["BTC","DASH","DOGE","LTC","XLM"]

data=[]

from itertools import product

debug=False

data=[]


for path in PATHS:
    csv = "../" + path + "/Report/stockseries_oriented/"
    data1=[]
    for coin in COINS:
        for neur,dayz in product(neuroni,days):
            for filename in Path('').glob(csv+coin+'*/**/*.csv'):
                if (debug) : print(filename)
                i=0
                for line in open(filename, "r").readlines():
                    pezzi=line.split(',')
                    if i==0:
                        target_index=pezzi.index(target)
                        i+=1
                        config_index=pezzi.index(config)
                    if "LSTM_"+str(neur)+"_neurons_"+ str(dayz)+"_days" in line:
                        if (debug) : print(pezzi[config_index])
                        cfg=pezzi[config_index].split("_")
                        if (debug) : print(pezzi[target_index])
                        data1.append(float(pezzi[target_index]))

    data.append(data1)

dat=[]


for i in range(0,len(data)):
    for y in range(i+1,len(data)):
        print(PATHS[i] + " - " + PATHS[y])
        if debug: print(data[i])
        if debug: print(data[y])
        w,p = ss.wilcoxon(data[i],data[y])
        print(w, p)
        dat.append(p)

        '''
        w,p = ss.wilcoxon(data[i],data[y],correction=True)
        print(w, p)
        w,p = ss.mannwhitneyu(data[i],data[y])
        print(w, p)
        w,p = ss.ranksums(data[i],data[y])
        print(w, p)
        '''


if debug: print(len(dat))
if debug: print(dat)



#FDR CORRECTION
from mne.stats import fdr_correction

w,p = fdr_correction(dat)
print(w, p)