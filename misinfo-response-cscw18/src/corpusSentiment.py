#!/usr/local/bin/python3

import os, sys, json, random, time
import pandas as pd
import numpy as np
from lexiconSentimentAnalyzer import lexiconMapper

# aggregate text
def agg_tokens(g):
    return " ".join(g["tokens"].values)

# get sentiment
def get_sentiment(r):
    dict = lexicon.analyze(r["tokens"], normalize = True)
    if dict:
        for key in dict:
            r[key] = dict[key]
    return r

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    aim = "agg"
    try:
        lex = sys.argv[1].lower()
    except:
        lex = "w2v_cluster"

    # agg tokens
    token_path = os.path.join(file_path, "data", "corpus_token.csv")
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    agg_path = os.path.join(file_path, "data", "corpus_token_" + aim + ".csv")
    if aim == "agg" and (not os.path.exists(agg_path)):
        token_df = pd.read_csv(token_path)
        token_df = token_df[token_df["type"] == "normal"]
        factcheck = pd.read_csv(factcheck_path)
        df = factcheck.merge(token_df, left_on = "social_id", right_on = "id", how = "inner")
        df = df.dropna(subset = ["tokens", "ruling_val"])
        df["time_lag"] = df["time"] - df["ruling_time"]
        df["after_checked"] = np.sign(df["time_lag"])
        df = df.groupby(["id", "ruling_val", "after_checked"]).apply(agg_tokens).reset_index(name = "tokens")
        df.to_csv(agg_path, index = False)
        print(df)
        sys.exit()

    # map sentiment
    senti_path = os.path.join(file_path, "data", "corpus_sentiment_" + lex + ".csv")
    df = pd.read_csv(agg_path)
    lexicon = lexiconMapper(lex)
    df = df.apply(get_sentiment, axis = 1)
    df = df.drop(["tokens"], axis = 1)
    df.to_csv(senti_path, index = False)

