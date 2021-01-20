import os, sys, json, nltk
from collections import defaultdict

# split only
def default_tokenizer(doc):
    return doc.split()

# map to lexicon
class lexiconMapper:
    def __init__(self, lex):
        self.cats = defaultdict(list)
        self.staging = {}
        self.inv_cache = {}
        self.load(os.path.join(sys.path[0][0:sys.path[0].find("src")], "lexicon", lex, lex + ".tsv"))

    def load(self,file):
        with open(file,"r") as f:
            for line in f:
                cols = line.strip().split("\t")
                name = cols[0]
                terms = cols[1:]
                for t in set(terms):
                    self.cats[name].append(t)

    def analyze(self, doc, categories = None, tokenizer = "default", normalize = False):
        if isinstance(doc,list):
            doc = "\n".join(doc)
        if tokenizer == "default":
            tokenizer = default_tokenizer
        elif tokenizer == "no_punc":
            tokenizer = no_punc_tokenizer
        if not hasattr(tokenizer,"__call__"):
            raise Exception("invalid tokenizer")
        if not categories:
            categories = self.cats.keys()
        invcats = defaultdict(list)
        key = tuple(sorted(categories))
        if key in self.inv_cache:
            invcats = self.inv_cache[key]
        else:
            for k in categories:
                for t in self.cats[k]: invcats[t].append(k)
            self.inv_cache[key] = invcats
        count = {}
        tokens = 0.0
        for cat in categories: count[cat] = 0.0
        for tk in tokenizer(doc):
            tokens += 1.0
            for cat in invcats[tk]:
                count[cat]+=1.0
        if normalize:
            for cat in count.keys():
                if tokens == 0:
                    return None
                else:
                    count[cat] = count[cat] / tokens
        return count
