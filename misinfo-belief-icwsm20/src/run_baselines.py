#!/usr/local/bin/python3

import os, sys
import random
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.preprocessing import normalize
from sklearn.linear_model import LogisticRegression

def get_chance(l):
    return [random.random(), random.random()]

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    
    
    # Chance.
    train_path = os.path.join(data_path, "train.csv")
    train_chance_path = os.path.join(data_path, "train_chance_pred.csv")
    chance_df = pd.read_csv(train_path)
    chance_df["labels"] = chance_df["labels"].apply(lambda l: eval(l))
    chance_df["predictions"] = chance_df["labels"].apply(get_chance)
    chance_df.to_csv(train_chance_path, index=False)

    test_path = os.path.join(data_path, "test.csv")
    test_chance_path = os.path.join(data_path, "test_chance_pred.csv")
    chance_df = pd.read_csv(test_path)
    chance_df["labels"] = chance_df["labels"].apply(lambda l: eval(l))
    chance_df["predictions"] = chance_df["labels"].apply(get_chance)
    chance_df.to_csv(test_chance_path, index=False)
    
    # LIWC
    train_liwc_path = os.path.join(data_path, "train_liwc+lr_pred.csv")
    test_liwc_path = os.path.join(data_path, "test_liwc+lr_pred.csv")
    train_path = os.path.join(data_path, "train_liwc.csv")
    test_path = os.path.join(data_path, "test_liwc.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    assert test_df.columns.tolist() == test_df.columns.tolist()
    
    pred_Y = {"train": [], "test": []}
    for label in [0, 1]:
        train_Y = train_df["labels"].apply(lambda l: eval(l)[label]).values
        train_X = train_df[train_df.columns[2:]].values
        test_X = test_df[test_df.columns[2:]].values
        model = LogisticRegression(random_state=0, solver="lbfgs", max_iter=10000)
        model.fit(train_X, train_Y)
        pred_Y["train"].append([prob[1] for prob in model.predict_proba(train_X)])
        pred_Y["test"].append([prob[1] for prob in model.predict_proba(test_X)])
    predictions = [[pred1, pred2] for pred1, pred2 in zip(pred_Y["train"][0], pred_Y["train"][1])]
    train_df["predictions"] = predictions
    train_df[["text", "labels", "predictions"]].to_csv(train_liwc_path, index=False)
    predictions = [[pred1, pred2] for pred1, pred2 in zip(pred_Y["test"][0], pred_Y["test"][1])]
    test_df["predictions"] = predictions
    test_df[["text", "labels", "predictions"]].to_csv(test_liwc_path, index=False)
    
    
    # ComLex
    train_comlex_path = os.path.join(data_path, "train_comlex+lr_pred.csv")
    test_comlex_path = os.path.join(data_path, "test_comlex+lr_pred.csv")
    train_path = os.path.join(data_path, "train_comlex.csv")
    test_path = os.path.join(data_path, "test_comlex.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    assert test_df.columns.tolist() == test_df.columns.tolist()

    pred_Y = {"train": [], "test": []}
    for label in [0, 1]:
        train_Y = train_df["labels"].apply(lambda l: eval(l)[label]).values
        train_X = train_df[train_df.columns[3:]].values
        test_X = test_df[test_df.columns[3:]].values
        model = LogisticRegression(random_state=0, solver="lbfgs", max_iter=10000)
        model.fit(train_X, train_Y)
        pred_Y["train"].append([prob[1] for prob in model.predict_proba(train_X)])
        pred_Y["test"].append([prob[1] for prob in model.predict_proba(test_X)])
    predictions = [[pred1, pred2] for pred1, pred2 in zip(pred_Y["train"][0], pred_Y["train"][1])]
    train_df["predictions"] = predictions
    train_df[["text", "labels", "predictions"]].to_csv(train_comlex_path, index=False)
    predictions = [[pred1, pred2] for pred1, pred2 in zip(pred_Y["test"][0], pred_Y["test"][1])]
    test_df["predictions"] = predictions
    test_df[["text", "labels", "predictions"]].to_csv(test_comlex_path, index=False)
