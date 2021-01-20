#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, ttest_ind, ttest_rel
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]

# check potential backfire
def check_example(t):
    t = str(t)
    if "fake" in t:
        return True
    else:
        return False

# main
if __name__ == "__main__":
    
    # get path
    token_path = os.path.join(file_path, "data", "corpus_token.csv")
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")

    factcheck = pd.read_csv(factcheck_path)
    token_df = pd.read_csv(token_path)
    token_df = token_df[token_df["type"] == "normal"]
    df = factcheck.merge(token_df, left_on = "social_id", right_on = "id", how = "inner")

    #df = df[df["ruling_val"] == 1]
    df["example"] = df["tokens"].apply(lambda t: True if "😳" in str(t) else False)
    df = df[df["example"]]
    for v in df["tokens"].values:
        if len(v) < 100:
            print(v)
