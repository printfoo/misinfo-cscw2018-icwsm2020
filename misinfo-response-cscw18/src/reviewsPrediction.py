#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from sklearn import linear_model, svm
from sklearn import neural_network
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from scipy.stats import pearsonr, spearmanr, ttest_ind, ttest_rel
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]

# run different models
def run_model(X_train, X_test, y_train, y_test):
    reg = svm.LinearSVC(C = 100, random_state = 0)
    reg.fit(X_train, y_train)
    y_predict = reg.predict(X_test)
    acc = accuracy_score(y_predict, y_test)
    return acc

# compute
def compute():

    df = pd.read_csv(data_apth)
    if type == "hotels":
        df = df[df["pos_neg"] == "pos"]
        df["y"] = df["true_fake"].apply(lambda s: 1 if s == "true" else 0)
    elif type == "movies":
        df["y"] = df["pos_neg"].apply(lambda s: 1 if s == "pos" else 0)
    sel = [cluster for cluster in df.columns if cluster.isdigit()]
    y = df["y"].values
    X = df[sel].values
    kf = KFold(n_splits = fold, random_state = 0, shuffle = True)
    acc_list = []
    for train_index, test_index in kf.split(y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        acc = run_model(X_train, X_test, y_train, y_test)
        acc_list.append(acc)
    return acc_list

# show results
def show():
    with open(save_path, "r") as f:
        js = json.loads(f.read())
    for name in js:
        print(name, sum(js[name]) / fold)

# main
if __name__ == "__main__":
    
    # get path
    save_path = os.path.join(file_path, "results", "review_results.json")
    fold = 10
    res_dict = {}

    # compute result
    for type in ["hotels", "movies"]:
        data_apth = os.path.join(file_path, "data", "review_" + type + "_sentiment_w2v_cluster.csv")
        acc_list = compute()
        res_dict[type] = acc_list
    with open(save_path, "w") as f:
        f.write(json.dumps(res_dict))

    # show result
    show()
