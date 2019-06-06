import scipy.stats as ss

PATHS=["SingleTarget_Data","SingleTarget_Data_with_Indicators","MultiTarget_Data","MultiTarget_Data_with_Indicators"]

from pathlib import Path

target="RMSE_normalized"
target_index=-1
config="configuration"
config_index=-1

neuroni=[128,256]
days=[30,100,200]

COINS=["BTC","DASH","DOGE","ETC","ETH","LTC","XEM","XLM","XMR","XRP"]

data=[]

from itertools import product

debug=False

data=[]


for path in PATHS:
    csv = "../baseline/" + path + "/Report/stockseries_oriented/"
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

print(len(data))
print(data)

dat=[]

for i in range(0,len(data)):
    for y in range(i+1,len(data)):
        print(PATHS[i] + " - " + PATHS[y])
        w,p = ss.wilcoxon(data[i],data[y])
        print(w, p)
        dat.append(p)

        '''w,p = ss.wilcoxon(data[i],data[y],correction=True)
        print(w, p)
        w,p = ss.mannwhitneyu(data[i],data[y])
        print(w, p)
        w,p = ss.ranksums(data[i],data[y])
        print(w, p)
        '''



table='''\\begin{{frame}}{{Results - Wilcoxon}}
\\begin{{block}}{{Wilcoxon signed-rank test}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c|c}}
          & ST & ST-i & MT & MT-i \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}
         ST &  & {0:.4f} & {1:.4f} & {2:.4f}\\\\
         ST-i & {0:.4f} & & {3:.4f} & {4:.4f}\\\\
         MT & {1:.4f} & {3:.4f} & & {5:.4f}\\\\
         MT-i & {2:.4f} & {4:.4f} & {5:.4f} &
    \end{{tabular}}
\end{{table}}
\end{{block}}
\end{{frame}}'''

print(len(dat))
print(dat)

table=table.format(*dat)



print(table)


table='''\\begin{{frame}}{{Results - FDR}}
\\begin{{block}}{{FDR correction}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c|c}}
          & ST & ST-i & MT & MT-i \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}
         \multirow{{2}}{{*}}{{ST}} &  & {6} & {7} & {8}\\\\
          &  & {0} & {1} & {2}\\\\
         \hline
         \multirow{{2}}{{*}}{{ST-i}} & {6} &  & {9} & {10}\\\\
          & {0} &  & {3} & {4}\\\\
         \hline
         \multirow{{2}}{{*}}{{MT}} & {7} & {9} &  & {11}\\\\
          & {1} & {3} &  & {5}\\\\
         \hline
         \multirow{{2}}{{*}}{{MT-i}} & {8} & {10} & {11} &\\\\
          & {2} & {4} & {5} & 
    \end{{tabular}}
\end{{table}}
\end{{block}}
\end{{frame}}'''


#FDR CORRECTION
from mne.stats import fdr_correction

w,p = fdr_correction(dat)
print(w, p)

#non sono sicuro
table=table.format(*w,*p)

print(table)