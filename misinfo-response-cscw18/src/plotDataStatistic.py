#!/usr/local/bin/python3

import os, sys, json, time, datetime, math
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr
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
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    corpus_path = os.path.join(file_path, "data", "corpus_token.csv")
    fig_path1 = os.path.join(file_path, "results", "double_checked.pdf")
    fig_path2 = os.path.join(file_path, "results", "delete_distribution.pdf")

    # fig 1
    df = pd.read_csv(factcheck_path)
    dup_dict = {}
    p_list = []
    s_list = []
    for id, tdf in df.groupby("social_id"):
        if len(tdf) > 1 and "snopes" in tdf["checkedby"].values and "politifact" in tdf["checkedby"].values:
            s = tdf[tdf["checkedby"] == "snopes"]["ruling_val"].values[0]
            p = tdf[tdf["checkedby"] == "politifact"]["ruling_val"].values[0]
            if (not math.isnan(s)) and (not math.isnan(p)):
                s_list.append(s)
                p_list.append(p)
                if str(s)+str(p) not in dup_dict:
                    dup_dict[str(s)+str(p)] = {"x": s, "y": p, "s": 1}
                else:
                    dup_dict[str(s)+str(p)]["s"] += 1
    print(spearmanr(s_list, p_list))
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(1.5, 1.5))
    for key in dup_dict:
        color = dup_dict[key]["x"] + dup_dict[key]["y"]
        if color < 0:
            c = "indianred"
        elif color > 0:
            c = "seagreen"
        else:
            c = "gray"
        alpha = dup_dict[key]["x"] * dup_dict[key]["y"]
        if alpha > 0:
            a = 1
        elif alpha == 0:
            a = 0.6
        else:
            a = 0.2
        ax.scatter(dup_dict[key]["x"], dup_dict[key]["y"], s = dup_dict[key]["s"] * 60,
                   c = c, alpha = a, linewidth = 0)
        ax.text(dup_dict[key]["x"], dup_dict[key]["y"], str(dup_dict[key]["s"]), ha = "center", va = "center", fontproperties = font2)
    ax.set_xlim([-3.8, 2.5])
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_xlabel("Snopes", fontproperties = font)
    ax.set_ylim([-3.8, 2.5])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_ylabel("PolitiFact", fontproperties = font)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path1, bbox_inches = "tight", pad_inches = 0)

    # fig 2
    df1 = pd.read_csv(corpus_path)
    df1 = df1[df1["type"] == "exceptional"]
    df1 = df1[df1["tokens"] != "nocomments"]
    df1 = df1[df1["tokens"] != "commentsdisabled"]
    df1 = df1[df1["tokens"] != "unknown"]
    df1 = df1.merge(df, left_on = "id", right_on = "social_id")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(1.8, 1.5))
    count = df1.groupby("ruling_val").count()
    bars = ax.barh(count.index, count["id"], linewidth = 0)
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_xlim([0, 570])
    bars[0].set_color("indianred")
    bars[1].set_color("indianred")
    bars[1].set_alpha(0.6)
    bars[2].set_color("gray")
    bars[2].set_alpha(0.6)
    bars[3].set_color("seagreen")
    bars[3].set_alpha(0.6)
    bars[4].set_color("seagreen")
    for i in range(len(count)):
        ax.text(count["id"].values[i] + 4, i-2, count["id"].values[i], horizontalalignment = "left",
                verticalalignment = "center", color = "#999999", fontproperties = font2)
    ax.set_xlabel("Deleted Number", fontproperties = font)
    ax.set_ylabel("Veracity", fontproperties = font)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path2, bbox_inches = "tight", pad_inches = 0)

    """
    df1 = pd.read_csv(corpus_path)
    df1 = df1[df1["tokens"] != "unknown"]
    df1["moderated"] = df1.apply(lambda r: 1 if r["type"] == "exceptional" and r["tokens"] != "nocomments" \
                                 and r["tokens"] != "commentsdisabled" and r["tokens"] != "unknown" else 0, axis = 1)
    df = df1.merge(df, left_on = "id", right_on = "social_id")
    df = df.groupby(["id", "ruling_val"]).sum()
    df.to_csv(os.path.join(file_path, "data", "get_deletion_corr.csv"))
    df = pd.read_csv(os.path.join(file_path, "data", "get_deletion_corr.csv"))
    df["moderated"] = df["moderated"].apply(lambda x: 0 if x == 0 else 1)
    print(pearsonr(df["moderated"], df["ruling_val"]))
    """
