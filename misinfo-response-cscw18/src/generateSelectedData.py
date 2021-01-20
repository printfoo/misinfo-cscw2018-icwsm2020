#!/usr/local/bin/python3

import os, sys, json, random, time
import pandas as pd
import numpy as np
import hashlib, base64

# aggregate text
def agg_coms(g):
    return "\n".join(g["tokens"].values)

# main
if __name__ == "__main__":

    # agg tokens
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]

    # public fact-check
    factcheck_path = os.path.join(file_path, "data", "selected_factcheck_v2.xlsx")
    factcheck1 = pd.read_excel(factcheck_path)
    factcheck1_col = [c for c in factcheck1.columns if c not in ["social_id", "comments"]]
    factcheck1 = factcheck1[factcheck1_col]
    factcheck2_path = os.path.join(file_path, "data", "factcheck.csv")
    factcheck2 = pd.read_csv(factcheck2_path)
    factcheck2 = factcheck2[["factcheck", "href", "social_id"]]
    factcheck = factcheck2.merge(factcheck1, on=["factcheck", "href"])
    factcheck["social_id"] = factcheck["social_id"].astype("str")

    # public corpus
    token_path = os.path.join(file_path, "data", "corpus_token.pkl")
    token_df = pd.read_pickle(token_path)
    token_df = token_df[token_df["type"] == "normal"]
    token_df = token_df.dropna(subset = {"site", "id", "tokens"})
    token_df = token_df.fillna("")
    token_df["social_id"] = token_df["id"].astype("str")
    token_df["comment_time"] = token_df["time"].astype("int")
    token_df = token_df.groupby(["social_id", "name", "comment_time"]).apply(agg_coms).reset_index(name = "comment_content")
    token_df = token_df[["social_id", "comment_time", "comment_content"]]
    
    # merge
    df = factcheck.merge(token_df, on="social_id")
    info_path = os.path.join(file_path, "data", "belief_annotation_v2", "info")
    comm_path = os.path.join(file_path, "data", "belief_annotation_v2", "comments")
    for id, comm in df.groupby("social_id"):
        id = id.split(":")[-1]
        info = comm[factcheck.columns].head(1)
        info.to_csv(os.path.join(info_path, id + ".csv"), index=False)
        comm = comm[["comment_time", "comment_content"]].sort_values("comment_time")
        comm = comm.head(1000)
        comm.to_csv(os.path.join(comm_path, id + ".csv"))

