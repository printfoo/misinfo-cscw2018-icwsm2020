#!/usr/local/bin/python3

import os, sys, json, time
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec, LineSentence
from sklearn.cluster import MiniBatchKMeans, SpectralClustering
from sklearn.preprocessing import Normalizer

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    data_path = os.path.join(file_path, "data", "corpus_token.csv")
    corpus_path = os.path.join(file_path, "data", "corpus_w2v_corpus.txt")
    w2v_path = os.path.join(file_path, "data", "corpus_w2v.bin")
    cluster_path = os.path.join(file_path, "data", "corpus_w2v_cluster.ttsv")
    lex_path = os.path.join(file_path, "lexicon", "w2v_cluster", "w2v_cluster.tsv")
    
    # creat corpus
    if not os.path.exists(corpus_path):
        df = pd.read_csv(data_path)
        df = df[df["type"] == "normal"]
        df = df.dropna(subset = ["tokens"])
        with open(corpus_path, "w") as corpus_file:
            for line in df["tokens"].values:
                corpus_file.write(str(line) + "\n")
        sys.exit()

    # train word2vec model
    if not os.path.exists(w2v_path):
        sentences = LineSentence(corpus_path)
        w2v = Word2Vec(sentences, min_count = 100)
        w2v.save(w2v_path)
        sys.exit()

    # train cluster model
    #if not os.path.exists(cluster_path):
    else:
        w2v = Word2Vec.load(w2v_path)
        print(w2v.wv.most_similar(positive=["fuck"]))
        X = Normalizer().fit_transform(w2v.wv.syn0)
        #cluster_model = MiniBatchKMeans(n_clusters = 300, init_size = 5000)
        cluster_model = SpectralClustering(n_clusters = 300, n_jobs = 50)
        clusters = cluster_model.fit_predict(X)
        #print(cluster_model.score(X))
        f = open(cluster_path, "w")
        f.write("index\t\tcluster\t\ttoken\t\tcount\n")
        for i in range(len(clusters)):
            f.write(str(i) + "\t\t" + str(clusters[i]) + "\t\t" + w2v.wv.index2word[i] + \
                    "\t\t" + str(w2v.wv.vocab[w2v.wv.index2word[i]].count) + "\n")

        df = pd.read_csv(cluster_path, sep = "\t\t", engine = "python")
        clusters = df["cluster"].drop_duplicates().values
        f = open(lex_path, "w")
        for cluster in clusters:
            f.write(str(cluster))
            tokens = df[df["cluster"] == cluster]["token"].values
            for token in tokens:
                f.write("\t" + str(token))
            f.write("\n")
        f.close()
