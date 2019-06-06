# We are sure that all stocks series are observed until 15th of January 2019 (2019-01-15)
# Due to it's useful create a function that takes the starting and ending date
# and "number_samples" entries choosed randomly
import pandas as pd
import random
import ast
import numpy as np
import calendar, random
from datetime import datetime

np.random.seed(0)


def generate_testset(start, end, output_path, filename_output):

    start=datetime.date(start)
    end=datetime.date(end)
    #calcolo il numero di mesi tra le due date
    m=(end.year - start.year) * 12 + end.month - start.month
    m=m+1

    test_set=[]

    for i in range(0,m):
        random_day=randomdate(start.year, start.month)
        #se l'ultimo giorno che genero supera l'ultimo giorno disponibile lo setto di default a l'ultimo giorno disponibile
        #possibile cosa pure per il primo giorno ma al momento partiamo dal primo del mese
        if i+1==m and random_day.day>end.day:
            random_day=random_day.replace(day=end.day)

        test_set.append(str(random_day))
        new_year=start.year
        new_month=start.month+1
        if(new_month==13):
            new_month=1
            new_year=start.year+1

        start=start.replace(year=new_year,month=new_month)

    with open(output_path + filename_output + ".txt", 'w') as file:
        file.write(str(test_set))
    print("Test set generato : " , test_set)
    return

def randomdate(year, month):
    dates = calendar.Calendar().itermonthdates(year, month)
    return random.choice([date for date in dates if date.month == month])

def get_testset(path_file):
    with open(path_file) as td:
        file_test_set = td.read()
    test_set = ast.literal_eval(file_test_set)
    test_set = np.array(pd.to_datetime(test_set, yearfirst=True))
    return test_set
