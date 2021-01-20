#!/usr/local/bin/python3

import os, sys, json, random, time, datetime
import pandas as pd
import numpy as np

# facebook parser
class facebookParser:
    
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
            js2 = {"id": js["facebookId"]} # to save
            if "error" in js: # if error
                js2["type"] = "exceptional"
                js2["paragraph"] = js["error"]["message"]
                self.f.write(json.dumps(js2) + "\n")
            elif "data" not in js: # if recover id
                js2["type"] = "exceptional"
                js2["paragraph"] = "unknown"
                self.f.write(json.dumps(js2) + "\n")
            elif len(js["data"]) == 0: # if not comments
                js2["type"] = "exceptional"
                js2["paragraph"] = "noComments"
                self.f.write(json.dumps(js2) + "\n")
            else: # if have some comments
                for item in js["data"]:
                    js2["type"] = "normal"
                    js2["name"] = "unknown"
                    js2["likes"] = "unknown"
                    time_str = item["created_time"]
                    js2["time"] = time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%S+0000"))
                    text = item["message"]
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
    raw_path = os.path.join(file_path, "data", "facebook_raw")
    save_path = os.path.join(file_path, "data", "facebook.json")

    # parser initilization
    facebook = facebookParser(raw_path, save_path)
    facebook.traverse()
