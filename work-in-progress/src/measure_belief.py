#!/usr/local/bin/python3

import os, sys
import pandas as pd
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

if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data", "data.csv")
    df = pd.read_csv(data_path)
    rename = lambda r: r["primary category"] + " - " + r["event"]
    df["event"] = df["primary category"] + " - " + df["event"]
    df = df.sort_values("event")
        
    # Reads plot data.
    for label in ["belief", "disbelief"]:
        
        # Plot RQ1: (dis)belief distribution.
        plot_args = {"belief": {"c": "seagreen"},
                     "disbelief": {"c": "indianred"}}
        fig_path = os.path.join(sys_path, "results", label + "_distribution.pdf")
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 5))
        yticklabel = []
        ax.axhspan(-1, 6.5, alpha=0.3, color="gray")
        ax.axhspan(13.5, 21.5, alpha=0.3, color="gray")
        for i, (event, gdf) in enumerate(df.groupby("event")):
            yticklabel.append(event)
            positive_count = len(gdf[gdf[label] == 1])
            negative_count = len(gdf[gdf[label] == 0])
            total_count = positive_count + negative_count
            postitive_rate = positive_count / total_count
            print(event, postitive_rate, total_count)
            ax.barh(event, postitive_rate, color=plot_args[label]["c"], alpha=0.8)
            ci_low, ci_upp = pc(positive_count, total_count, alpha=0.05/30)
            ax.plot([ci_low, ci_upp], [i, i], color="k", alpha=0.8)

        ax.set_xlabel(label.capitalize() + " %", fontproperties=font2)
        ax.set_ylim([-1, 30])
        ax.set_yticklabels(yticklabel, ha="left", x=-1)
        ax.set_ylabel("Topic - event", fontproperties=font2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
