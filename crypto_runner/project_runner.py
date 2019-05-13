# Single target + basic data
# Single target + indicators
# Multi target + basic data
# Multi target + indicators

# invocare esperimento 1, alias SINGLE TARGET
#   string - path dei dati di input
#       1. "../crypto_preprocessing/step0_data/"
#       2. "../crypto_preprocessing/step1_indicators/"
#   string - path test set
#   list - configurazione sequenza temporale
#       1. 30
#       2. 60
#       3. 100
#       4. 200
#   list - numero neuroni
#       1. 128
#       2. 256
#       3. 512
#       4. 1024
#   string - nome esperimento

# invocare esperimento 3, alias MULTI TARGET
#   string - path dei dati di input
#       1. "../crypto_preprocessing/step5_horizontal/"
#       2. "../crypto_preprocessing/step6_horizontal/" [MANCA QUELLO CON GLI INDICATORI]
#   string - path test set
#   list - configurazione sequenza temporale
#       1. 30
#       2. 60
#       3. 100
#       4. 200
#   list - numero neuroni
#       1. 128
#       2. 256
#       3. 512
#       4. 1024
#   string - nome esperimento
