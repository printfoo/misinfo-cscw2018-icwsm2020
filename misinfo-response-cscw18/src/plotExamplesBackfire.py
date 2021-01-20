#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, ttest_ind, ttest_rel
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]

# check potential backfire
def check_potential_backfire(t):
    t = str(t)
    if ("snopesref" in t or "politifactref" in t) and ("fuck" in t or "fck" in t or "fuk" in t or "dam" in t):
        return True
    else:
        return False

# main
if __name__ == "__main__":
    
    # get path
    token_path = os.path.join(file_path, "data", "corpus_token.csv")
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    potential_path = os.path.join(file_path, "data", "potential_backfire.csv")

    factcheck = pd.read_csv(factcheck_path)
    token_df = pd.read_csv(token_path)
    token_df = token_df[token_df["type"] == "normal"]
    token_df["potential_backfire"] = token_df["tokens"].apply(check_potential_backfire)
    token_df = token_df[token_df["potential_backfire"]]
    df = factcheck.merge(token_df, left_on = "social_id", right_on = "id", how = "inner")
    df.to_csv(potential_path, index = False)

    df = pd.read_csv(potential_path)
    print(df["href"].values)
