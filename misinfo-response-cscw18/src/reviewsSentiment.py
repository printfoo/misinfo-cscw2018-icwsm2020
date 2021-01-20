#!/usr/local/bin/python3

import os, sys, json, random, time
import pandas as pd
import numpy as np
from lexiconSentimentAnalyzer import lexiconMapper

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
    try:
        lex = sys.argv[1].lower()
    except:
        lex = "w2v_cluster"

    # map sentiment
    lexicon = lexiconMapper(lex)

    movie_path = os.path.join(file_path, "data", "review_movies")
    hotel_path = os.path.join(file_path, "data", "review_hotels")
    for raw_path in [movie_path, hotel_path]:
        corpus_path = raw_path + ".ttsv"
        senti_path = raw_path + "_sentiment_" + lex + ".csv"
        df = pd.read_csv(corpus_path, sep = "\t\t", engine = "python")
        df = df.dropna(subset = ["tokens"])
        df = df.apply(get_sentiment, axis = 1)
        df = df.drop(["tokens"], axis = 1)
        df.to_csv(senti_path, index = False)

