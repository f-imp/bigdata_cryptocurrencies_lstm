table1_inizio="""\\begin{{frame}}{{Results - Stock Oriented}}
\\begin{{block}}{{RMSE - PH_TITLE}}
\\begin{{table}}[] 
  \\begin{{tabular}}{{c?c|c|c?c|c|c}}
     Neurons & \multicolumn{{3}}{{c?}}{{128}}
        & \multicolumn{{3}}{{c}}{{256}}\\\\
        \hline
        Days & 30 & 100 & 200 & 30 & 100 & 200\\\\
        \specialrule{{.1em}}{{.05em}}{{.05em}}"""

table1_fine="""    \end{{tabular}}
\end{{table}}
\end{{block}}
\end{{frame}}"""

table2_inizio="""\\begin{{frame}}{{Results - Configuration Oriented}}
\\begin{{block}}{{RMSE - PH_TITLE}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c|c}}
         Coin & ST & ST-i & MT & MT-i \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}"""

table2_fine="""    \end{{tabular}}
\end{{table}}
\end{{block}}
\end{{frame}}"""

pretable3="""\subsection{Results Average}\n"""

table3="""\\begin{{frame}}{{Results - Neurons Average}}
\\begin{{block}}{{Average RMSE}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c}}
         \multirow{{2}}{{*}}{{Type}} & \multicolumn{{2}}{{c|}}{{Neurons}} & \multirow{{2}}{{*}}{{Average}}\\\\\cline{{2-3}}
          & 128 & 256 & \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}
         Single-target & {} & {} & {}\\\\
         Single-target indicators & {} & {} & {}\\\\
         Multi-target & {} & {} & {}\\\\
         Multi-target indicators & {} & {} & {}
    \end{{tabular}}
\end{{table}}
\end{{block}}
\\begin{{block}}{{Baseline RMSE}}
\\begin{{itemize}}
    \item \\textbf{{Simple:}} 0.0378
    \item \\textbf{{VAR Model:}} 0.0378
\end{{itemize}}
\end{{block}}
\end{{frame}}"""

table4="""\\begin{{frame}}{{Results - Days Average}}
\\begin{{block}}{{Average RMSE}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c|c}}
         \multirow{{2}}{{*}}{{Type}} & \multicolumn{{3}}{{c|}}{{Days}} & \multirow{{2}}{{*}}{{Average}}\\\\\cline{{2-4}}
          & 30 & 100 & 200 & \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}
         Single-target & {} & {} & {} & {}\\\\
         Single-target indicators & {} & {} & {} & {}\\\\
         Multi-target & {} & {} & {} & {}\\\\
         Multi-target indicators & {} & {} & {} & {}
    \end{{tabular}}
\end{{table}}
\end{{block}}
\\begin{{block}}{{Baseline RMSE}}
\\begin{{itemize}}
    \item \\textbf{{Simple:}} 0.0378
    \item \\textbf{{VAR Model:}} 0.0378
\end{{itemize}}
\end{{block}}
\end{{frame}}"""


def create_latex_table_red(tabella):
    righe = tabella.split("\n")
    for rigo in righe:
        vals = []
        dentro = False
        rig = []
        for coin in COINS:
            if coin in rigo:
                dentro = True
                rig = rigo.replace("\\\\", "").split("&")
                if len(COINS) != COINS.index(coin) + 1:
                    rig.append("\\\\")
                else:
                    rig.append("")
                for ri in rig:
                    try:
                        val = float(ri)
                        vals.append(val)
                    except ValueError:
                        None
                break
        if (dentro):
            rig[vals.index(min(vals)) + 1] = "\\textcolor{red}{" + str(min(vals)) + "}"
            print("&".join(rig[:-1]) + rig[len(rig) - 1])
        else:
            print(rigo)
    print('\n')

def create_latex_table3_red(tabella):
    righe = tabella.split("\n")
    i=1
    for rigo in righe:
        vals = []
        dentro = False
        rig = []
        if "target" in rigo:
            dentro = True
            rig = rigo.replace("\\\\", "").split("&")
            if i!= len(PATHS):
                rig.append("\\\\")
                i+=1
            else:
                rig.append("")
            for ri in rig:
                try:
                    val = float(ri)
                    vals.append(val)
                except ValueError:
                    None
        if (dentro):
            rig[vals.index(min(vals)) + 1] = "\\textcolor{red}{" + str(min(vals)) + "}"
            print("&".join(rig[:-1]) + rig[len(rig) - 1])
        else:
            print(rigo)
    print('\n')

PATHS=["SingleTarget_Data","SingleTarget_Data_with_Indicators","MultiTarget_Data","MultiTarget_Data_with_Indicators"]

from pathlib import Path

target="RMSE_normalized"
target_index=-1
config="configuration"
config_index=-1

neuroni=[128,256]
days=[30,100,200]

#TOP10
#COINS=['BTC', 'DASH', 'DOGE', 'ETC', 'ETH', 'LTC', 'XEM', 'XLM', 'XMR', 'XRP']

#TOP8
#COINS=['BTC', 'DASH', 'DOGE', 'LTC', 'XEM', 'XLM', 'XMR', 'XRP']

