# This file was just used to test if the svd_train_val could be called from somewhere else.
# Maybe it can serve as an interface to the machine learning algorithm.
# ----------------------------
# Author Carl Eriksson
# Latest change 2017-09-30
# ----------------------------
from machine_learning.prediction import svd_train_val

if __name__ == '__main__':
    x = svd_train_val.get_rating('1', '2')
    print(x)
