#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr, ttest_ind, ttest_rel, f_oneway, kruskal, friedmanchisquare
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.size"] = 8
font = FontProperties()
font.set_size(8)
font2 = FontProperties()
font2.set_size(8)
font2.set_weight("bold")
font3 = FontProperties()
font3.set_size(7)

# combine all tokens in each cluster
def combine_tokens(g):
    words = g.sort_values("count", ascending = False)["token"].values
    words = [str(w) for w in words]
    return pd.Series({"words": ", ".join(words)})

# main
if __name__ == "__main__":
    
    # get path
    folder_path = os.path.join(file_path, "lexicon", "ratings")
    rating_paths = []
    for rater in ["shan", "dan", "jun", "ming"]:
        rating_paths.append(os.path.join(folder_path, "rating_" + rater + ".csv"))
    fig_path = os.path.join(file_path, "results", "ratings_q1.pdf")

    # read data
    dfs = []
    for rating_path in rating_paths:
        dfs.append(pd.read_csv(rating_path))

    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(3.6, 1.5))

    # plot fig1
    handle = ax[0].violinplot([df["rating_1"] for df in dfs],
                              showmeans = True, showextrema = False, widths = 0.7)
    print([df["rating_1"].mean() for df in dfs])
    c = matplotlib.cm.get_cmap("Blues")
    for i in range(len(handle["bodies"])):
        handle["bodies"][i].set_facecolor(c(0.7))
        handle["bodies"][i].set_alpha(0.8)
    handle["cmeans"].set_color("k")
    ax[0].set_xlim([0.5, 4.5])
    ax[0].set_xticks([1, 2, 3, 4])
    ax[0].set_xticklabels(["A", "R1", "R2", "R3"])
    ax[0].set_xlabel("Rater", fontproperties = font2)
    ax[0].set_ylim([1, 5])
    ax[0].set_yticks([1, 2, 3, 4, 5])
    ax[0].set_yticklabels([r"$\bf{Not\ related}$ (1)", r"$\bf{Slightly\ related}$ (2)",
                           r"$\bf{Moderately\ related}$ (3)", r"$\bf{Very\ related}$ (4)", r"$\bf{Extremely\ related}$ (5)"])
    ax[0].set_ylabel("Rating", fontproperties = font2)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["top"].set_visible(False)

    # plot fig2
    m = np.zeros([4, 4])
    for i in range(len(["shan", "dan", "jun", "ming"])):
        for j in range(len(["shan", "dan", "jun", "ming"])):
            m[i][j], p = pearsonr(dfs[i]["rating_1"], dfs[j]["rating_1"])
            m[i][j] = round(m[i][j], 3)
            print(m[i][j], p)
    print(kruskal(dfs[0]["rating_1"], dfs[1]["rating_1"], dfs[2]["rating_1"], dfs[3]["rating_1"]))
    map = ax[1].imshow(m, cmap = "Blues", alpha = 0.8, vmin = 0, vmax = 1)
    ax[1].set_xticks([0, 1, 2, 3])
    ax[1].set_xticklabels(["A", "R1", "R2", "R3"])
    ax[1].set_xlabel("Rater", fontproperties = font2)
    ax[1].set_yticks([0, 1, 2, 3])
    ax[1].set_yticklabels(["A", "R1", "R2", "R3"])
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["top"].set_visible(False)
    cb = plt.colorbar(map, fraction = 0.05)
    cb.outline.set_linewidth(0)
    cb.set_label(r"Pearson $r$", fontproperties = font2)

    # save figs
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