#TOP5
COINS=['BTC', 'DASH', 'DOGE', 'LTC', 'XLM']

table1_mezzo=""

for i in range(0,len(COINS)):
    if i==len(COINS): table1_mezzo=table1_mezzo+"\n         "+COINS[i]+" & {} & {} & {} & {} & {} & {}"
    else: table1_mezzo=table1_mezzo+"\n         "+COINS[i]+" & {} & {} & {} & {} & {} & {}\\\\"

table2_mezzo=""

for i in range(0,len(COINS)):
    if i==len(COINS): table2_mezzo=table2_mezzo+"\n         "+COINS[i]+" & {} & {} & {} & {}\\\\"
    else: table2_mezzo=table2_mezzo+"\n         "+COINS[i]+" & {} & {} & {} & {}\\\\"

table1=table1_inizio+table1_mezzo+"\n"+table1_fine
table2=table2_inizio+table2_mezzo+"\n"+table2_fine




data=[]

from itertools import product

debug=False

for path in PATHS:
    csv = "../" + path + "/Report/stockseries_oriented/"
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
                        data.append(pezzi[target_index])



table1=table1.replace("{}","{:.6}")
for i in range (0,len(PATHS)):
    data_cut=data[(len(data)//len(PATHS))*(i):(len(data)//len(PATHS))*(i+1)]
    title=PATHS[i].replace("T","-t").replace("_Data","").replace("_with_I", " with i")
    tabella=table1.replace("PH_TITLE",title)
    tabella= tabella.format(*data_cut)
    create_latex_table_red(tabella)



#---TABLE2


data2=[]

title=[]

for neur,dayz in product(neuroni,days):
    title.append("LSTM "+str(neur)+" neurons "+str(dayz)+" days")
    for coin in COINS:
        for path in PATHS:
            csv = "../" + path + "/Report/stockseries_oriented/" + coin
            for filename in Path('').glob(csv +'*/**/*.csv'):
                if debug: print(filename)
                i = 0
                for line in open(filename, "r").readlines():
                    pezzi = line.split(',')
                    if i == 0:
                        target_index = pezzi.index(target)
                        i += 1
                        config_index = pezzi.index(config)
                    if "LSTM_" + str(neur) + "_neurons_" + str(dayz) + "_days" in line:
                        if (debug): print(pezzi[config_index])
                        cfg = pezzi[config_index].split("_")
                        if (debug): print(pezzi[target_index])
                        data2.append(pezzi[target_index])

table2=table2.replace("{}","{:.6}")

for i in range (0,len(title)):
    data_cut=data2[(len(data2)//len(title))*(i):(len(data2)//len(title))*(i+1)]
    tabella=table2.replace("PH_TITLE",title[i])
    tabella=tabella.format(*data_cut)
    create_latex_table_red(tabella)


print(pretable3)
#---- table 3

data3=[]

for i in range(0, len(PATHS)):
    for y in range(i,len(data2), len(PATHS)):
        data3.append(data2[y])

data_avg=[]

for i in range(0,len(PATHS)):
    data_cut=data3[(len(data2)//len(PATHS))*(i):(len(data2)//len(PATHS))*(i+1)]
    data_cut=[float(i) for i in data_cut]
    datz=[]
    for i in range (0, len(neuroni)):
        data_neu_cut=data_cut[i*len(days)*len(COINS):(i+1)*len(days)*len(COINS)]
        if (debug) : print(str(i*len(days)*len(COINS)) + " - " + str((i+1)*len(days)*len(COINS)))
        datz.append(sum(data_neu_cut)/len(data_neu_cut))

    [data_avg.append(i) for i in datz]
    data_avg.append((sum(datz)/len(datz)))

table3=table3.replace("{}","{:.4f}")
table3=table3.format(*data_avg)
create_latex_table3_red(table3)


#---- table 4

data4=[]

for i in range(0, len(days)):
    for y in range(i,len(data), len(days)):
        data4.append(data[y])
        
data_to_avg=[]


for i in range(0,len(days)):
    data_cut=data4[(len(data)//len(days))*(i):(len(data)//len(days))*(i+1)]
    if (debug): print(str((len(data)//len(days))*(i)) + " - " + str((len(data)//len(days))*(i+1)))
    data_cut=[float(i) for i in data_cut]
    for i in range (0, len(PATHS)):
        data_path_cut=data_cut[i*len(neuroni)*len(COINS):(i+1)*len(neuroni)*len(COINS)]
        if (debug) : print(str(i*len(neuroni)*len(COINS)) + " - " + str((i+1)*len(neuroni)*len(COINS)))
        data_to_avg.append(sum(data_path_cut)/len(data_path_cut))

data_avg=[]

for i in range(0, len(PATHS)):
    dataz=[]
    for y in range(i,len(data_to_avg), len(days)+1):
        dataz.append(data_to_avg[y])

    [data_avg.append(i) for i in dataz]
    data_avg.append((sum(dataz)/len(dataz)))

table4=table4.replace("{}","{:.4f}")
table4=table4.format(*data_avg)
create_latex_table3_red(table4)