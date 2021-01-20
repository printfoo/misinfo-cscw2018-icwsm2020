#!/usr/local/bin/python3

import os, sys, json, random, time, re
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, ttest_ind, ttest_rel
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

# compute
def compute():
    
    sig_clusters_f1 = open(sig_clusters_path1, "w")
    sig_clusters_f1.write("cluster_num,stat,p,mean-2,mean-1,mean0,mean1,case\n")
    sig_clusters_f2 = open(sig_clusters_path2, "w")
    sig_clusters_f2.write("cluster_num,stat,p,mean-not2,mean2,case\n")
    sig_clusters_f3 = open(sig_clusters_path3, "w")
    sig_clusters_f3.write("cluster_num,stat,p,mean-before,mean-after,case\n")
    df1 = pd.read_csv(emolex_path)
    df2 = pd.read_csv(w2v_path)
    df3 = pd.read_csv(liwc_path)
    df_tmp = df1.merge(df2, on = ["id", "ruling_val", "after_checked"]).merge(df3, on = ["id", "ruling_val", "after_checked"])
    df = df_tmp[df_tmp["after_checked"] == -1]
    checked = df_tmp[df_tmp["after_checked"] == 1]
    
    fdf = df[df["ruling_val"] < 2]
    for cluster in fdf.columns:
        if cluster in {"id", "after_checked", "ruling_val"}:
            continue
        rho, p = spearmanr(fdf["ruling_val"], fdf[cluster])
        if p < 0.05:
            print(cluster, rho, p)
            sig_clusters_f1.write(cluster + "," + str(rho) + "," + str(p) + "," \
                                  + ",".join([str(_) for _ in fdf.groupby("ruling_val").mean()[cluster].values]) + \
                                  ",falsetomosttrue\n")
    print("\n\n")

    tdf = df.copy()
    tdf["trueornot"] = tdf["ruling_val"].apply(lambda x: 1 if x == 2 else 0)
    for cluster in tdf.columns:
        if cluster in {"id", "after_checked", "ruling_val", "trueornot"}:
            continue
        t, p = ttest_ind(tdf[tdf["trueornot"] == 1][cluster], tdf[tdf["trueornot"] == 0][cluster])
        if p < 0.05:
            print(cluster, t, p)
            sig_clusters_f2.write(cluster + "," + str(t) + "," + str(p) + "," \
                                  + ",".join([str(_) for _ in tdf.groupby("trueornot").mean()[cluster].values]) + \
                                  ",trueornot\n")
    print("\n\n")
    
    df = df.merge(checked, on = ["id", "ruling_val"])
    df = df[df["999_y"] > 0]
    for cluster in fdf.columns:
        if cluster in {"id", "after_checked", "ruling_val"}:
            continue
        t, p = ttest_rel(df[cluster + "_y"], df[cluster + "_x"])
        if p < 0.05:
            print(cluster, t, p)
            sig_clusters_f3.write(cluster + "," + str(t) + "," + str(p) + "," \
                                  + ",".join([str(_) for _ in df.mean()[[cluster + "_x", cluster + "_y"]].values]) + \
                                  ",checkornot\n")
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
    df1 = pd.read_csv(sig_clusters_path1)
    df1 = df1[df1["p"] < 0.05]
    df2 = pd.read_csv(names_path)
    df2["cluster_num"] = df2["cluster_num"].astype("str")
    df = df1.merge(df2, on = "cluster_num")
    df = df.sort_values("stat")
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
    ax.scatter([-5], [-5], color = "indianred", marker = "s", label = r"$\rho<0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.6, marker = "s", label = r"$\rho<0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.2, marker = "s", label = r"$\rho<0^{*}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", marker = "s", label = r"$\rho>0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.6, marker = "s", label = r"$\rho>0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.2, marker = "s", label = r"$\rho>0^{*}$", linewidth = 0)
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
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token1"].values[0], 0.0015, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token2"].values[0], 0.0095, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token3"].values[0], 0.0175, i + 0.1)
    ax.set_xlabel(r"Spearman $\rho$", fontproperties = font2)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path1, bbox_inches = "tight", pad_inches = 0)


    # fig 2
    df1 = pd.read_csv(sig_clusters_path2)
    df1 = df1[df1["p"] < 0.05]
    df1["cluster_num"] = df1["cluster_num"].astype("str")
    df2 = pd.read_csv(names_path)
    df = df1.merge(df2, on = "cluster_num")
    df = df.sort_values("stat")
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
    ax.scatter([-5], [-5], color = "indianred", marker = "s", label = r"$t<0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.6, marker = "s", label = r"$t<0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.2, marker = "s", label = r"$t<0^{*}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", marker = "s", label = r"$t>0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.6, marker = "s", label = r"$t>0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.2, marker = "s", label = r"$t>0^{*}$", linewidth = 0)
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

    # fig 3
    df1 = pd.read_csv(sig_clusters_path3)
    df1 = df1[df1["p"] < 0.05]
    df1["cluster_num"] = df1["cluster_num"].astype("str")
    df2 = pd.read_csv(names_path)
    df = df1.merge(df2, on = "cluster_num")
    df = df.sort_values("stat")
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
    ax.scatter([-5], [-5], color = "indianred", marker = "s", label = r"$t<0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.6, marker = "s", label = r"$t<0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "indianred", alpha = 0.2, marker = "s", label = r"$t<0^{*}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", marker = "s", label = r"$t>0^{***}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.6, marker = "s", label = r"$t>0^{**}$", linewidth = 0)
    ax.scatter([-5], [-5], color = "seagreen", alpha = 0.2, marker = "s", label = r"$t>0^{*}$", linewidth = 0)
    leg = ax.legend(bbox_to_anchor=(0.5, 1.01, 0, 0), loc = "center", ncol = 6, borderaxespad = 0.)
    leg.get_frame().set_alpha(0)
    for i in range(len(df)):
        if df[df["cluster_num"] == y[i]]["stat"].values[0] < 0:
            ax.text(0.048, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "left", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "right", verticalalignment = "center", color = "#999999", fontproperties = font3)
        else:
            ax.text(-0.032, i, r"$\bf{" + df[df["cluster_num"] == y[i]]["name"].values[0] + \
                    "}$ [" + df[df["cluster_num"] == y[i]]["info"].values[0] + \
                    "] $\it{(" + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token1"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token2"].values[0]) + \
                    ", " + re.sub("^emo..", "\ \ \ \ ", df[df["cluster_num"] == y[i]]["token3"].values[0]) + ")}$",
                    horizontalalignment = "right", verticalalignment = "center")
            ax.text(df[df["cluster_num"] == y[i]]["stat"].values[0], i,
                    round(df[df["cluster_num"] == y[i]]["stat"].values[0], 3),
                    horizontalalignment = "left", verticalalignment = "center", color = "#999999", fontproperties = font3)
        if df[df["cluster_num"] == y[i]]["token1"].values[0].startswith("emo"):
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token1"].values[0], 0.73, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token2"].values[0], 0.875, i + 0.1)
            annotate_emoji1(ax, df[df["cluster_num"] == y[i]]["token3"].values[0], 1.02, i + 0.1)
    ax.set_xlabel(r"Dependent $t$", fontproperties = font2)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path3, bbox_inches = "tight", pad_inches = 0)

# main
if __name__ == "__main__":
    
    # get path
    emolex_path = os.path.join(file_path, "data", "corpus_sentiment_emolex.csv")
    w2v_path = os.path.join(file_path, "data", "corpus_sentiment_w2v_cluster.csv")
    liwc_path = os.path.join(file_path, "data", "corpus_sentiment_liwc.csv")
    sig_clusters_path1 = os.path.join(file_path, "lexicon", "w2v_cluster", "sig_clusters_falsetomosttrue.csv")
    sig_clusters_path2 = os.path.join(file_path, "lexicon", "w2v_cluster", "sig_clusters_trueornot.csv")
    sig_clusters_path3 = os.path.join(file_path, "lexicon", "w2v_cluster", "sig_clusters_checkornot.csv")
    names_path = os.path.join(file_path, "lexicon", "w2v_cluster", "cluster_names.csv")
    emoji_path = os.path.join(file_path, "resources", "emojis128")
    fig_path1 = os.path.join(file_path, "results", "sig_clusters_falsetomosttrue.pdf")
    fig_path2 = os.path.join(file_path, "results", "sig_clusters_trueornot.pdf")
    fig_path3 = os.path.join(file_path, "results", "sig_clusters_checkornot.pdf")

    compute()
    plot()
