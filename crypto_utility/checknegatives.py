import os
import pandas as pd

PATHS=["SingleTarget_Data","SingleTarget_Data_with_Indicators","MultiTarget_Data","MultiTarget_Data_with_Indicators"]

PATH="Result"

top5="top5Result"
top8="top8Result"

COIN8=["BTC","XRP","LTC","XLM","XMR","DASH","XEM","DOGE"] #Top8

COIN5=["BTC","LTC","XLM","DASH","DOGE"] #Top5

file="stats/predictions.csv"

c1=0

print("TOP8")
for path in PATHS:
    print(path)

    for coin in COIN8:
       # if "SingleTarget_Data_with_Indicators" in path: coin=coin+"_with_indicators"
        for conf in os.listdir("../"+ top8 + "/"+path+"/"+PATH+"/"+coin):
            csv=pd.read_csv("../"+ top8 + "/"+path+"/"+PATH+"/"+coin+"/"+conf+"/"+file)
            i=0
            for value in csv["predicted_norm"]:
                if value <0 :
                    print(csv["date"][i],csv["symbol"][i],csv["predicted_norm"][i],"(",csv["observed_norm"][i],")")
                    c1=c1+1
                i=i+1


print("TOP5")
for path in PATHS:
    print(path)

    for coin in COIN5:
        #if "SingleTarget_Data_with_Indicators" in path: coin=coin+"_with_indicators"
        for conf in os.listdir("../"+ top5 + "/"+path+"/"+PATH+"/"+coin):
            csv=pd.read_csv("../" + top5 + "/"+path+"/"+PATH+"/"+coin+"/"+conf+"/"+file)
            i=0
            for value in csv["predicted_norm"]:
                if value <0 :
                    print(csv["date"][i],csv["symbol"][i],csv["predicted_norm"][i],"(",csv["observed_norm"][i],")")
                    c1=c1+1
                i=i+1


print("Valori negativi trovati: ",c1)