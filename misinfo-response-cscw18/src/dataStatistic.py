#!/usr/local/bin/python3

import os, sys, json, time, datetime, math
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    factcheck_path = os.path.join(file_path, "data", "factcheck.csv")
    corpus_path = os.path.join(file_path, "data", "corpus_token.csv")
    
    # list parser initilization
    df1 = pd.read_csv(corpus_path)
    df = pd.read_csv(factcheck_path)
    """
    df1 = df1[df1["type"] == "exceptional"]
    df1 = df1[df1["tokens"] == "nocomments"]
    df1 = df1.merge(df, left_on = "id", right_on = "social_id")
    print(df1)
    print(df1.groupby(["id", "time"]).count())
    print("twitter", df1[df1["site"] == "twitter"].groupby(["id", "time"]).count())
    print("facebook", df1[df1["site"] == "facebook"].groupby(["id", "time"]).count())
    print("youtube", df1[df1["site"] == "youtube"].groupby(["id", "time"]).count())
    sys.exit()
    """
    df = pd.read_csv(factcheck_path)
    """
    print(df[df["checkedby"] == "politifact"].groupby("ruling").count())
    print(df[df["checkedby"] == "snopes"].groupby("ruling").count())
    sys.exit()
    print("twitter", len(df[df["site"] == "twitter"]))
    print("facebook", len(df[df["site"] == "facebook"]))
    print("youtube", len(df[df["site"] == "youtube"]))
    """
    dup_snopes_list = []
    dup_politifact_list = []
    for id, tdf in df.groupby("social_id"):
        if len(tdf) > 1 and "snopes" in tdf["checkedby"].values and "politifact" in tdf["checkedby"].values:
            s = tdf[tdf["checkedby"] == "snopes"]["ruling_val"].values[0]
            p = tdf[tdf["checkedby"] == "politifact"]["ruling_val"].values[0]
            if (not math.isnan(s)) and (not math.isnan(p)):
                print(tdf["href"].values[0], s, p)
                dup_snopes_list.append(int(s))
                dup_politifact_list.append(int(p))
    print(spearmanr(dup_snopes_list, dup_politifact_list))
    print(len(dup_snopes_list), len(dup_politifact_list))
