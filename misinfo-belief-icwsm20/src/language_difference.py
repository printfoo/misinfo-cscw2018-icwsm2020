#!/usr/local/bin/python3

import os, sys
import random
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
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

def plot(plot_df, label):
    print(label)
    config = {"disbelief": {"c": "indianred"}, "belief": {"c": "seagreen"}}
    fig_path = os.path.join(sys_path, "results", "language_difference_" + label + ".pdf")
    print(plot_df)
    x = plot_df["t"]
    y = [i for i in range(len(plot_df))]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(6.5, 0.25 * len(plot_df)))
    bars = ax.barh(y, x, color=config[label]["c"], alpha=0.8, linewidth=0)
    for i in y:
        if "|" in plot_df["leg"].values[i]:
            lex = "ComLex"
            leg = r"$\bf{" + plot_df["leg"].values[i].replace("|", r"}$, $\bf{") + "}$, ... (" + lex + ")"
        else:
            lex = "LIWC"
            leg = r"$\bf{" + plot_df["leg"].values[i] + "}$ (" + lex + ")"
        if plot_df["t"].values[i] > 0:
            ax.text(-0.3, i, leg, ha = "right", va = "center")
        else:
            ax.text(0.3, i, leg, ha = "left", va = "center")
    ax.set_xlim([-16, 16])
    ax.set_xticks([-15, -10, -5, 0, 5, 10, 15])
    ax.set_xticklabels([-15, -10, -5, 0, 5, 10, 15])
    ax.set_xlabel(r" less in " + label + "   $\longleftarrow t \longrightarrow$   more in " + label, fontproperties = font2)
    ax.set_yticks([])
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    
    # LIWC.
    train_path = os.path.join(data_path, "train_liwc.csv")
    test_path = os.path.join(data_path, "test_liwc.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    liwc_df = pd.concat([train_df, test_df])
    
    # ComLex.
    train_path = os.path.join(data_path, "train_comlex.csv")
    test_path = os.path.join(data_path, "test_comlex.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    comlex_df = pd.concat([train_df, test_df])
    
    # Combines.
    df = pd.concat([liwc_df, comlex_df[comlex_df.columns[3:]]], axis=1)
    cats = list(df.columns[3:])
    print(len(cats), len(comlex_df.columns[3:]))
    df["belief"] = df["labels"].apply(lambda l: eval(l)[0]).values
    df["disbelief"] = df["labels"].apply(lambda l: eval(l)[1]).values
    #print(df.mean())

    # Hypothesis tests.
    labels = {
        "disbelief": {
            "col": ["negate", "posemo", "negemo", "anger", "discrep", "fact|research",
                    "fake|false", "lie|propaganda", "liar|crook", "stupid|dumb"],
            "leg": ["negation", "positive~emotion", "negative~emotion", "anger", "discrepancy", "fact|research|report",
                    "fake|false|bias", "lie|propaganda|corruption", "liar|crook|thief", "stupid|dumb|ignorant"],
            "t": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        "belief": {
            "col": ["anger", "swear", "Exclam", "discrep", "fake|false", "republican|democrat",
                    "stupid|dumb", "bye|maga", "call|support", "people|american"],
            "leg": ["anger", "swear", "exclamation", "discrepancy", "fake|false|bias", "republican|democrat|gop",
                    "stupid|dumb|ignorant", "!|yay|bye", "call|support|defend", "people|american|man"],
            "t": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
    }
    for label in labels:
        for cat in cats:
            for i, col in enumerate(labels[label]["col"]):
                if col in cat:
                    pos = df[df[label] == 1][cat]
                    neg = df[df[label] == 0][cat]
                    t, p = ttest_ind(pos, neg)
                    if p < 0.01 / len(cats):
                        print(cat, p / len(cats), t)
                        labels[label]["t"][i] = t
    
    # Plots.
    for label in labels:
        df = pd.DataFrame(data=labels[label])
        df = df.sort_values("t")
        plot(df, label)
