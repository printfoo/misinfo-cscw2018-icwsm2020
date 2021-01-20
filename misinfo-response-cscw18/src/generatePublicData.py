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
    
    # public lexicon
    lex_path = os.path.join(file_path, "lexicon", "w2v_cluster", "w2v_cluster.txt")
    lex_name = os.path.join(file_path, "lexicon", "w2v_cluster", "cluster_names.csv")
    lex_save_path = os.path.join(file_path, "public_data", "ComLex.csv")
    with open(lex_path, "r") as lex_f:
        lex = lex_f.read().strip("\n").split("\n")
    lex = [cluster.split("\t") for cluster in lex]
    lex = [{"cluster_num": cluster[0], "tokens": "|".join(cluster[1:])} for cluster in lex]
    lex = pd.DataFrame(lex)
    names = pd.read_csv(lex_name)
    names["info"] = names["info"].apply(lambda s: np.nan if s[-1] == "." else s)
    lex = lex.merge(names, on = "cluster_num", how = "left")
    lex = lex[["name", "info", "tokens"]].sort_values("name")
    lex.to_csv(lex_save_path, index = False)

    # public fact-check
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    factcheck_save_path = os.path.join(file_path, "public_data", "factchecks.csv")
    factcheck = pd.read_csv(factcheck_path)
    factcheck["ruling_time"] = factcheck["ruling_time"].astype("int")
    factcheck = factcheck[["social_id", "site", "checkedby", "ruling", "ruling_time", "ruling_val"]]
    factcheck = factcheck.dropna()
    factcheck.to_csv(factcheck_save_path, index = False)

    # public corpus
    token_path = os.path.join(file_path, "data", "corpus_token.csv")
    token_save_path = os.path.join(file_path, "public_data", "comments")
    token_df = pd.read_csv(token_path)
    token_df = token_df[token_df["type"] == "normal"]
    token_df = token_df.dropna(subset = {"site", "id"})
    token_df = token_df.fillna("")
    token_df["social_id"] = token_df["id"]
    token_df["comment_time"] = token_df["time"].astype("int")
    df = token_df.groupby(["site", "social_id", "name", "comment_time"]).apply(agg_coms).reset_index(name = "comment_tokens")
    df["username_hash"] = df["name"].apply(lambda s: hashlib.md5((s + "123").encode("utf-8")).hexdigest() if s != "unknown" else s)
    df = df[["site", "social_id", "username_hash", "comment_time", "comment_tokens"]]
    for site in {"youtube", "twitter", "facebook"}:
        tdf = df[df["site"] == site]
        tdf.to_csv(os.path.join(token_save_path, site + ".bz2"), index = False, compression = "bz2")
    print(df)
