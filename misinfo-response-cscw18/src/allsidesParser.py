#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os, sys, json, time

# allsides parser
class allsidesParser:
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "a")

    # write one record
    def write(self, title, site, allsides_bias_str, community_agree, community_disagree, community_bias_str):
        self.f.write("\t".join([title, site, allsides_bias_str, community_agree, community_disagree, community_bias_str]) + "\n")

    # parse records one by one
    def parse(self, tmp_f):
        soup = BeautifulSoup(tmp_f, "html.parser")
        for tbody in soup.find_all("tbody"):
            for tr in tbody.find_all("tr"):
                title = ""
                site = ""
                allsides_bias_str = ""
                community_agree = ""
                community_disagree = ""
                community_bias_str = ""
                for td in tr.find_all("td"):
                    if "source-title" in td.get("class"):
                        for a in td.find_all("a"):
                            title = a.get("href").split("/")[-1]
                    elif "views-field-field-bias-image" in td.get("class"):
                        for a in td.find_all("a"):
                            allsides_bias_str = a.get("href").split("/")[-1]
                    elif "community-feedback" in td.get("class"):
                        for div in td.find_all("div"):
                            if "rate-details" in div.get("class"):
                                for span in div.find_all("span"):
                                    if "agree" in span.get("class"):
                                        community_agree = span.get_text()
                                    elif "disagree" in span.get("class"):
                                        community_disagree = span.get_text()
                            elif "star" in div.get("class"):
                                for span in div.find_all("span"):
                                    if "on" in span.get("class"):
                                        community_bias_str = div.get("class")[1]
                with open(os.path.join(self.raw_path[:-1], title), "r") as f2:
                    soup2 = BeautifulSoup(f2, "html.parser")
                for a in soup2.find_all("a"):
                    if a.get("class"):
                        if "www" in a.get("class"):
                            site = a.get("href")
                            if len(site.split("/")) >= 5:
                                site = ""
                self.write(title, site, allsides_bias_str, community_agree, community_disagree, community_bias_str)

    # traverse all raw responses
    def traverse(self):
        with open(self.raw_path, "r") as tmp_f:
            self.parse(tmp_f)

# compute score from label
def get_allsides_bias(s):
    if s == "left":
        return -1
    elif s == "left-center":
        return -0.5
    elif s == "center":
        return 0
    elif s == "right-center":
        return 0.5
    elif s == "right":
        return 1
    else:
        return np.nan

# compute score from label
def get_community_bias(s):
    if s == "star-1":
        return -1
    elif s == "star-2":
        return -0.5
    elif s == "star-3":
        return 0
    elif s == "star-4":
        return 0.5
    elif s == "star-5":
        return 1
    else:
        return np.nan

# remove www. and m. temporarily
def get_domain(url):
    url = str(url).lower()
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    url = url.split("/")[0]
    if url.startswith("www."):
        return url[4:]
    elif url.startswith("m."):
        return url[2:]
    else:
        return url

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    root_raw_path = os.path.join(file_path, "data", "allsides_raw")
    save_path = os.path.join(file_path, "data", "allsides.tsv")
    
    if not os.path.exists(save_path):
        with open(save_path, "w") as f:
            f.write("\t".join(["title", "site", "allsides_bias_str", "community_agree", "community_disagree", "community_bias_str"]) + "\n")
        # crawler initilization
        for file_num in ["1", "2", "3", "4", "5", "6"]:
            raw_path = os.path.join(root_raw_path, file_num)
            allsides = allsidesParser(raw_path, save_path)
            allsides.traverse()

    else:
        df = pd.read_csv(save_path, sep = "\t")
        df["domain"] = df["site"].apply(get_domain)
        df["allsides_bias"] = df["allsides_bias_str"].apply(get_allsides_bias)
        df["community_bias"] = df["community_bias_str"].apply(get_community_bias)
        df.to_csv(save_path, sep = "\t", index = False)
