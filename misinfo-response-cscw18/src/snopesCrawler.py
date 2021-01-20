#!/usr/local/bin/python3

import requests
import os, sys, json, time

# snopes crawler
class snopesCrawler:
    
    # initialization
    def __init__(self, save_path, type, *args):
        self.index = 1
        self.type = type
        self.save_path = save_path
        self.base = "https://www.snopes.com/fact-check/page/"
        if args:
            self.url_list = args[0]

    # save current response and increment to next
    def save_and_increment(self):
        with open(os.path.join(self.save_path, self.type + "-{:05}".format(self.index)), "w") as f:
            f.write(self.res.content.decode("utf-8"))
        self.index += 1

    # get a response
    def get(self):
        if self.type == "lists":
            if self.index > 1182:
                exit()
            self.res = requests.get(self.base + str(self.index))
        else:
            if self.index > len(self.url_list):
                exit()
            self.res = requests.get(self.url_list[self.index - 1])
        print(self.index, self.res.status_code)
        self.save_and_increment()
        #time.sleep(1) # be gentle

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    save_path = os.path.join(file_path, "data", "snopes_raw")
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # list crawler initilization
    list_path = os.path.join(file_path, "data", "snopes_raw", "url_list")
    if not os.path.exists(list_path):
        snopes = snopesCrawler(save_path, "lists")
    else:
        with open(list_path, "r") as f:
            url_list = f.read().split("\n")[:-1]
        snopes = snopesCrawler(save_path, "articles", url_list)
    while True:
        snopes.get()
