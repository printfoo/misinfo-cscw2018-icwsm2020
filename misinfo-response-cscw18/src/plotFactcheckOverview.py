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
    fig_path = os.path.join(file_path, "results", "factchecked_num.pdf")

    # data
    politi_index = [-2.75, -2, -1, 0, 1, 2]
    politi = [444, 732, 645, 625, 501, 369]
    snopes_index = [-2, -1, 0, 1, 2]
    snopes = [1564, 317, 400, 63, 268]
    
    fig = plt.subplots(figsize=(5, 1.5))
    gs = GridSpec(1, 11)
    ax = [None for i in range(2)]
    ax[0] = plt.subplot(gs[0, :4])
    ax[1] = plt.subplot(gs[0, 7:])

    # fig 1
    bars = ax[0].barh(politi_index, politi, linewidth = 0)
    bars[0].set_color("indianred")
    bars[1].set_color("indianred")
    bars[2].set_color("indianred")
    bars[2].set_alpha(0.6)
    bars[3].set_color("gray")
    bars[3].set_alpha(0.6)
    bars[4].set_color("seagreen")
    bars[4].set_alpha(0.6)
    bars[5].set_color("seagreen")
    for i in range(len(bars)):
        ax[0].text(politi[i] + 8, politi_index[i], politi[i], horizontalalignment = "left",
                verticalalignment = "center", color = "#999999", fontproperties = font2)
    ax[0].set_yticks([-2.7, -2, -1, 0, 1, 2])
    ax[0].set_yticklabels([r"$\bf{Pants\ on\ fire!}$ (-2)", r"$\bf{False}$ (-2)", r"$\bf{Mostly\ false}$ (-1)",
                           r"$\bf{Half\ true}$ ( 0)", r"$\bf{Mostly\ true}$ ( 1)", r"$\bf{True}$ ( 2)"])
    ax[0].set_xlim([0, 850])
    ax[0].set_xlabel("PolitiFact", fontproperties = font)
    ax[0].spines["right"].set_visible(False)
    ax[0].spines["top"].set_visible(False)

    # fig 2
    bars = ax[1].barh(snopes_index, snopes, linewidth = 0)
    bars[0].set_color("indianred")
    bars[1].set_color("indianred")
    bars[1].set_alpha(0.6)
    bars[2].set_color("gray")
    bars[2].set_alpha(0.6)
    bars[3].set_color("seagreen")
    bars[3].set_alpha(0.6)
    bars[4].set_color("seagreen")
    for i in range(len(bars)):
        ax[1].text(snopes[i] + 10, snopes_index[i], snopes[i], horizontalalignment = "left",
                verticalalignment = "center", color = "#999999", fontproperties = font2)
    ax[1].set_yticks([-2, -1, 0, 1, 2])
    ax[1].set_yticklabels([r"$\bf{False}$ (-2)", r"$\bf{Mostly\ false}$ (-1)",
                               r"$\bf{Mixture}$ ( 0)", r"$\bf{Mostly\ true}$ ( 1)", r"$\bf{True}$ ( 2)"])
    ax[1].set_xlim([0, 1900])
    ax[1].set_xlabel("Snopes", fontproperties = font)
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["top"].set_visible(False)

    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
