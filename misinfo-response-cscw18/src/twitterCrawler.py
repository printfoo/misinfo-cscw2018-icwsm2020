#!/usr/local/bin/python3

from requests_oauthlib import OAuth1
import requests
import os, sys, json, random, time
import pandas as pd
import multiprocessing as mp

# twitter crawler
class twitterCrawler:
    
    # initialization
    def __init__(self, keys, id, save_path):
        self.keys = keys
        self.id = id
        self.save_path = save_path
        self.key_update()
        self.save_file = open(os.path.join(self.save_path, self.id), "w")
        self.params = {"count": 100, "id": self.id}
        self.base = "https://api.twitter.com/1.1/statuses/retweets.json"
    
    # save json to file
    def save(self):
        self.save_js = {"tweetId": self.id, "content": self.js}
        self.save_file.write(json.dumps(self.save_js) + "\n")
        time.sleep(15)
    
    # get next key
    def key_update(self):
        try:
            oath_ele = self.keys[0].split("\t")
            self.key = OAuth1(oath_ele[0], oath_ele[1], oath_ele[2], oath_ele[3])
        except IndexError:
            print("No usable keys left.")
            sys.exit()

    # get a response
    def get(self):
        self.res = requests.get(self.base, params = self.params, auth = self.key)
        if self.res.status_code >= 400:
            print(self.res.content)
        self.js = json.loads(self.res.content)
        self.save()
        self.save_file.close()

# get youtube video ids from factcheck data
def get_ids(id_path):
    factcheck = pd.read_csv(id_path)
    factcheck = factcheck[factcheck["site"] == "twitter"]
    return list(factcheck["social_id"].drop_duplicates().dropna().values)

# get usable youtube keys
def get_keys(key_path):
    with open(key_path, "r") as key_file:
        keys = key_file.read().strip("\n").split("\n")
    return keys

# create youtube crawler class and start crawling
def create_twitter_crawler(keys, id, save_path):
    twitter = twitterCrawler(keys, id, save_path)
    twitter.get()

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    
    # get all video ids to crawl
    id_path = os.path.join(file_path, "data", "factcheck.csv")
    ids = get_ids(id_path)

    # get all usable keys
    key_path = os.path.join(file_path, "resources", "twitter.keys")
    keys = get_keys(key_path)
    
    # intilize save path
    save_path = os.path.join(file_path, "data", "twitter_raw")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # crawler initilization
    for id in ids:
        create_twitter_crawler(keys, id, save_path)
