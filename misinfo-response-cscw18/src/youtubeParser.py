#!/usr/local/bin/python3

import os, sys, json, random, time, datetime
import pandas as pd

# youtube parser
class youtubeParser:
    
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "w")
    
    # parse records one by one
    def parse(self, res):
        for _ in res:
            js = json.loads(_) # original
            js2 = {"id": js["videoId"]} # to save
            if "error" in js: # if error
                js2["type"] = "exceptional"
                js2["paragraph"] = js["error"]["errors"][0]["reason"]
                self.f.write(json.dumps(js2) + "\n")
            elif len(js["items"]) == 0: # if not comments
                js2["type"] = "exceptional"
                js2["paragraph"] = "noComments"
                self.f.write(json.dumps(js2) + "\n")
            else: # if have some comments
                for item in js["items"]:
                    js2["type"] = "normal"
                    js2["name"] = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                    js2["likes"] = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                    time_str = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                    js2["time"] = time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%S.000Z"))
                    text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
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
    raw_path = os.path.join(file_path, "data", "youtube_raw")
    save_path = os.path.join(file_path, "data", "youtube.json")

    # parser initilization
    youtube = youtubeParser(raw_path, save_path)
    youtube.traverse()
