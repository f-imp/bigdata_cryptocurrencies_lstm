#da cancellare prima di consegnare
from crypto_utility import test_set
TEST_SET = test_set.get_testset("../crypto_testset/from_2016_07_01_until_2017_06_26/test_set.txt")

for data_tester in TEST_SET:
    print(data_tester)