#!/usr/local/bin/python3

import requests
import os, sys, json, time
import pandas as pd
from bs4 import BeautifulSoup

# snopes crawler
class votesmartCrawler:
    
    # initialization
    def __init__(self, list_path, speech_path, person):
        self.list_index = 0
        self.speech_index = 0
        self.base = "https://votesmart.org"
        self.old_list = []
        self.person = person
        self.list_path = os.path.join(list_path,
            "_".join([self.person[4], self.person[1], str(self.person[3])]))
        if not os.path.exists(self.list_path):
            os.mkdir(self.list_path)
        self.speech_path = os.path.join(speech_path,
            "_".join([self.person[4], self.person[1], str(self.person[3])]))
        if not os.path.exists(self.speech_path):
            os.mkdir(self.speech_path)
        self.add_url = "/candidate/public-statements/" + str(self.person[3]) + "/" + self.person[4]
        print(self.person, self.add_url)

    # save current response and increment to next
    def save_and_increment(self, type):
        if type == "list":
            with open(os.path.join(self.list_path, "{:05}".format(self.list_index)), "w") as f:
                for url in self.url_list:
                    f.write(url + "\n")
            self.list_index += 1
            self.get()
        if type == "speech":
            with open(os.path.join(self.speech_path, "{:05}".format(self.speech_index)), "w") as f:
                f.write(str(self.speech_res.content))
            self.speech_index += 1

    # get a response
    def get(self):
        self.url_list = []
        self.res = requests.get(self.base + self.add_url, params = {"p": self.list_index})
        print("List-", self.list_index, ": ", self.res.status_code)
        soup = BeautifulSoup(self.res.content, "html.parser")
        for table in soup.find_all("table"):
            for tr in table.find_all("tr"):
                for td in tr.find_all("td"):
                    for a in td.find_all("a"):
                        href = a.get("href")
                        self.url_list.append(href)
                        self.speech_res = requests.get(self.base + href)
                        print("Speech-", self.speech_index, ": ", self.speech_res.status_code)
                        self.save_and_increment("speech")
        if self.old_list == self.url_list: # end
            return
        else:
            self.old_list = self.url_list[:]
        self.save_and_increment("list")
        #time.sleep(1) # be gentle

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    poli_path = os.path.join(file_path, "data", "votesmart_raw", "politicians", "politicians.csv")
    list_path = os.path.join(file_path, "data", "votesmart_raw", "lists")
    speech_path = os.path.join(file_path, "data", "votesmart_raw", "speeches")

    # crawler initilization
    poli = pd.read_csv(poli_path)
    for person in poli.values:
        votesmart = votesmartCrawler(list_path, speech_path, person)
        votesmart.get()
