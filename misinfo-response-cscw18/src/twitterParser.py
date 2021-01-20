#!/usr/local/bin/python3

import os, sys, json, random, time, datetime
import pandas as pd

def get_month(s):
    return str({"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}[s])

# twitter parser
class twitterParser:
    
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "w")
    
    # parse records one by one
    def parse(self, res):
        for _ in res:
            if not _:
                continue
            js = json.loads(_) # original
            js2 = {"id": js["tweetId"]} # to save
            if "errors" in js["content"]: # if error
                js2["type"] = "exceptional"
                js2["paragraph"] = js["content"]["errors"][0]["message"]
                self.f.write(json.dumps(js2) + "\n")
            elif len(js["content"]) == 0: # if not comments
                js2["type"] = "exceptional"
                js2["paragraph"] = "noComments"
                self.f.write(json.dumps(js2) + "\n")
            else: # if have some comments
                for item in js["content"]:
                    js2["type"] = "normal"
                    js2["name"] = item["user"]["screen_name"]
                    js2["likes"] = item["user"]["favourites_count"]
                    time_str = get_month(item["created_at"][4:7]) + item["created_at"][7:]
                    js2["time"] = time.mktime(time.strptime(time_str, "%m %d %H:%M:%S +0000 %Y"))
                    text = item["text"]
                    for paragraph in text.split("\n"):
                        js2["paragraph"] = paragraph
                        self.f.write(json.dumps(js2) + "\n")
    
    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(self.raw_path):
            for path_postfix in path_postfixes:
                with open(os.path.join(path_base, path_postfix), "r") as tmp_f:
                    res = tmp_f.read().strip("\n").split("\n")
                    self.parse(res)

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "twitter_raw")
    save_path = os.path.join(file_path, "data", "twitter.json")

    # parser initilization
    twitter = twitterParser(raw_path, save_path)
    twitter.traverse()
