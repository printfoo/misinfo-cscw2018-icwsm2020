#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os, sys, json, time

# mediabias crawler
class mediabiasCrawler:
    
    # initialization
    def __init__(self, save_path, bias_type):
        self.save_path = save_path
        self.base = "https://mediabiasfactcheck.com/"
        self.bias_type = bias_type
        self.helfs = []
        self.names = []

    # save current response and increment to next
    def save_and_increment(self, name):
        with open(os.path.join(self.save_path, name), "w") as f:
            f.write(str(self.res.content))
        if self.res.status_code >= 400:
            print(self.res.content)

    # get a list of websites
    def get_list(self):
        self.res = requests.get(self.base + self.bias_type)
        soup = BeautifulSoup(self.res.content, "html.parser")
        for div in soup.find_all("div"):
            if div.get("class") == ["entry", "clearfix"]:
                for p in div.find_all("p"):
                    if p.get("style") == "text-align: center;":
                        for a in p.find_all("a"):
                            href = a.get("href")
                            if "euromaiden-press" in href: # special case 1
                                href = href.replace("euromaiden-press", "euromaidan-press")
                            if "hermancain.com" in href: # special case 2
                                continue
                            self.helfs.append(href)
                            self.names.append(href.strip("/").split("/")[-1])

    # get a response
    def get_each(self):
        for name, href in zip(self.names, self.helfs):
            self.res = requests.get(href)
            print(name, self.res.status_code)
            self.save_and_increment(name)

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    root_save_path = os.path.join(file_path, "data", "mediabias_raw")

    # crawler initilization
    bias_types = ["left", "leftcenter", "center", "right-center", "right"]
    for bias_type in bias_types:
        save_path = os.path.join(root_save_path, bias_type)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        mediabias = mediabiasCrawler(save_path, bias_type)
        mediabias.get_list()
        mediabias.get_each()
