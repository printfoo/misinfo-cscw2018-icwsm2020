#!/usr/local/bin/python3

import os, sys, json, time
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec, LineSentence
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.size"] = 8
font = FontProperties()
font.set_size(8)
font.set_weight("bold")

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    w2v_path = os.path.join(file_path, "data", "corpus_w2v.bin")
    cluster_path = os.path.join(file_path, "data", "corpus_w2v_cluster.ttsv")
    fig_path = os.path.join(file_path, "results", "factcheck_cluster.pdf")

    tsne = TSNE(n_components = 2, random_state = 2)
    w2v = Word2Vec.load(w2v_path)
    cluster = pd.read_csv(cluster_path, sep = "\t\t", engine = "python")
    fake1 = cluster[cluster["cluster"] == 235]
    p1 = len(fake1)
    fake2 = cluster[cluster["cluster"] == 153]
    p2 = len(fake2) + p1
    fake3 = cluster[cluster["cluster"] == 99]
    p3 = len(fake3) + p2
    fact = cluster[cluster["cluster"] == 278]
    #cluster["vector"] = cluster["token"].apply(lambda t: list(w2v.wv[t]))
    #snopes = list(fact["token"].values).index("snopesref")
    #politifact = list(fact["token"].values).index("politifactref")
    df = pd.concat([fake1, fake2, fake3, fact])
    #df = cluster.dropna(subset = ["token"])
    X = w2v[df["token"].values]
    X_r = tsne.fit_transform(X)
    
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3.6, 1.5))
    """
    for i, row in enumerate(cluster[["token", "cluster"]].values):
        word = row[0]
        cluster = row[1]
        if cluster == 278:
            ax.scatter(X_r[i, 0], X_r[i, 1], c = "seagreen")
        else:
            ax.scatter(X_r[i, 0], X_r[i, 1], c = "indianred")
    """
    ax.scatter(X_r[p3:][:, 0], X_r[p3:][:, 1], color = "seagreen", alpha = 0.6, lw = 0, s = 40,
               label = r"$\bf{Fact}$ [n.] $\it{(fact,evidence,data)}$")
    ax.scatter(X_r[:p1][:, 0], X_r[:p1][:, 1], color = "indianred", alpha = 0.6, lw = 0, s = 40,
               label = r"$\bf{Fake}$ [v.] $\it{(fake,mislead,fabricate)}$")
    ax.scatter(X_r[p2:p3][:, 0], X_r[p2:p3][:, 1], color = "maroon", alpha = 0.6, lw = 0, s = 40,
               label = r"$\bf{Fake}$ [somewhat fake] $\it{(propaganda,rumor,distortion)}$")
    ax.scatter(X_r[p1:p2][:, 0], X_r[p1:p2][:, 1], color = "r", alpha = 0.6, lw = 0, s = 30,
               label = r"$\bf{Fake}$ [very fake] $\it{(hoax,scam,conspiracy)}$")
    #ax.scatter(X_r[snopes, 0], X_r[snopes, 1], color = "k", lw = 0, s = 120)
    #ax.scatter(X_r[politifact, 0], X_r[politifact, 1], color = "k", lw = 0, s = 120)
    for i, word in enumerate(df["token"].values):
        if word == "snopesref":
            ax.annotate(word, xy=(X_r[i, 0], X_r[i, 1]), va = "bottom", ha = "center", fontproperties = font)
        if word == "politifactref":
            ax.annotate(word, xy=(X_r[i, 0], X_r[i, 1]), va = "top", ha = "center", fontproperties = font)
    #ax.set_xlim([X_r[:, 0].min() - 4, X_r[:, 0].max() + 1])
    #ax.set_ylim([X_r[:, 1].min() - 3, X_r[:, 1].max() + 1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("tSNE dimension 1", fontproperties = font)
    ax.set_ylabel("tSNE dimension 2", fontproperties = font)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    leg = ax.legend(bbox_to_anchor=(1.62, 0.3, 0, 0), loc = "center", ncol = 1, borderaxespad = 0.)
    leg.get_frame().set_alpha(0)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)

