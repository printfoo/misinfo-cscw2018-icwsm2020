#!/usr/local/bin/python3

from bs4 import BeautifulSoup
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import os, sys, json, time, re, string

# votesmart parser
class votesmartParser:
    # initialization
    def __init__(self, raw_path, save_path):
        self.raw_path = raw_path
        self.save_path = save_path
        self.wnl = WordNetLemmatizer()
        self.tknzr = TweetTokenizer(preserve_case = False, reduce_len = True)

    # write one record
    def write(self, tokens):
        self.bif = open(os.path.join(save_path, "bigrams.tsv"), "a")
        for i in range(len(tokens) - 1):
            token = tokens[i] + "_" + tokens[i + 1]
            if self.party == "rep":
                self.bif.write(token + "\t1\t0\n")
            if self.party == "dem":
                self.bif.write(token + "\t0\t1\n")
        self.unif = open(os.path.join(save_path, "unigrams.tsv"), "a")
        for i in range(len(tokens)):
            token = tokens[i]
            if self.party == "rep":
                self.unif.write(token + "\t1\t0\n")
            if self.party == "dem":
                self.unif.write(token + "\t0\t1\n")

    # parse records one by one
    def parse(self, tmp_f):
        soup = BeautifulSoup(tmp_f, "html.parser")
        for div in soup.find_all("div"):
            if div.get("itemprop"):
                if "articleBody" in div.get("itemprop"):
                    text = div.get_text().replace(r"\n", "\n").replace(r"\'", "'").replace("-", "")
                    text = re.sub("Source:", "", text)
                    text = re.sub(r"http\S+", "", text)
                    text = re.sub(r"[^\w\s]","", text)
                    tokens = self.tknzr.tokenize(text) # lower and tokenize
                    tokens = [self.wnl.lemmatize(token, "n") for token in tokens] # lemmatization noun
                    tokens = [self.wnl.lemmatize(token, "v") for token in tokens] # lemmatization verb
                    tokens = [token for token in tokens if token not in stops]
                    self.write(tokens)

    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(raw_path):
            for path_postfix in path_postfixes:
                print(path_postfix)
                self.party = path_base.split("/")[-1].split("_")[1]
                with open(os.path.join(path_base, path_postfix), "r") as tmp_f:
                    self.parse(tmp_f)

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "votesmart_raw", "speeches")
    save_path = os.path.join(file_path, "data", "votesmart_token")
    csv_path = os.path.join(file_path, "data", "votesmart.csv")
    cmd = sys.argv[1]
    stops = set(stopwords.words("english"))
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    if cmd == "token":
        with open(os.path.join(save_path, "unigrams.tsv"), "w") as f:
            f.write("\t".join(["token", "rep", "dem"]) + "\n")
        with open(os.path.join(save_path, "bigrams.tsv"), "w") as f:
            f.write("\t".join(["token", "rep", "dem"]) + "\n")
        # crawler initilization
        votesmart = votesmartParser(raw_path, save_path)
        votesmart.traverse()

    elif cmd == "count":
        unidf = pd.read_csv(os.path.join(save_path, "unigrams.tsv"), sep = "\t")
        unidf = unidf.groupby("token").sum()
        unidf["ngram"] = 1
        bidf = pd.read_csv(os.path.join(save_path, "bigrams.tsv"), sep = "\t")
        bidf = bidf.groupby("token").sum()
        bidf["ngram"] = 2
        df = pd.concat([unidf, bidf])
        df.to_csv(csv_path)
        print(df)
