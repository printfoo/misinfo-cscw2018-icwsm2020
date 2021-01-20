#!/usr/local/bin/python3

import requests
import os, sys, json, time

# politifact crawler
class politifactCrawler:
    
    # initialization
    def __init__(self, save_path):
        self.index = 0
        self.save_path = save_path
        self.base = "http://www.politifact.com"
        self.next = "/api/v/2/statement/?format=json&order_by=ruling_date"
    
    # save current response and increment to next
    def save_and_increment(self):
        with open(os.path.join(self.save_path, "articles-{:05}".format(self.index)), "w") as f:
            json.dump(self.js, f)
        self.next = self.js["meta"]["next"]
        print(self.js["meta"]) # debug
        if self.next:
            self.index += 1
        else:
            sys.exit()

    # get a response
    def get(self):
        self.res = requests.get(self.base + self.next)
        self.js = json.loads(self.res.content)
        self.save_and_increment()
        #time.sleep(1) # be gentle

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    save_path = os.path.join(file_path, "data", "politifact_raw")
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # crawler initilization
    politifact = politifactCrawler(save_path)
    while True:
        politifact.get()
