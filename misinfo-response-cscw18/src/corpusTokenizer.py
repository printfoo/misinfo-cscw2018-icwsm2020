#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer

# replace urls to other tokens
def http_parse(t):
    if "snopes" in t:
        return "snopesref"
    elif "politifact" in t:
        return "politifactref"
    elif "http" in t:
        return "urlref"
    else:
        return t

# tokenize sentence
def tokenize(p):
    tokens = p.split(" ")
    tokens = [http_parse(token.lower()) for token in tokens]
    p = " ".join(tokens)
    tokens = tknzr.tokenize(p) # lower and tokenize
    tokens = [wnl.lemmatize(token, "n") for token in tokens] # lemmatization noun
    tokens = [wnl.lemmatize(token, "v") for token in tokens] # lemmatization verb
    return " ".join(tokens)
    #tokens = [token for token in tokens if token.isalpha()] # remove punctuation

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    youtube_path = os.path.join(file_path, "data", "youtube.json")
    facebook_path = os.path.join(file_path, "data", "facebook.json")
    twitter_path = os.path.join(file_path, "data", "twitter.json")
    save_path = os.path.join(file_path, "data", "corpus_token.csv")
    pickle_path = os.path.join(file_path, "data", "corpus_token.pkl")

    # tokenize
    wnl = WordNetLemmatizer()
    tknzr = TweetTokenizer(preserve_case = False, reduce_len = True)
    youtube = pd.read_json(youtube_path, lines = True)
    youtube["site"] = "youtube"
    facebook = pd.read_json(facebook_path, lines = True)
    facebook["site"] = "facebook"
    twitter = pd.read_json(twitter_path, lines = True)
    twitter["site"] = "twitter"
    df = pd.concat([youtube, facebook, twitter])
    df = df.dropna(subset = ["paragraph"])
    df["tokens"] = df["paragraph"]#.apply(tokenize)
    df = df.drop(columns = ["paragraph"])
    df = df.dropna(subset = ["tokens"])
    df.to_csv(save_path, index=False)
    df.to_pickle(pickle_path)
    df = pd.read_pickle(pickle_path)
