#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]

# combine all tokens in each cluster
def combine_tokens(g):
    words = g.sort_values("count", ascending = False)["token"].values
    words = [str(w) for w in words]
    return pd.Series({"words": ", ".join(words)})

# main
if __name__ == "__main__":
    
    # get path
    names_path = os.path.join(file_path, "lexicon", "w2v_cluster", "cluster_names.csv")
    cluster_path = os.path.join(file_path, "lexicon", "w2v_cluster", "corpus_w2v_cluster.ttsv")
    spreadsheet_path = os.path.join(file_path, "lexicon", "w2v_cluster", "to_rate.csv")

    # read data
    cluster = pd.read_csv(cluster_path, sep = "\t\t", engine = "python")
    cluster = cluster.groupby("cluster_num").apply(combine_tokens)
    cluster["cluster_num"] = cluster.index.astype("str")
    names = pd.read_csv(names_path)
    df = cluster.merge(names, on = "cluster_num")
    df = df[["words", "name", "info"]]
    df["info"] = df["info"].apply(lambda s: "" if s[-1] == "." else s)
    df["rating_1"] = ""
    df["rating_2"] = ""
    df.to_csv(spreadsheet_path, index = False)
    print(df)
