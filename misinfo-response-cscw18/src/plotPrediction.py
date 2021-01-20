#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from sklearn import linear_model, svm, neural_network, preprocessing
from sklearn.model_selection import KFold
from sklearn.metrics import coverage_error, label_ranking_average_precision_score, label_ranking_loss
from scipy.stats import pearsonr, spearmanr, ttest_ind, ttest_rel
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]

# get a matrix in order to compute metrics
def get_matrix(y):
    matrix = []
    for _y in y:
        if _y <= -1.5:
            matrix.append([1,0,0,0,0])
        elif _y <= -0.5:
            matrix.append([0,1,0,0,0])
        elif _y <= 0.5:
            matrix.append([0,0,1,0,0])
        elif _y <= 1.5:
            matrix.append([0,0,0,1,0])
        else:
            matrix.append([0,0,0,0,1])
    return matrix

# run different models
def run_model(name, X_train, X_test, y_train, y_test):
    if name == "random":
        y_predict = np.random.randint(low = 1, high = 6, size = len(y_test))
    elif name == "alltrue":
        y_predict = [2 for _ in range(len(y_test))]
    elif name == "allfalse":
        y_predict = [-2 for _ in range(len(y_test))]
    elif name == "linear":
        reg = linear_model.LinearRegression()
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "ridge":
        reg = linear_model.Ridge(alpha = 0.1, random_state = 0)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "lasso":
        reg = linear_model.Lasso(alpha = 0.0001, random_state = 0)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "svml1":
        reg = svm.LinearSVR(loss = "epsilon_insensitive", random_state = 0, C = 10) #l1
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "svml2":
        reg = svm.LinearSVR(loss = "squared_epsilon_insensitive", random_state = 0, C = 10) #l2
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "dnn10":
        reg = neural_network.MLPRegressor(hidden_layer_sizes=(10,), random_state = 1, max_iter = 200)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "dnn50":
        reg = neural_network.MLPRegressor(hidden_layer_sizes=(50,), random_state = 0, max_iter = 200)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "dnn100":
        reg = neural_network.MLPRegressor(hidden_layer_sizes=(100,), random_state = 0, max_iter = 200)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "dnn500":
        reg = neural_network.MLPRegressor(hidden_layer_sizes=(500,), random_state = 0, max_iter = 200)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    elif name == "dnn1000":
        reg = neural_network.MLPRegressor(hidden_layer_sizes=(1000,), random_state = 0, max_iter = 200)
        reg.fit(X_train, y_train)
        y_predict = reg.predict(X_test)
    rho, p = spearmanr(y_predict, y_test)
    y_true = get_matrix(y_test)
    y_score = get_matrix(y_predict)
    ce = coverage_error(y_true, y_score)
    lrap = label_ranking_average_precision_score(y_true, y_score)
    lrl = label_ranking_loss(y_true, y_score)
    return rho, ce, lrap, lrl

# compute
def compute():

    df = pd.read_csv(senti_path)
    #sig = pd.read_csv(sig_clusters_path1)
    #df = df[df["after_checked"] == -1]
    y = df["ruling_val"].values
    X = df[df.columns[3:]].values
    if lex == "liwc":
        X = preprocessing.normalize(X, norm = "l2")
    kf = KFold(n_splits = 10, random_state = 0, shuffle = True)
    res_dict = {}
    for name in names:
        res_dict[name] = {}
        res_dict[name]["rho"] = []
        #res_dict[name]["ce"] = []
        res_dict[name]["lrap"] = []
        res_dict[name]["lrl"] = []
    for train_index, test_index in kf.split(y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        for name in names:
            rho, ce, lrap, lrl = run_model(name, X_train, X_test, y_train, y_test)
            res_dict[name]["rho"].append(rho)
            #res_dict[name]["ce"].append(ce)
            res_dict[name]["lrap"].append(lrap)
            res_dict[name]["lrl"].append(lrl)
    with open(save_path, "w") as f:
        f.write(json.dumps(res_dict))

# show results
def show():
    with open(save_path, "r") as f:
        js = json.loads(f.read())
    for name in names:
        print(name)
        for metric in ["rho", "lrap", "lrl"]:
            print(round(sum(js[name][metric])/10, 3), "&", end = "\t")
        print()

# main
if __name__ == "__main__":
    
    # get path
    dict = {"emolex": "emolex", "comlex": "w2v_cluster", "liwc": "liwc"}
    try:
        lex = sys.argv[1].lower()
    except:
        exit()
    if lex not in dict:
        exit()
    
    senti_path = os.path.join(file_path, "data", "corpus_sentiment_" + dict[lex] + ".csv")
    save_path = os.path.join(file_path, "results", "regression_results_" + lex + ".json")

    names = ["random", "alltrue", "allfalse", "linear", "lasso", "ridge", "svml1", "svml2", "dnn50", "dnn100", "dnn500", "dnn1000"]
    compute()
    show()
