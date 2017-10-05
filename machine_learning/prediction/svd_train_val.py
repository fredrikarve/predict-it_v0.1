# Source:  https://github.com/songgc/TF-recomm
# Changes have been made so that the ratings.dat file serves as a training-set and
# the requests.dat- file serves as a test set. Currently the requests.dat can only contain one row,
# if more rows are inputted into requests.dat only the last one will be returned.
# The user-ID and item-ID gets it's ID reduced by one (if id = 3699, the output will be id = 3698.0)
# This is probably caused by line 10 and 11 in file dataio.py.

# ----------------------------
# Author Carl Eriksson
# Latest change 2017-09-30
# ----------------------------

import time
from collections import deque

import numpy as np
import tensorflow as tf
from six import next
from tensorflow.core.framework import summary_pb2

from machine_learning.prediction import dataio
from machine_learning.prediction import ops

import pandas as pd
from io import StringIO

import os

np.random.seed(13575)

BATCH_SIZE = 1000
USER_NUM = 6040
ITEM_NUM = 3952
DIM = 15
EPOCH_MAX = 2  # Originally set to 100, currently set to 10 for faster testing.
DEVICE = "/cpu:0"


def clip(x):
    return np.clip(x, 1.0, 5.0)


def make_scalar_summary(name, val):
    return summary_pb2.Summary(value=[summary_pb2.Summary.Value(tag=name, simple_value=val)])


def get_data():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../machine_learning/prediction/ml-1m/ratings.dat')
    filename = os.path.abspath(os.path.realpath(filename))
    df = dataio.read_process(filename, sep="::")
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../machine_learning/prediction/ml-1m/requests.dat')
    filename = os.path.abspath(os.path.realpath(filename))
    df2 = dataio.read_process(filename, sep="::")
    rows = len(df)
    df = df.iloc[np.random.permutation(rows)].reset_index(drop=True)
    df2 = df2.iloc[np.random.permutation(len(df2))].reset_index(drop=True)

    #Original code:---------------
    # split_index = int(rows * 0.9)
    # df_train = df[0:split_index]
    # df_test = df[split_index:].reset_index(drop=True)
    # return df_train, df_test
    #--------------------------------
    split_index = int(rows * 1)
    df_train = df[0:split_index]
    df_test = df[split_index:].reset_index(drop=True)
    return df_train, df2    # OBS, I'm not using df_test, instead I'm using df2, imported from ratings2.dat.
                            # df_test might be removed from the code when we know better how it works.
                            # all of the "split_index" related stuff might also be removed, not sure yet. -Calle

def svd(train, test):
    samples_per_batch = len(train) // BATCH_SIZE

    iter_train = dataio.ShuffleIterator([train["user"],
                                         train["item"],
                                         train["rate"]],
                                        batch_size=BATCH_SIZE)

    iter_test = dataio.OneEpochIterator([test["user"],
                                         test["item"],
                                         test["rate"]],
                                        batch_size=-1)

    user_batch = tf.placeholder(tf.int32, shape=[None], name="id_user")
    item_batch = tf.placeholder(tf.int32, shape=[None], name="id_item")
    rate_batch = tf.placeholder(tf.float32, shape=[None])

    infer, regularizer, predict = ops.inference_svd(user_batch, item_batch, user_num=USER_NUM, item_num=ITEM_NUM, dim=DIM,
                                           device=DEVICE)
    global_step = tf.contrib.framework.get_or_create_global_step()
    _, train_op = ops.optimization(infer, regularizer, rate_batch, learning_rate=0.001, reg=0.05, device=DEVICE)

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        summary_writer = tf.summary.FileWriter(logdir="/ml-1m", graph=sess.graph)
        print("{} {} {} {}".format("epoch", "train_error", "val_error", "elapsed_time"))
        errors = deque(maxlen=samples_per_batch)
        start = time.time()
        for i in range(EPOCH_MAX * samples_per_batch):
            users, items, rates = next(iter_train)
            _, pred_batch = sess.run([train_op, infer], feed_dict={user_batch: users,
                                                                   item_batch: items,
                                                                   rate_batch: rates})

            pred_batch = clip(pred_batch)

            errors.append(np.power(pred_batch - rates, 2))
            if i % samples_per_batch == 0:
                train_err = np.sqrt(np.mean(errors))
                test_err2 = np.array([])

                for users, items, rates in iter_test:
                    pred_batch = sess.run(infer, feed_dict={user_batch: users,
                                                            item_batch: items})

                    pred_batch = clip(pred_batch)

                   # for i in range (samples_per_batch):
                        # print("users: ", users[i])
                        # print("items: ", items[i])
                        # print("pred_batch: ", pred_batch[i])
                        # print("rates: ", rates[i])
                        # print("-----------------------")

                    test_err2 = np.append(test_err2, np.power(pred_batch - rates, 2))


                end = time.time()
                test_err = np.sqrt(np.mean(test_err2))
                print("{:3d} {:f} {:f} {:f}(s)".format(i // samples_per_batch, train_err, test_err,
                                                       end - start))
                train_err_summary = make_scalar_summary("training_error", train_err)
                test_err_summary = make_scalar_summary("test_error", test_err)
                summary_writer.add_summary(train_err_summary, i)
                summary_writer.add_summary(test_err_summary, i)
                start = end
                if i == (EPOCH_MAX-1) * samples_per_batch:
                    for j in range(0, pred_batch.size):
                        #print("pred_batch[", j, "]: ", pred_batch[j], "rate: ", rates[j])
                        prediction = [users[j], items[j], pred_batch[j]]
                        # This is the predicted rating for the user and id input in the file ratings2.dat.
                        # Currently only works for the last row in ratings2.dat. probably want to change it
                        # so it works for multiple users at the same time for efficiency.

        return prediction


if __name__ == '__main__':
    df_train, df_test = get_data()
    prediction = svd(df_train, df_test)

    print("Done!")

#This function takes in the id of a user and an item. The function will return a prediction of the users rating on the item
def get_rating(user_id, item_id):
    request_data = str(user_id) + '::' + str(item_id) + '::5::978298459'
    col_names = ["user", "item", "rate", "st"]
    request_data = pd.read_fwf(StringIO(request_data), delimiter="::", header=None, names=col_names, engine='python')
    for col in ("user", "item"):
        request_data[col] = request_data[col].astype(np.int32)
    request_data["rate"] = request_data["rate"].astype(np.float32)
    df_train, df_test = get_data()
    prediction = svd(df_train, request_data)
    rating = prediction[2]
    return rating
