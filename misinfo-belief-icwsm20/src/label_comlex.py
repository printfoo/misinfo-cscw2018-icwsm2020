#!/usr/local/bin/python3

import os, sys, re, html
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
wnl = WordNetLemmatizer()
tknzr = TweetTokenizer(preserve_case=False, reduce_len=True)

# get linguistic features
def get_linguistic(t, ts):
    return len(set(t.split(" ")).intersection(ts))

# tokenize tweets
def lemmatize(t):
    tokens = t.lower().split()
    tokens = [wnl.lemmatize(token, "n") for token in tokens] # lemmatization noun
    tokens = [wnl.lemmatize(token, "v") for token in tokens] # lemmatization verb
    return " ".join(tokens)

# Labels comlex.
def label_comlex(df):
    for name, info, tokens in lex.values:
        ts = tokens.split("|")
        col_name = ":::".join([str(name), str(info), "|".join(ts[:5])])
        df[col_name] = df["text"].apply(lambda t: get_linguistic(t, ts))
    return df
    
if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    train_path = os.path.join(data_path, "train.csv")
    test_path = os.path.join(data_path, "test.csv")
    lex_path = os.path.join(sys_path, "resources", "ComLex.csv")
    lex = pd.read_csv(lex_path)

    # Labels ComLex.
    for path in [train_path, test_path]:
        df = pd.read_csv(path)
        df["lemmas"] = df["text"].apply(lemmatize)
        df = label_comlex(df)
        df.to_csv(path.replace(".csv", "_comlex.csv"), index=False)
