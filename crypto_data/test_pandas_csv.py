#test ignore

import pandas
df = pandas.read_csv('dataset/1/cyrpto_prices_v2.csv', index_col='DateTime')
print(df)