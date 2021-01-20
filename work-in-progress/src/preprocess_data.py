#!/usr/local/bin/python3

import os, sys, re, html
import pandas as pd
import numpy as np

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    raw_path = os.path.join(data_path, "annotations")
    clean_path = os.path.join(data_path, "data.csv")

    # Cleans annotated summary data.
    file_name = "List of stories and topic categorizations.xlsx"
    file_path = os.path.join(raw_path, file_name)
    lists = pd.read_excel(file_path, skiprows=0)
    lists["event"] = lists["Box file name"]
    lists = lists[["event", "primary category"]]
    
    # Cleans annotated event data.
    dfs = []
    for _, _, file_names in os.walk(raw_path):
        for file_name in file_names:
            if file_name == "List of stories and topic categorizations.xlsx":
                continue
            file_path = os.path.join(raw_path, file_name)
            
            skiprows=3
            if "Wisconsin" in file_name:
                skiprows=11

            df = pd.read_excel(file_path, skiprows=skiprows)
            
            if "Wisconsin" in file_name:
                df["belief"] = df["DB.1"]
                df["disbelief"] = df["DNB.1"]
                # df["neither"] = df["CT.1"]
            else:
                df["belief"] = df["DOES believe"]
                df["disbelief"] = df["DOES NOT believe"]
                # df["neither"] = df["Can't Tell"]
            
            df["event"] = file_name.split(".x")[0]
            df = df[["event", "belief", "disbelief"]]
            dfs.append(df)
    df = pd.concat(dfs)
    
    df = lists.merge(df, on="event")
    fe = lambda e: e.lower().split(",")[0].split("final")[0].split("form")[0].strip(" -")
    df["event"] = df["event"].apply(fe)
    df = df.fillna(0)
    df.to_csv(clean_path, index=False)
    print(df)
