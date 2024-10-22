#only for dataset 1
#crea in automatico i file singoli per ogni crypto se non presenti e li sovrascrive se rieseguito
#NB la cartella "data" deve essere già esistente

#dubbi da risolvere 1) il prezzo delle crypto è in USD o in BTC?

#header da inserire come prima riga di ogni csv
header="DateTime,Open,High,Low,Close,Volume,VolumeBTC,Symbol"

#crypto da cercare
#TOP10
#cryptocurrenciesSymbols=["BTC","XRP","LTC","ETC","ETH","XLM","XMR","DASH","XEM","DOGE"]

#TOP8
cryptocurrenciesSymbols=["BTC","XRP","LTC","XLM","XMR","DASH","XEM","DOGE"]

#TOP5
#cryptocurrenciesSymbols=["BTC","LTC","XLM","DASH","DOGE"]

for crypto in cryptocurrenciesSymbols:
    fileToRead=""
    fileToWrite = open("data/"+crypto+".csv", "w+")
    fileToWrite.write(header+"\n")
    if crypto == "BTC":
        fileToRead = open("dataset/1/btc_prices.csv", "r")
        crypto = "USD"
    else:
        fileToRead = open("dataset/1/crypto_prices.csv", "r")
    for line in fileToRead:
        #per prendere quelli giusti controllo se sta la virgola a sinistra e "a capo" a destra del simbolo
        if line.count(","+crypto+"\n") >0:
            line = line[:line.find(" ")] + line[line.find(","):]
            if crypto=="USD": line=line.replace("USD","BTC")
            fileToWrite.write(line)
            #debug print
            #print(line[:-1])
    fileToWrite.close()
    fileToRead.close()

