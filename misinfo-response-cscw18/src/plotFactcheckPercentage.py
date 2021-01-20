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
    senti_path = os.path.join(file_path, "data", "corpus_sentiment_w2v_cluster.csv")
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    fig_path = os.path.join(file_path, "results", "factchecked_percentage.pdf")

    # data
    """
    df = pd.read_csv(senti_path)
    factcheck = pd.read_csv(factcheck_path)
    df = df.merge(factcheck, left_on = "id", right_on = "social_id")
    politi = df[df["checkedby"] == "politifact"]
    print(len(politi), len(politi[politi["998"] > 0]))
    snopes = df[df["checkedby"] == "snopes"]
    print(len(snopes), len(snopes[snopes["999"] > 0]))
    """
    politi = [193, 2888 - 193]
    snopes = [107, 1732 - 107]
    explode = [0.2, 0]
    colors = ["seagreen", "indianred"]
    
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(3, 1.5))
    _, text = ax[0].pie(politi, startangle = 90, explode = explode, colors = colors, labels = [r"$\bf{politifactref}:$ 6.68%", ""], wedgeprops = {"alpha": 0.9})
    text[0].set_x(1.6)
    text[0].set_y(1.3)
    _, text = ax[1].pie(snopes, startangle = 90, explode = explode, colors = colors, labels = [r"$\bf{snopesref}:$ 6.18%", ""], wedgeprops = {"alpha": 0.9})
    text[0].set_x(1.5)
    text[0].set_y(1.3)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
