#!/usr/local/bin/python3

import os, sys, json, time
from bs4 import BeautifulSoup

# politifact parser
class politifactParser:
    
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "w")
        self.f.write("index\t\thref\t\truling\t\truling_date\t\tsite\n")

    # write one record
    def write(self, href, ruling, ruling_date, site):
        self.f.write("\t\t".join([str(self.index), href, ruling, ruling_date, site]) + "\n")
        self.index += 1
    
    # parse records one by one
    def parse(self, js):
        ruling = js["ruling"]["ruling"]
        ruling_date = js["ruling_date"]
        soup = BeautifulSoup(js["sources"], "html.parser")
        for a in soup.find_all("a"):
            href = a.get("href")
            if href:
                # if it is a facebook link and contain id of digits
                if "facebook.com/" in href and len([1 for c in href if c.isdigit()]) > 5:
                    self.write(href, ruling, ruling_date, "facebook")
                # if it is a twitter link and contain id of digits
                elif "twitter.com/" in href and len([1 for c in href if c.isdigit()]) > 5:
                    self.write(href, ruling, ruling_date, "twitter")
                # if it is a youtube video link
                elif "youtube.com/watch" in href or "youtu.be/" in href:
                    self.write(href, ruling, ruling_date, "youtube")
                """
                # count the appearence of domains
                if len(href.split("/")) > 2:
                    print("1," + href.split("/")[2].replace(",", ""))
                """
    
    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(raw_path):
            for path_postfix in path_postfixes:
                if "articles" not in path_postfix:
                    continue
                with open(os.path.join(path_base, path_postfix), "r") as f:
                    res = json.load(f)
                    for js in res["objects"]:
                        self.parse(js)
                print(path_postfix)

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "politifact_raw")
    save_path = os.path.join(file_path, "data", "politifact.ttsv")

    # parser initilization
    politifact = politifactParser(raw_path, save_path)
    politifact.traverse()
