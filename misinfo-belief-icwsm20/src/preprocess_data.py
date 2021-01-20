#!/usr/local/bin/python3

import os, sys, re, html
import pandas as pd
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import words
wnl = WordNetLemmatizer()
tknzr = TweetTokenizer(preserve_case=True, reduce_len=True)
english_words = set(words.words())
trans_dict = dict([(ord(x), ord(y)) for x,y in zip(u"‘’´“”",  u"'''\"\"")])

def get_label(row):
    if row["DOES NOT"] == 1:
        return [0, 1]  # not believe
    elif row["DOES"] == 1:
        return [1, 0]  # believe
    else:
        return [0, 0]  # neither

# Pre-tokenizeation parse, replaces special tokens.
def pretoken_parse(t):
    if not t:
        return t
    elif "http" in t.lower():
        return "URLREF"
    else:
        return t
        
# Post-tokenizeation parse, replaces special tokens.
def posttoken_parse(t):
    if not t:
        return t
    elif t[0] == "@":
        return "USERREF"
    elif t.replace(".","").replace(",","").isdigit():
        return "NUMREF"
    else:
        return t

# Tokenizes tweets.
def tokenize(p):
    tokens = " ".join([pretoken_parse(token) for token in str(p).split(" ")])
    tokens = tknzr.tokenize(tokens)  # lower and tokenize
    num_english_words = [token in english_words for token in tokens]
    if sum(num_english_words) < 0.05 * len(tokens):  # At least 5% English words.
        return np.nan
    tokens = " ".join([posttoken_parse(token) for token in tokens])
    tokens = tokens.translate(trans_dict).strip()
    tokens = tokens.replace("\n", " ")
    if tokens[:3] == "RT ":
        tokens = " ".join(tokens[3:].split(":")[1:])
    tokens = html.unescape(tokens)
    tokens = re.sub("\s+", " ", tokens).strip()
    return tokens

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    corpus_path = os.path.join(sys_path, "resources", "corpus_token.pkl")
    data_path = os.path.join(sys_path, "data")
    raw_path = os.path.join(data_path, "annotations")
    train_path = os.path.join(data_path, "train.csv")
    test_path = os.path.join(data_path, "test.csv")
    predict_path = os.path.join(data_path, "predict.csv")

    # Cleans annotated data.
    dfs = []
    for _, _, file_names in os.walk(raw_path):
        for file_name in file_names:
            file_path = os.path.join(raw_path, file_name)
            df = pd.read_excel(file_path, skiprows=1)
            df["text"] = df["Unnamed: 2"]
            df["labels"] = df[["DOES NOT", "DOES"]].apply(get_label, axis=1)
            df = df.dropna(subset={"text"})
            df["text"] = df["text"].apply(tokenize)
            df = df.dropna(subset={"text"})
            df["group"] = file_name.split(", ")[2].split(" tweet")[0]
            dfs.append(df[["group", "text", "labels"]])
    df = pd.concat(dfs).reset_index()
    
    # Splits data.
    train = df.sample(frac=0.8)
    test = df.drop(index=train.index)
    
    # Saves data.
    for df, df_path in zip([train, test], [train_path, test_path]):
        df[["text", "labels"]].dropna().to_csv(df_path, index=False)
        df = pd.read_csv(df_path)
        df = df.dropna()
        df.to_csv(df_path, index=False)
    print("Done train and test sets.")
        
    # Cleans previous data for predictions.
    predict = pd.read_pickle(corpus_path)
    predict = predict[predict["type"] == "normal"]
    predict = predict.dropna(subset={"tokens"}).drop_duplicates(subset={"tokens"})
    predict["text"] = predict["tokens"].apply(tokenize)
    predict = predict.dropna(subset={"text"})
    predict[["id", "time", "text"]].to_csv(predict_path, index=False)
    predict = pd.read_csv(predict_path)
    predict = predict.dropna()
    predict[["id", "time", "text"]].to_csv(predict_path, index=False)
    print("Done predict set.")
