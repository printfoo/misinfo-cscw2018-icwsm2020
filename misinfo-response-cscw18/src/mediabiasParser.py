#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import pandas as pd
import os, sys, json, time

# mediabias parser
class mediabiasParser:
    # initialization
    def __init__(self, raw_path, save_path, bias_type):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.bias_type = bias_type
        self.f = open(self.save_path, "a")

    # write one record
    def write(self, bias_img_link, bias_img, ruling, site):
        self.f.write("\t".join([str(self.index), self.bias_type, bias_img_link, bias_img, ruling, site]) + "\n")
        self.index += 1

    # parse records one by one
    def parse(self, f):
        soup = BeautifulSoup(f, "html.parser")
        if self.path_postfix == "the-fucking-news": # special case 1
            site = "http://thefingnews.com/"
        if self.path_postfix == "western-free-press": # special case 2
            bias_img_link = "https://i0.wp.com/mediabiasfactcheck.com/wp-content/uploads/2016/12/right011.png?resize=600%2C67&#038;ssl=1"
            bias_img = "right01"
        if self.path_postfix == "egyptian-streets": # special case 3
            return
        for article in soup.find_all("article"):
            for h1 in article.find_all("h1"):
                for img in h1.find_all("img"):
                    bias_img_link = img.get("src")
                    bias_img = img.get("data-image-title")
                    break
            for p in article.find_all("p"):
                text = p.get_text()
                if text.startswith("Factual Reporting:") or text.startswith("Factual News:") or text.startswith("Bias"):
                    ruling = text.replace("Factual Reporting:", "") \
                        .replace("Factual News:", "").replace("Bias:", "")\
                        .replace("\\xc2", "").replace("\\xa0", "").replace(" ", "") \
                        .split("\n")[0].split("\\n")[0].lower()
                if text.startswith("Source:") or text.startswith("Sources:") or text.startswith("Notes:"):
                    for a in p.find_all("a"):
                        site = a.get("href")
                        break
        self.write(bias_img_link, bias_img, ruling, site)

    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(raw_path):
            for path_postfix in path_postfixes:
                self.path_postfix = path_postfix
                print(path_postfix)
                with open(os.path.join(path_base, path_postfix), "r") as f:
                    self.parse(f)

# compute score from label
def get_score(s):
    #  e-left     left      left-center    center    right-center    right     e-right
    # <------|------------|------------|------------|------------|------------|------>
    end_len = 0.1
    interval = (1 - end_len) * 2 / 5
    split = [-1 + end_len, -1 + end_len + interval, -1 + end_len + interval * 2,
             1 - end_len - interval * 2, 1 - end_len - interval, 1 - end_len]
    # extreme-left 3,6
    if "extremeleft" in s:
        label = float(s.replace("extremeleft", ""))
        score = -1 + label / 6 * end_len
    # extreme-right 6-3
    elif "extremeright" in s:
        label = float(s.replace("extremeright", ""))
        score = split[-1] + (end_len - label / 6 * end_len)
    # left-center 1-11
    elif "leftcenter" in s:
        label = float(s.replace("leftcenter", ""))
        score = split[1] + label / 11 * interval
    # right-center 12-1
    elif "rightcenter" in s:
        label = float(s.replace("rightcenter", ""))
        score = split[3] + (interval - label / 12 * interval)
    # left 1-12
    elif "left" in s:
        label = float(s.replace("left", ""))
        score = split[0] + label / 12 * interval
    # right 11-1
    elif "right" in s:
        label = float(s.replace("right", ""))
        score = split[-2] + (interval - label / 11 * interval)
    # center 1-10
    elif "leastbiased" in s:
        label = float(s.replace("leastbiased", ""))
        score = split[2] + label / 11 * interval
    else:
        print(s)
    return score

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
    root_raw_path = os.path.join(file_path, "data", "mediabias_raw")
    save_path = os.path.join(file_path, "data", "mediabias.tsv")
    
    if not os.path.exists(save_path):
        with open(save_path, "w") as f:
            f.write("\t".join(["index", "bias_type", "bias_img_link", "bias_img", "ruling", "site"]) + "\n")
        # crawler initilization
        bias_types = ["left", "leftcenter", "center", "right-center", "right"]
        for bias_type in bias_types:
            raw_path = os.path.join(root_raw_path, bias_type)
            mediabias = mediabiasParser(raw_path, save_path, bias_type)
            mediabias.traverse()

    else:
        df = pd.read_csv(save_path, sep = "\t")
        df["domain"] = df["site"].apply(get_domain)
        for domain in df["domain"]:
            print(domain)
        df["score"] = df["bias_img"].apply(get_score)
        df = df.sort_values("score")
        for row in df[["bias_img", "score"]].drop_duplicates().values:
            print(row[0], "\t", row[1])
        df.to_csv(save_path, sep = "\t", index = False)
