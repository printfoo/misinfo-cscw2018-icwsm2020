#!/usr/local/bin/python3

import requests
import os, sys, json, random, time
import pandas as pd
import multiprocessing as mp

# facebook crawler
class facebookCrawler:
    
    # initialization
    def __init__(self, keys, id, save_path):
        self.keys = keys
        self.idname = id
        self.save_path = save_path
        self.key_update()
        self.save_file = open(os.path.join(self.save_path, self.idname), "w")
        if self.idname.split(":::::")[0].isdigit():
            self.id = self.idname.split(":::::")[0]
        else:
            self.params = {"access_token": self.key, "fields": "id"}
            self.base = "https://graph.facebook.com/v2.12/" + self.idname.split(":::::")[0]
            self.id_recover()
        self.params = {"access_token": self.key, "summary": True, "limit": 1000}
        self.base = "https://graph.facebook.com/v2.12/" + self.id + "/comments"
    
    # save json to file
    def save(self):
        self.js["facebookId"] = self.idname
        self.save_file.write(json.dumps(self.js) + "\n")
        #time.sleep(15)
    
    # get next key
    def key_update(self):
        try:
            self.key = self.keys[0]
        except IndexError:
            print("No usable key left.")
            sys.exit()

    # get real id from alias
    def id_recover(self):
        self.res = requests.get(self.base, params = self.params)
        if self.res.status_code >= 400:
            print("ID Recovery Failed: ", self.res.content)
        else:
            print("ID Recovery Succeed: ", self.idname, self.res.status_code)
        self.js = json.loads(self.res.content)
        self.save()
        if "id" in self.js:
            self.id = self.js["id"] + "_" + self.idname.split(":::::")[1]
        else:
            self.id = self.idname.split(":::::")[1]

    # get a response
    def get(self):
        self.res = requests.get(self.base, params = self.params)
        if self.res.status_code >= 400:
            print("Comments Crawling Failed: ", self.res.content)
        else:
            print("Comments Crawling Succeed: ", self.idname, self.res.status_code)
        self.js = json.loads(self.res.content)
        self.save()
        if "paging" not in self.js:
            return 0
        while "next" in self.js["paging"]:
            self.base = self.js["paging"]["next"]
            self.res = requests.get(self.base)
            print(self.id, self.res.status_code)
            if self.res.status_code >= 400:
                print(self.res.content)
            self.js = json.loads(self.res.content)
            self.save()
            if "paging" not in self.js:
                return 0
        self.save_file.close()

# get youtube video ids from factcheck data
def get_ids(id_path):
    factcheck = pd.read_csv(id_path)
    factcheck = factcheck[factcheck["site"] == "facebook"]
    return list(factcheck["social_id"].drop_duplicates().dropna().values)

# get usable youtube keys
def get_keys(key_path):
    with open(key_path, "r") as key_file:
        keys = key_file.read().strip("\n").split("\n")
    return keys

# create youtube crawler class and start crawling
def create_facebook_crawler(keys, id, save_path):
    facebook = facebookCrawler(keys, id, save_path)
    facebook.get()

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    
    # get all video ids to crawl
    id_path = os.path.join(file_path, "data", "factcheck.csv")
    ids = get_ids(id_path)

    # get all usable keys
    key_path = os.path.join(file_path, "resources", "facebook.keys")
    keys = get_keys(key_path)

    # intilize save path
    save_path = os.path.join(file_path, "data", "facebook_raw")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # crawler initilization
    for id in ids:
        create_facebook_crawler(keys, id, save_path)
