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
    movie_path = os.path.join(file_path, "data", "review_movies")
    hotel_path = os.path.join(file_path, "data", "review_hotels")

    # tokenize
    wnl = WordNetLemmatizer()
    tknzr = TweetTokenizer(preserve_case = False, reduce_len = True)
    for raw_path in [movie_path, hotel_path]:
        save_path = raw_path + ".ttsv"
        save = open(save_path, "w")
        save.write("pos_neg\t\ttrue_fake\t\ttokens\n")
        for path, _, names in os.walk(raw_path):
            label1 = ""
            label2 = ""
            if "neg" in path.split("/")[-1]:
                label1 = "neg"
            if "pos" in path.split("/")[-1]:
                label1 = "pos"
            if "true" in path.split("/")[-1]:
                label2 = "true"
            if "fake" in path.split("/")[-1]:
                label2 = "fake"
            for name in names:
                with open(os.path.join(path, name), "r", errors = "ignore") as f:
                    s = f.read()
                s = tokenize(s)
                save.write(label1 + "\t\t" + label2 + "\t\t" + s + "\n")
