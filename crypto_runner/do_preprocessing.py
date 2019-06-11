import os

from crypto_utility import preprocessing

def run(fd, COINS):

    # PRE PROCESSING
    # Set the name of folder in which save all intermediate results
    name_folder = "crypto_preprocessing"
    raw_data = "../crypto_data/data/"

    try:
        os.mkdir("../" + name_folder)
    except OSError:
        print("Creation of the directory %s failed" % name_folder)
    else:
        print("Successfully created the directory %s " % name_folder)


    # ------------------------------------------
    # STEP.0: PreProcessData
    # ------------------------------------------
    #Converts data into our format

    folder_step_zero = "step0_data"
    try:
        os.mkdir("../" + name_folder + "/" + folder_step_zero)
    except OSError:
        print("Creation of the directory %s failed" % folder_step_zero)
    else:
        print("Successfully created the directory %s " % folder_step_zero)
    output_indicators_path = "../" + name_folder + "/" + folder_step_zero + "/"

    for each_stock in os.listdir(raw_data):
        name = each_stock.replace(".csv", "")
        if name in COINS:
            file = raw_data + each_stock
            preprocessing.generate_normal(file, output_indicators_path, name)

    # ------------------------------------------
    # STEP.1: Add Additional Features
    # ------------------------------------------
    # Listing all available time series (original data)

    folder_step_one = "step1_indicators"
    try:
        os.mkdir("../" + name_folder + "/" + folder_step_one)
    except OSError:
        print("Creation of the directory %s failed" % folder_step_one)
    else:
        print("Successfully created the directory %s " % folder_step_one)
    output_indicators_path = "../" + name_folder + "/" + folder_step_one + "/"
    # Execute over all time series in the folder chosen
    # Performs indicators: RSI, SMA, EMA
    # Over 14, 30, 60 previous days
    lookback = [14, 30, 60]
    for each_stock in os.listdir(raw_data):
        name = each_stock.replace(".csv", "")
        if name in COINS:
            file = raw_data + each_stock
            preprocessing.generate_indicators(file, "Close", lookback, output_indicators_path, name)


    # ------------------------------------------
    # STEP.2: Normalize Data
    # ------------------------------------------
    # Not used, but we will leave this bit
    with_indicators_data = "../" + name_folder + "/" + folder_step_one + "/"
    with_indicators_stock_series = os.listdir(with_indicators_data)
    folder_step_two = "step2_normalized"
    try:
        os.mkdir("../" + name_folder + "/" + folder_step_two)
    except OSError:
        print("Creation of the directory %s failed" % folder_step_two)
    else:
        print("Successfully created the directory %s " % folder_step_two)
    output_normalized_path = "../" + name_folder + "/" + folder_step_two + "/"
    # Chosen features to exclude in normalizing process
    excluded_features = ['DateTime', 'Symbol']
    for each_stock_with_indicators in with_indicators_stock_series:
        name = each_stock_with_indicators.replace("_with_indicators.csv", "")
        file = with_indicators_data + "/" + each_stock_with_indicators
        preprocessing.normalized(file, excluded_features, output_normalized_path, name)


    # ------------------------------------------
    # STEP.3: Create All Data .csv for experiment 2
    # ------------------------------------------

    folder_step_three = "step3_alldata"
    try:
        os.mkdir("../" + name_folder + "/" + folder_step_three)
    except OSError:
        print("Creation of the directory %s failed" % folder_step_three)
    else:
        print("Successfully created the directory %s " % folder_step_three)

    fileToWrite = open("../" + name_folder + "/" + folder_step_three + "/all.csv", "w+")
    prima_volta=True
    for stock in os.listdir(raw_data):
        if stock in COINS:
            fileToRead=open(raw_data+stock, "r")
            if prima_volta:
                prima_volta=False
            else:
                fileToRead.readline()
            for line in fileToRead:
                fileToWrite.write(line)
            fileToRead.close()
        fileToWrite.close()

    data_path = "../" + name_folder + "/" + folder_step_one + "/"
    fileToWrite = open("../" + name_folder + "/" + folder_step_three + "/all_with_indicators.csv", "w+")
    prima_volta=True
    for stock in os.listdir(data_path):
        fileToRead=open(data_path+stock, "r")
        if prima_volta:
            prima_volta=False
        else:
            fileToRead.readline()
        for line in fileToRead:
            fileToWrite.write(line)
        fileToRead.close()
    fileToWrite.close()

    data_path = "../" + name_folder + "/" + folder_step_two + "/"
    fileToWrite = open("../" + name_folder + "/" + folder_step_three + "/all_normalized.csv", "w+")
    prima_volta=True
    for stock in os.listdir(data_path):
        fileToRead=open(data_path+stock, "r")
        if prima_volta:
            prima_volta=False
        else:
            fileToRead.readline()
        for line in fileToRead:
            fileToWrite.write(line)
        fileToRead.close()
    fileToWrite.close()


    # ------------------------------------------
    # STEP.4: Create cut files from specified day for horizontal dataset
    # ------------------------------------------

    folder_step_four = "step4_cutdata"

    first_day = fd


    steps=["","_indicators"]

    for step in steps:

        try:
            os.mkdir("../" + name_folder + "/" + folder_step_four + step)
        except OSError:
            print("Creation of the directory %s failed" % folder_step_four + step)
        else:
            print("Successfully created the directory %s " % folder_step_four + step)

        if step=="":
            folder_data = folder_step_zero
        else:
            folder_data = folder_step_one

        for stock in os.listdir("../" + name_folder + "/" + folder_data):
            after_data = False
            fileToRead=open("../"+name_folder+ "/" +folder_data + "/"+ stock, "r")
            fileToWrite = open("../" + name_folder + "/" + folder_step_four + step + "/" +stock, "w")
            for line in fileToRead:
                if (line.startswith(first_day)):
                    after_data=True
                if(after_data or line.startswith("Date")):
                    fileToWrite.write(line)
            fileToRead.close()
            fileToWrite.close()



        # ------------------------------------------
        # STEP.5: Create horizontal dataset from cut files
        # ------------------------------------------


        folder_step_five = "step5_horizontal"


        try:
            os.mkdir("../" + name_folder + "/" + folder_step_five)
        except OSError:
            print("Creation of the directory %s failed" % folder_step_five)
        else:
            print("Successfully created the directory %s " % folder_step_five)


        file=[]
        primo=True
        n=0
        colonne=0

        #concatenuta in orizzontale tutti i file in un array di stringhe

        for stock in os.listdir("../" + name_folder + "/" + folder_step_four + step):
            n+=1

            fileToRead = open("../" + name_folder + "/" + folder_step_four + step + "/" + stock, "r")
            i = 0
            if primo:
                primo = False
                for line in fileToRead:

                    if i==0:
                        colonne=len(line.split(","))

                    file.append(line)
                    i += 1

            else:
                for line in fileToRead:

                    file[i]=file[i][:-1]+","+line

                    split=file[i].split(",",1)

                    split[1]=split[1].replace(split[0]+",","")

                    file[i]=split[0]+","+split[1]

                    i+=1

            fileToRead.close()


        #aggiungi un numero per disambiguare le colonne
        for i in range (n,0, -1):
            if i==n:
                file[0]=file[0].replace(",", "_" + str(i) + ",")
            else:
                if i==1:
                    file[0]=file[0].replace("_"+str(i+1)+",", "_" + str(i) + ",", colonne)
                else:
                    file[0]=file[0].replace("_"+str(i+1)+",", "_" + str(i) + ",", colonne+((i-1)*(colonne-1)))

        #rimuovi il numero per la prima colonna e aggiungilo all'ultima
        file[0]=file[0].replace("_1,", ",", 1)[:-1]+ "_"+str(n)+"\n"


        #scrivi l'array nel file

        if step == "":
            filename = "/horizontal.csv"
        else:
            filename = "/horizontal_indicators.csv"

        fileToWrite = open("../" + name_folder + "/" + folder_step_five + filename, "w")
        for line in file:
            fileToWrite.write(line)
        fileToWrite.close()
