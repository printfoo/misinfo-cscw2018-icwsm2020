#!/usr/local/bin/python3

import os, sys
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.proportion import proportion_confint as pc
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

def get_start(g):
    return g["delta"].min()

if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
        
    # Reads plot data.
    for label in ["belief", "disbelief"]:
        plot_path = os.path.join(data_path, label + "_factcheck_plot.csv")
        df = pd.read_csv(plot_path)
        df = df[df["verdict"] == -1]
        start = df.groupby("social_id").apply(get_start).to_frame(name="start").dropna()
        df = df.merge(start, on="social_id")
        print(df)
        df["delta"] = df["delta"] - df["start"]
        df["i"] = 1 - df["before_fc"]
        X = df[["delta", "i"]]
        X = sm.add_constant(X)
        y = df[label]
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        continue
        
        # Plot RQ1: (dis)belief distribution.
        plot_args = {"belief": {"c": "seagreen",
                                "xlim": [0, 0.295],
                                "xticks": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                                "xticklabels": ["0%", "5%", "10%", "15%", "20%", "25%"]},
                     "disbelief": {"c": "indianred",
                                   "xlim": [0, 0.215],
                                   "xticks": [0, 0.05, 0.1, 0.15, 0.2],
                                   "xticklabels": ["0%", "5%", "10%", "15%", "20%"]}}
        fig_path = os.path.join(sys_path, "results", label + "_distribution.pdf")
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 1.2))
        for verdict, gdf in df[df["before_fc"] == True].groupby("verdict"):
            positive_count = gdf[gdf[label] == True]["count"].values[0]
            negative_count = gdf[gdf[label] == False]["count"].values[0]
            total_count = positive_count + negative_count
            postitive_rate = positive_count / total_count
            ax.barh(verdict, postitive_rate, color=plot_args[label]["c"], alpha=0.8)
            ci_low, ci_upp = pc(positive_count, total_count, alpha=0.05/3)
            ax.plot([ci_low, ci_upp], [verdict, verdict], color="k", alpha=0.8)
            ax.text(postitive_rate, verdict, "  " + str(int(round(postitive_rate * 100))) + "%",
                    ha="left", va="center", color="gray", alpha=0.8, fontproperties=font)
            ax.set_xlim(plot_args[label]["xlim"])
            ax.set_xticks(plot_args[label]["xticks"])
            ax.set_xticklabels(plot_args[label]["xticklabels"])
        ax.set_xlabel(label.capitalize() + " %", fontproperties=font2)
        ax.set_ylim([-1.6, 1.6])
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(["False", "Mixed", "True"])
        ax.set_ylabel("(Mis)info. type", fontproperties=font2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    
        # Plot RQ2: role of fact-checking on false stories.
        plot_args = {"belief": {"c": "seagreen",
                                "xlim": [0, 0.27],
                                "xticks": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                                "xticklabels": ["0%", "5%", "10%", "15%", "20%", "25%"]},
                     "disbelief": {"c": "indianred",
                                   "xlim": [0, 0.27],
                                   "xticks": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                                   "xticklabels": ["0%", "5%", "10%", "15%", "20%", "25%"]}}
        fig_path = os.path.join(sys_path, "results", label + "_factcheck.pdf")
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 0.8))
        for before_fc, gdf in df[df["verdict"] == -1].groupby("before_fc"):
            positive_count = gdf[gdf[label] == True]["count"].values[0]
            negative_count = gdf[gdf[label] == False]["count"].values[0]
            total_count = positive_count + negative_count
            postitive_rate = positive_count / total_count
            ax.barh(before_fc, postitive_rate, color=plot_args[label]["c"], alpha=0.8)
            ci_low, ci_upp = pc(positive_count, total_count, alpha=0.05/3)
            ax.plot([ci_low, ci_upp], [before_fc, before_fc], color="k", alpha=0.8)
            ax.text(postitive_rate, before_fc, "  " + str(int(round(postitive_rate * 100))) + "%",
                    ha="left", va="center", color="gray", alpha=0.8, fontproperties=font)
            ax.set_xlim(plot_args[label]["xlim"])
            ax.set_xticks(plot_args[label]["xticks"])
            ax.set_xticklabels(plot_args[label]["xticklabels"])
        ax.set_xlabel(label.capitalize() + " %", fontproperties=font2)
        ax.set_ylim([-0.6, 1.6])
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["After", "Before"])
        ax.set_ylabel("Fact-check", fontproperties=font2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
