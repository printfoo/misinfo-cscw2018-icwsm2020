#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
"""
sys_path = sys.path[0]
sep = sys_path.find("src")
file_path = sys_path[0:sep]
"""
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
"""

# compute
def compute():
    
    sig_clusters_f1 = open(sig_clusters_hotel_path, "w")
    sig_clusters_f1.write("cluster_num,stat,p,mean-fake,mean-true\n")
    sig_clusters_f2 = open(sig_clusters_movie_path, "w")
    sig_clusters_f2.write("cluster_num,stat,p,mean-pos,mean-neg\n")

    tdf = pd.read_csv(hotel_path)
    for cluster in tdf.columns:
        if cluster in {"pos_neg", "true_fake"}:
            continue
        t, p = ttest_ind(tdf[tdf["true_fake"] == "true"][cluster], tdf[tdf["true_fake"] == "fake"][cluster])
        if p < 0.05:
            print(cluster, t, p)
            mean_fake = tdf.groupby("true_fake").mean()[cluster].sort_index().values[0]
            mean_true = tdf.groupby("true_fake").mean()[cluster].sort_index().values[1]
            sig_clusters_f1.write(cluster + "," + str(t) + "," + str(p) + "," + str(mean_fake) + "," + str(mean_true) + "\n")
    print("\n\n")

    tdf = pd.read_csv(movie_path)
    for cluster in tdf.columns:
        if cluster in {"pos_neg", "true_fake"}:
            continue
        t, p = ttest_ind(tdf[tdf["pos_neg"] == "pos"][cluster], tdf[tdf["pos_neg"] == "neg"][cluster])
        if p < 0.05:
            print(cluster, t, p)
            mean_pos = tdf.groupby("pos_neg").mean()[cluster].sort_index().values[1]
            mean_neg = tdf.groupby("pos_neg").mean()[cluster].sort_index().values[0]
            sig_clusters_f2.write(cluster + "," + str(t) + "," + str(p) + "," + str(mean_pos) + "," + str(mean_neg) + "\n")
    print("\n\n")

# annotate emoji for fig 1
def annotate_emoji1(ax, name, x_add, y):
    move = {"emoA": 0.037, "emoF": 0.0365, "emoG": 0.0405, "emoH": 0.0375, "emoQ": 0.0366, "emoS": 0.0325, "emoU": 0.0415}
    x = move[name[:-1]]
    emoji = plt.imread(os.path.join(emoji_path, name + ".png"), format = "png")
    imagebox = OffsetImage(emoji, zoom = 0.08)
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox, (x + x_add, y), frameon = False, pad = 0.1)
    ax.add_artist(ab)

# annotate emoji for fig 3
def annotate_emoji3(ax, name, x_add, y):
    move = {"emoQ": 0.75}
    x = move[name[:-1]]
    emoji = plt.imread(os.path.join(emoji_path, name + ".png"), format = "png")
    imagebox = OffsetImage(emoji, zoom = 0.08)
    imagebox.image.axes = ax
    ab = AnnotationBbox(imagebox, (x + x_add, y), frameon = False, pad = 0.1)
    ax.add_artist(ab)

# plot
def plot():

    # fig 1
    df1 = pd.read_csv(sig_clusters_hotel_path)
    df2 = pd.read_csv(names_path)
    df1["cluster_num"] = df1["cluster_num"].astype("str")
    df = df1.merge(df2, on = "cluster_num")
    df = df.sort_values("stat")
    print(df)
    """
    exit()
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(9.5, len(df) * 0.2))
    y = df["cluster_num"].values
    df1 = df[df["stat"] < 0]
    y1 = df1["cluster_num"].values
    p = df1["p"].values
    bars = ax.barh(y1, df1["stat"], color = "indianred", linewidth = 0)
    for i, bar in enumerate(bars):
        if df[i:i+1]["p"].values[0] > 0.001 and df[i:i+1]["p"].values[0] <= 0.01:
            bar.set_alpha(0.6)
        elif df[i:i+1]["p"].values[0] > 0.01:
            bar.set_alpha(0.2)
    df2 = df[df["stat"] > 0]
    y2 = df2["cluster_num"].values
    bars = ax.barh(y2, df2["stat"], color = "seagreen", linewidth = 0)
    for j, bar in enumerate(bars):
        i = j + len(df1)
        if df[i:i+1]["p"].values[0] > 0.001 and df[i:i+1]["p"].values[0] <= 0.01:
            bar.set_alpha(0.6)
        elif df[i:i+1]["p"].values[0] > 0.01:
            bar.set_alpha(0.2)
    ax.set_xlim([df["stat"].min(), df["stat"].max()])
    ax.set_ylim([-1,len(df)])
    ax.set_yticks([])
    ax.scatter([-5], [-5], color = "seagreen", marker = "s", label = r"$\rho>0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.6, marker = "s", label = r"$\rho>0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.2, marker = "s", label = r"$\rho>0^{*}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", marker = "s", label = r"$\rho<0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.6, marker = "s", label = r"$\rho<0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.2, marker = "s", label = r"$\rho<0^{*}$", linewidth = 0)
    leg = ax.legend(bbox_to_anchor=(0.5, 1.01, 0, 0), loc = "center", ncol = 6, borderaxespad = 0.)
    leg.get_frame().set_alpha(0)
    for i in range(len(df)):
        if df[df["cluster_num"] == y[i]]["stat"].values[0] < 0:
            ax.text(0.003, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "left", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "right", verticalalignment = "center", color = "#999999", fontproperties = font3)
        else:
            ax.text(-0.002, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "right", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "left", verticalalignment = "center", color = "#999999", fontproperties = font3)
        if df[df["cluster_num"] == y[i]]["token1"].values[0].startswith("emo"):
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token1"].values[0], 0, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token2"].values[0], 0.008, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token3"].values[0], 0.016, i + 0.1)
    ax.set_xlabel(r"Spearman $\rho$", fontproperties = font2)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path1, bbox_inches = "tight", pad_inches = 0)
    """


    # fig 2
    df1 = pd.read_csv(sig_clusters_movie_path)
    df2 = pd.read_csv(names_path)
    df1["cluster_num"] = df1["cluster_num"].astype("str")
    df = df1.merge(df2, on = "cluster_num")
    df = df.sort_values("stat")
    #print(df)
    """
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(9.5, len(df) * 0.2))
    y = df["cluster_num"].values
    df1 = df[df["stat"] < 0]
    y1 = df1["cluster_num"].values
    p = df1["p"].values
    bars = ax.barh(y1, df1["stat"], color = "indianred", linewidth = 0)
    for i, bar in enumerate(bars):
        if df[i:i+1]["p"].values[0] > 0.001 and df[i:i+1]["p"].values[0] <= 0.01:
            bar.set_alpha(0.6)
        elif df[i:i+1]["p"].values[0] > 0.01:
            bar.set_alpha(0.2)
    df2 = df[df["stat"] > 0]
    y2 = df2["cluster_num"].values
    bars = ax.barh(y2, df2["stat"], color = "seagreen", linewidth = 0)
    for j, bar in enumerate(bars):
        i = j + len(df1)
        if df[i:i+1]["p"].values[0] > 0.001 and df[i:i+1]["p"].values[0] <= 0.01:
            bar.set_alpha(0.6)
        elif df[i:i+1]["p"].values[0] > 0.01:
            bar.set_alpha(0.2)
    ax.set_xlim([df["stat"].min(), df["stat"].max()])
    ax.set_ylim([-1,len(df)])
    ax.set_yticks([])
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.6, marker = "s", label = r"$t>0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.2, marker = "s", label = r"$t>0^{*}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.6, marker = "s", label = r"$t<0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.2, marker = "s", label = r"$t<0^{*}$", linewidth = 0)
    leg = ax.legend(bbox_to_anchor=(0.5, 1.01, 0, 0), loc = "center", ncol = 6, borderaxespad = 0.)
    leg.get_frame().set_alpha(0)
    for i in range(len(df)):
        if df[df["cluster_num"] == y[i]]["stat"].values[0] < 0:
            ax.text(0.057, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "left", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "right", verticalalignment = "center", color = "#999999", fontproperties = font3)
        else:
            ax.text(-0.038, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "right", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "left", verticalalignment = "center", color = "#999999", fontproperties = font3)
    ax.set_xlabel(r"Independent $t$", fontproperties = font2)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path2, bbox_inches = "tight", pad_inches = 0)
    """

# main
if __name__ == "__main__":
    
    # get path
    hotel_path = os.path.join(file_path, "data", "review_hotels_sentiment_w2v_cluster.csv")
    movie_path = os.path.join(file_path, "data", "review_movies_sentiment_w2v_cluster.csv")
    sig_clusters_hotel_path = os.path.join(file_path, "lexicon", "w2v_cluster", "sig_clusters_hotel.csv")
    sig_clusters_movie_path = os.path.join(file_path, "lexicon", "w2v_cluster", "sig_clusters_movie.csv")
    names_path = os.path.join(file_path, "lexicon", "w2v_cluster", "cluster_names.csv")
    #emoji_path = os.path.join(file_path, "resources", "emojis128")
    hotel_fig_path = os.path.join(file_path, "results", "sig_clusters_hotel.pdf")
    movie_fig_path = os.path.join(file_path, "results", "sig_clusters_movie.pdf")

    #compute()
    plot()
