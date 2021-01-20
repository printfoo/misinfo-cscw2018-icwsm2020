#!/usr/local/bin/python3

import os, sys
import pandas as pd
from sklearn.metrics import roc_auc_score, precision_recall_curve, f1_score, accuracy_score
from scipy.stats import chi2_contingency
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

def threshold(label, model):
    print(label, model)

    # Chooses a balancing threshold from train set to make classifier consistent with annotators.
    train_path = os.path.join(data_path, "train_" + model + "_pred.csv")
    train_df = pd.read_csv(train_path)
    label_true = [eval(l)[labels[label]] for l in train_df["labels"].values]
    #print("Training sample:\t", len(label_true))
    #print("Labeled as 1:\t\t", sum(label_true), sum(label_true)/len(label_true))
    label_score = [eval(l)[labels[label]] for l in train_df["predictions"].values]
    label_score.sort(reverse=True)
    threshold = label_score[sum(label_true)]
    assert sum([l > threshold for l in label_score]) == sum(label_true)
    print("Chosen threshold:\t", round(threshold, 3))

    # Tests this on test set to see if it is consistent.
    test_path = os.path.join(data_path, "test_" + model + "_pred.csv")
    test_df = pd.read_csv(test_path)
    label_true = [eval(l)[labels[label]] for l in test_df["labels"].values]
    #print("Testing sample:\t\t", len(label_true))
    #print("Labeled as 1:\t\t", sum(label_true), sum(label_true)/len(label_true))
    label_score = [eval(l)[labels[label]] for l in test_df["predictions"].values]
    label_predict = [1 if l > threshold else 0 for l in label_score]
    #print("Predicted as 1:\t\t", sum(label_predict), sum(label_predict)/len(label_predict))
    fp = [t == 0 and p == 1 for t, p in zip(label_true, label_predict)]
    fn = [t == 1 and p == 0 for t, p in zip(label_true, label_predict)]
    contingency = [[sum(fp),
                    len(fp) - sum(fp)],
                   [sum(fn),
                    len(fn) - sum(fn)]]
    chi2, p, dof, ex = chi2_contingency(contingency, correction=False)
    print("Consistent?\t\t", p > 0.01 / 6, p)
    
    return threshold


def evaluate(model):
    path = os.path.join(data_path, "test_" + model + "_pred.csv")
    df = pd.read_csv(path)

    belief = {}
    belief_true = [eval(l)[0] for l in df["labels"].values]
    belief_score = [eval(l)[0] for l in df["predictions"].values]
    belief_predict = [1 if l > thresholds["belief"][model] else 0 for l in belief_score]
    print("\nBelief")
    for average in ["binary", "macro", "micro"]:
        print(model, average + " F1:", round(f1_score(belief_true, belief_predict, average=average), 3))
    belief["precision"], belief["recall"], belief["threshold"] = precision_recall_curve(belief_true, belief_score)
    belief["precision"] = [0] + list(belief["precision"]) + [1]
    belief["recall"] = [1] + list(belief["recall"]) + [0]

    disbelief = {}
    disbelief_true = [eval(l)[1] for l in df["labels"].values]
    disbelief_score = [eval(l)[1] for l in df["predictions"].values]
    disbelief_predict = [1 if l > thresholds["disbelief"][model] else 0 for l in disbelief_score]
    print("\nDisbelief")
    for average in ["binary", "macro", "micro"]:
        print(model, average + " F1:", round(f1_score(disbelief_true, disbelief_predict, average=average), 3))
    disbelief["precision"], disbelief["recall"], disbelief["threshold"] = precision_recall_curve(disbelief_true, disbelief_score)
    disbelief["precision"] = [0] + list(disbelief["precision"]) + [1]
    disbelief["recall"] = [1] + list(disbelief["recall"]) + [0]
    
    return belief, disbelief


if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    
    labels = {"belief": 0, "disbelief": 1}
    models = ["Chance", "LIWC+LR", "ComLex+LR", "BERT", "XLNet", "RoBERTa"]
    
    # Finds threshold.
    thresholds = {label: {model.lower(): 0 for model in models} for label in labels}
    for label in labels:
        for model in models:
            thresholds[label][model.lower()] = threshold(label, model.lower())
    
    # Evaluates models.
    prc = {model: {} for model in models}
    for model in models:
        prc[model]["belief"], prc[model]["disbelief"] = evaluate(model.lower())
            
    # Plots.
    plot_args = {"belief": {"Chance": {"c": "k", "ls": "-"},
                            "LIWC+LR": {"c": "#AAAAAA", "ls": ":"},
                            "ComLex+LR": {"c": "#AAAAAA", "ls": "-"},
                            "XLNet": {"c": "seagreen", "ls": "--"},
                            "BERT": {"c": "seagreen", "ls": ":"},
                            "RoBERTa": {"c": "seagreen", "ls": "-"}},
                 "disbelief": {"Chance": {"c": "k", "ls": "-"},
                               "LIWC+LR": {"c": "#AAAAAA", "ls": ":"},
                               "ComLex+LR": {"c": "#AAAAAA", "ls": "-"},
                               "XLNet": {"c": "indianred", "ls": "--"},
                               "BERT": {"c": "indianred", "ls": ":"},
                               "RoBERTa": {"c": "indianred", "ls": "-"}}}

    for split in ["test"]:
        for label in ["belief", "disbelief"]:
            fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 3))
           
            # Plots F1 isoheights.
            f_scores = np.linspace(0.2, 0.8, num=4)
            x_locs = [0.16, 0.35, 0.54, 0.73]
            y_locs = [0.295, 0.495, 0.695, 0.895]
            lines = []
            labels = []
            for x_loc, y_loc, f_score in zip(x_locs, y_locs, f_scores):
                x = np.linspace(0.01, 1)
                y = f_score * x / (2 * x - f_score)
                l, = ax.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2, linewidth=1)
                ax.annotate("F$_1$={:0.1f}".format(f_score), xy=(x_loc, y_loc), alpha=0.3, fontproperties=font)

            # Plots model precision recall curves.
            for model in models:
                ax.plot(prc[model][label]["recall"], prc[model][label]["precision"],
                        label=model, alpha=0.8, color=plot_args[label][model]["c"],
                        linestyle=plot_args[label][model]["ls"])

            # Other specifications.
            ax.set_xlim([0, 1.005])
            ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
            ax.set_xlabel("Recall", fontproperties=font2)
            ax.set_ylim([0, 1.005])
            ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
            ax.set_ylabel("Precision", fontproperties=font2)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            leg = ax.legend(bbox_to_anchor=(0.5, -0.18, 0, 0), loc="upper center", ncol=2, borderaxespad=0.)
            leg.get_frame().set_alpha(0)

            # Save.
            fig_path = os.path.join(sys_path, "results", split + "_" + label + "_pr_re_curve.pdf")
            plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
