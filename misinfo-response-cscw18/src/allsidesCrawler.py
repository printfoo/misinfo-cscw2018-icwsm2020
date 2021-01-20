#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
import os, sys, json, time

# allsides crawler
class allsidesCrawler:
    
    # initialization
    def __init__(self, save_path):
        self.save_path = save_path
        self.base = "https://www.allsides.com/media-bias/media-bias-ratings"
        self.para = {"page": 0}

    # save current response and increment to next
    def save(self, file_name):
        with open(os.path.join(self.save_path, file_name), "w") as f:
            f.write(str(self.res.content))
        print(self.res.status_code)
        if self.res.status_code >= 400:
            print(self.res.content)

    # get a list of websites
    def get(self):
        if self.para["page"] == 0:
            self.res = requests.get(self.base)
            self.para["page"] += 1
        elif self.para["page"] > 0 and self.para["page"] < 7:
            self.res = requests.get(self.base, params = self.para)
            self.para["page"] += 1
        else:
            return
        self.save(str(self.para["page"]))
        soup = BeautifulSoup(self.res.content, "html.parser")
        for tbody in soup.find_all("tbody"):
            for tr in tbody.find_all("tr"):
                for td in tr.find_all("td"):
                    if "source-title" in td.get("class"):
                        for a in td.find_all("a"):
                            href = a.get("href")
                            self.res = requests.get("https://www.allsides.com" + href)
                            self.save(href.split("/")[-1])
        self.get()

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    save_path = os.path.join(file_path, "data", "allsides_raw")

    # crawler initilization
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    allsides = allsidesCrawler(save_path)
    allsides.get()
