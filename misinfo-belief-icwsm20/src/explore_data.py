#!/usr/local/bin/python3

import os, sys
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
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

def get_int(x):
    try:
        return int(x)
    except:
        return 0
        
def agreement(y1, y2):
    agree = [1 if _y1 == _y2 else 0 for _y1, _y2 in zip(y1, y2)]
    return sum(agree) / len(agree)

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    raw_path = os.path.join(data_path, "annotations")

    # Cleans annotated data.
    d = {"topic": [], "disbelief": [], "belief": [], "disbelief_%": [], "belief_%": []}
    for _, _, file_names in os.walk(raw_path):
        for file_name in file_names:
            d["topic"].append(file_name.split(", ")[-1].replace(".xlsx", ""))
            file_path = os.path.join(raw_path, file_name)
            df = pd.read_excel(file_path, skiprows=1)
            df = df.dropna(subset={"Unnamed: 2"})
            for c in df.columns:
                df[c] = df[c].apply(get_int)
            c1 = "seems like person DOES NOT believe this tweet"
            disbelief_r1 = df[c1].values
            c2 = df.columns[list(df.columns).index(c1) + 1]
            disbelief_r2 = df[c2].values
            c3 = "seems like person DOES believe this tweet"
            belief_r1 = df[c3].values
            c4 = df.columns[list(df.columns).index(c3) + 1]
            belief_r2 = df[c4].values
            d["disbelief"].append(agreement(disbelief_r1, disbelief_r2))
            d["belief"].append(agreement(belief_r1, belief_r2))
            d["disbelief_%"].append(df["DOES NOT"].mean())
            d["belief_%"].append(df["DOES"].mean())
    df = pd.DataFrame(data=d)
    df = df.sort_values("topic").reset_index()
    
    """
    for agr in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]:
        p = len(df[df["disbelief"] > agr]) + len(df[df["belief"] > agr])
        print(p, 0.5 * p / len(df))
    """
    
    # Plots (dis)belief by claim.
    plot_args = {"belief": {"c": "seagreen"},
                 "disbelief": {"c": "indianred"}}
    for key in plot_args:
        print(key, df[key + "_%"].min(), df[key + "_%"].max(), df[key + "_%"].var())
        fig_path = os.path.join(sys_path, "results", key + "_by_claim_raw.pdf")
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.5, 1.5))
        ax.grid(axis="y", color="gray", alpha=0.2, linewidth=1)
        ax.bar(df.index, df[key + "_%"], color=plot_args[key]["c"], alpha=0.8, lw=0)
        ax.set_ylim([0, 1.1])
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
        ax.set_ylabel(key.capitalize() + " %", fontproperties=font2)
        ax.set_xlim([-1, len(df["topic"])])
        ax.set_xticks([i for i in range(len(df["topic"]))])
        ax.set_xticklabels(df["topic"], rotation=45, ha="right", fontproperties=font2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        #leg = ax.legend(bbox_to_anchor=(0.5, -0.8, 0, 0), loc="upper center", ncol=2, borderaxespad=0.)
        #leg.get_frame().set_alpha(0)
        plt.savefig(fig_path, bbox_inches="tight", pad_inches=0)
    print(pearsonr(df["belief_%"], df["disbelief_%"]))
    
    # Plots agreement by claim.
    fig_path = os.path.join(sys_path, "results", "interrater_agreement.pdf")
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6.5, 1.5))
    ax.grid(axis="y", color="gray", alpha=0.2, linewidth=1)
    ax.scatter(df.index, df["disbelief"], color="indianred",
               label="Disbelief", alpha=0.9, lw=0, s=50, marker="v")
    ax.scatter(df.index, df["belief"], color="seagreen",
               label="Belief", alpha=0.9, lw=0, s=50, marker="^")
    
    ax.set_ylim([0, 1.1])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_ylabel("Agreement", fontproperties=font2)
    ax.set_xlim([-1, len(df["topic"])])
    ax.set_xticks([i for i in range(len(df["topic"]))])
    ax.set_xticklabels(df["topic"], rotation=45, ha="right", fontproperties=font2)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    leg = ax.legend(bbox_to_anchor=(0.5, -0.8, 0, 0), loc="upper center", ncol=2, borderaxespad=0.)
    leg.get_frame().set_alpha(0)
    plt.savefig(fig_path, bbox_inches="tight", pad_inches=0)
