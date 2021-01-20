#!/usr/local/bin/python3

import os, sys, json, time, datetime
import pandas as pd
import numpy as np

# get id of certain platform
def row_cleaner(row):
    # identify social media id
    row["social_id"] = np.nan
    if row["site"] == "youtube":
        if "youtube.com" in row["href"] and "watch?v=" in row["href"]:
            row["social_id"] = row["href"].split("watch?v=")[-1].split("&")[0][:11]
        elif "youtu.be" in row["href"] and "watch" not in row["href"]:
            row["social_id"] = row["href"].split("/")[-1].split("?")[0][:11]
    elif row["site"] == "twitter":
        tmp_list = row["href"].replace("?", "/").replace("#", "/").split("/")
        if "status" in tmp_list:
            row["social_id"] = tmp_list[tmp_list.index("status") + 1][:18]
        elif "statuses" in tmp_list:
            row["social_id"] = tmp_list[tmp_list.index("statuses") + 1][:18]
    elif row["site"] == "facebook":
        tmp_list = row["href"].replace("?", "/").replace("&", "/") \
            .replace(":", "/").replace("#", "/") \
            .replace("fbid=", "/").replace("_id=", "/").replace("v=", "/") \
            .split("/")
        alias = ""
        social_id = ""
        for i in range(len(tmp_list)):
            if tmp_list[i].isdigit() and len(tmp_list[i]) > 5:
                social_id = tmp_list[i]
            if tmp_list[i] == "posts":
                alias = tmp_list[i - 1]
            if tmp_list[i] == "notes" or tmp_list[i] == "pages":
                alias = tmp_list[i + 1]
        if alias and social_id:
            row["social_id"] = alias + ":::::" + social_id
        elif social_id:
            row["social_id"] = social_id
    else:
        pass

    # get time
    try:
        row["ruling_time"] = time.mktime(time.strptime(row["ruling_date"][:18], "%Y-%m-%dT%H:%M:%S"))
    except:
        row["ruling_time"] = np.nan

    # assign a numerical value for each ruling
    try:
        r = row["ruling"].lower()
    except:
        row["ruling_val"] = np.nan
        return row
    if r == "true":
        row["ruling_val"] = 2
    elif r == "mostly true":
        row["ruling_val"] = 1
    elif r == "half-true" or r.lower() == "mixture":
        row["ruling_val"] = 0
    elif r == "mostly false":
        row["ruling_val"] = -1
    elif r == "false" or r == "pants on fire!":
        row["ruling_val"] = -2
    else:
        row["ruling_val"] = np.nan
    return row

# main
if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    politifact_path = os.path.join(file_path, "data", "politifact.ttsv")
    snopes_path = os.path.join(file_path, "data", "snopes.ttsv")
    save_path = os.path.join(file_path, "data", "factcheck.csv")
    
    # list parser initilization
    politifact = pd.read_csv(politifact_path, sep = "\t\t", engine = "python")
    politifact["checkedby"] = "politifact"
    snopes = pd.read_csv(snopes_path, sep = "\t\t", engine = "python")
    snopes["checkedby"] = "snopes"
    df = pd.concat([politifact, snopes])
    df = df.apply(row_cleaner, axis = 1)
    df = df.sort_values("ruling_val")
    df = df.drop_duplicates(subset = ["social_id", "checkedby"])
    df.to_csv(save_path, index = False)
