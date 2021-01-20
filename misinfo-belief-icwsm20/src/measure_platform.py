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
    data_path = os.path.join(sys_path, "data")
        
    # Reads plot data.
    for label in ["belief", "disbelief"]:
        plot_path = os.path.join(data_path, label + "_platform_plot.csv")
        df = pd.read_csv(plot_path)
        
        # Plot RQ4: platform distribution.
        plot_args = {"belief": {"c": "seagreen",
                                "xlim": [0, 0.265],
                                "xticks": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                                "xticklabels": ["0%", "5%", "10%", "15%", "20%", "25%"]},
                     "disbelief": {"c": "indianred",
                                   "xlim": [0, 0.25],
                                   "xticks": [0, 0.05, 0.1, 0.15, 0.2],
                                   "xticklabels": ["0%", "5%", "10%", "15%", "20%"]}}
        fig_path = os.path.join(sys_path, "results", label + "_platform.pdf")
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 1.2))
        for i, (site, gdf) in enumerate(df[df["before_fc"] == True].groupby("site")):
            positive_count = gdf[gdf[label] == True]["count"].values[0]
            negative_count = gdf[gdf[label] == False]["count"].values[0]
            total_count = positive_count + negative_count
            postitive_rate = positive_count / total_count
            print(site, postitive_rate)
            ax.barh(i, postitive_rate, color=plot_args[label]["c"], alpha=0.8)
            ci_low, ci_upp = pc(positive_count, total_count, alpha=0.05/3)
            ax.plot([ci_low, ci_upp], [i, i], color="k", alpha=0.8)
            ax.text(ci_upp, i, " " + str(int(round(postitive_rate * 100))) + "%",
                    ha="left", va="center", color="gray", alpha=0.8, fontproperties=font)
            ax.set_xlim(plot_args[label]["xlim"])
            ax.set_xticks(plot_args[label]["xticks"])
            ax.set_xticklabels(plot_args[label]["xticklabels"])
        ax.set_xlabel(label.capitalize() + " %", fontproperties=font2)
        ax.set_ylim([-0.6, 2.6])
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["Facebook", "Twitter", "YouTube"])
        ax.set_ylabel("Platform", fontproperties=font2)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
