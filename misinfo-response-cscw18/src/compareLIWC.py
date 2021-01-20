#!/usr/local/bin/python3

import os, sys, json, random, time
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr, ttest_ind, ttest_rel
from sklearn import linear_model, svm, tree
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
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
font2 = FontProperties()
font2.set_size(7)

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    w2v_path = os.path.join(file_path, "data", "corpus_sentiment_w2v_cluster.csv")
    liwc_path = os.path.join(file_path, "data", "corpus_sentiment_liwc.csv")
    fig_path = os.path.join(file_path, "results", "compare_liwc.pdf")

    w2v = pd.read_csv(w2v_path)
    w2v_col = w2v.columns[3:]
    liwc = pd.read_csv(liwc_path)
    liwc_col = liwc.columns[4:]
    ttdf = w2v.merge(liwc, on = ["id", "ruling_val", "after_checked"])
    """
    for c1 in w2v_col:
        for c2 in liwc_col:
            tdf = ttdf[[c1, c2]].dropna()
            r, p = pearsonr(tdf[c1], tdf[c2])
            if r > 0.8:
                print(c1, c2, r)
    """

    fig = plt.subplots(figsize=(6, 1.5))
    gs = GridSpec(1, 12)
    ax = [None for i in range(3)]
    ax[0] = plt.subplot(gs[0, 1:4])
    ax[1] = plt.subplot(gs[0, 5:8])
    ax[2] = plt.subplot(gs[0, 9:12])
    c = matplotlib.cm.get_cmap("Blues")
    for i, cats in zip([0, 1, 2], [["family", "250"], ["pronoun", "236"], ["prep", "91"]]):
        tdf = ttdf[cats].dropna()
        r, p = pearsonr(tdf[cats[0]], tdf[cats[1]])
        ax[i].scatter(tdf[cats[0]], tdf[cats[1]], alpha = 0.2, c = c(0.9), s = 5, linewidth = 0)
        ax[i].set_xlim(0, tdf[cats[0]].quantile(0.99))
        ax[i].set_ylim(0, tdf[cats[1]].quantile(0.99))
        ax[i].spines["right"].set_visible(False)
        ax[i].spines["top"].set_visible(False)
        ax[i].set_ylabel("ComLex", fontproperties = font)
        ax[i].text(tdf[cats[0]].quantile(0.99) * 0.05, tdf[cats[1]].quantile(0.99) * 0.9,
                   "$\mathbf{r=" + str(round(r, 3)) + "^{***}}$")
        ax[i].ticklabel_format(style = "sci", axis = "y", scilimits = (0,0))
        print(r, p)
    ax[0].set_xlabel("Family (LIWC)", fontproperties = font)
    ax[1].set_xlabel("Pronoun (LIWC)", fontproperties = font)
    ax[2].set_xlabel("Preposition (LIWC)", fontproperties = font)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
