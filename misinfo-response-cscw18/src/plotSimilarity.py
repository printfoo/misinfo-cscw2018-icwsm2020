#!/usr/local/bin/python3

import os, sys, json, random, time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import cosine
from scipy.stats import spearmanr, pearsonr, ttest_ind, ttest_rel
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams.update({"font.size": 8})
font = FontProperties()
font.set_size(8)
font.set_weight("bold")
font2 = FontProperties()
font2.set_size(30)

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    emolex_path = os.path.join(file_path, "data", "corpus_sentiment_emolex.csv")
    w2v_path = os.path.join(file_path, "data", "corpus_sentiment_w2v_cluster.csv")
    fig_path = os.path.join(file_path, "results", "true_fake_similarity.pdf")

    df1 = pd.read_csv(emolex_path)
    df2 = pd.read_csv(w2v_path)
    df = df1.merge(df2, on = ["id", "ruling_val", "after_checked"])
    df = df[df["after_checked"] == -1]
    df = df.groupby("ruling_val").mean()
    df = df.drop(["after_checked"], axis = 1)
    l = [-2, -1, 0, 1, 2]
    m = np.zeros([5, 5])
    for i in range(len(l)):
        for j in range(len(l)):
            x = df[df.index == l[i]].values[0]
            y = df[df.index == l[j]].values[0]
            m[i][j] = 1 - cosine(x, y)
    n = np.zeros([5, 5])
    for i in range(len(l)):
        for j in range(len(l)):
            x = df[df.index == l[i]].values[0]
            y = df[df.index == l[j]].values[0]
            n[i][j], p = pearsonr(x, y)

    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(6, 1.5))
    map1 = ax[0].imshow(m, cmap = "gray", alpha = 0.8)
    map2 = ax[1].imshow(n, cmap = "gray", alpha = 0.8)
    for i in range(2):
        ax[i].set_xlim([-0.5, 4.5])
        ax[i].set_xticks([])
        ax[i].set_yticks([0, 1, 2, 3, 4])
        ax[i].spines["right"].set_visible(False)
        ax[i].spines["top"].set_visible(False)
    ax[0].set_yticklabels([r"$\bf{False}$ (-2)", r"$\bf{Mostly\ false}$ (-1)",
                        r"$\bf{Half\ half}$ ( 0)", r"$\bf{Mostly\ true}$ ( 1)", r"$\bf{True}$ ( 2)"])
    ax[1].set_yticklabels(["(-2)", "(-1)", "( 0)", "( 1)", "( 2)"])
    trans = ax[0].get_xaxis_transform()
    ax[0].annotate("Misinformation", xy=(-5.8, 0.55), xycoords=trans, ha = "right",
                fontproperties = font)
    ax[0].annotate("Information", xy=(-5.8, 0.07), xycoords=trans, ha = "right",
                fontproperties = font)
    ax[0].plot([-5.5, -5.5], [0.25, 0.95], color="k", transform = trans, clip_on = False)
    ax[0].plot([-5.5, -5.5], [0.04, 0.16], color="k", transform = trans, clip_on = False)
    cb1 = fig.colorbar(map1, ax = ax[0], fraction = 0.05)
    cb1.outline.set_linewidth(0)
    cb1.set_label("Cosine similarity", fontproperties = font)
    cb2 = fig.colorbar(map2, ax = ax[1], fraction = 0.05)
    cb2.outline.set_linewidth(0)
    cb2.set_label(r"Pearson $r$", fontproperties = font)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
