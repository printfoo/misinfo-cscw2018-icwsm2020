#!/usr/local/bin/python3

import os, sys, json, time
from bs4 import BeautifulSoup

# snopes list parser
class snopesListParser:
    
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "w")

    # write one record
    def write(self, href):
        self.f.write(href + "\n")
    
    # parse records one by one
    def parse(self, f):
        soup = BeautifulSoup(f, "html.parser")
        if len(soup.find_all("article")) < 5:
            print(self.index)
        for article in soup.find_all("article"):
            for a in article.find_all("a"):
                href = a.get("href")
                self.write(href)
    
    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(raw_path):
            path_postfixes.sort()
            for path_postfix in path_postfixes:
                if "lists" not in path_postfix:
                    continue
                with open(os.path.join(path_base, path_postfix), "r") as f:
                    self.parse(f)
                # print(path_postfix)

# snopes list parser
class snopesParser:
    
    # initialization
    def __init__(self, raw_path, save_path):
        self.index = 0
        self.raw_path = raw_path
        self.save_path = save_path
        self.f = open(self.save_path, "w")
        self.f.write("index\t\thref\t\truling\t\truling_date\t\tsite\n")
    
    # write one record
    def write(self, href, ruling, ruling_date, site):
        self.f.write("\t\t".join([str(self.index), href, ruling, ruling_date, site]) + "\n")
        self.index += 1
        self.href_num += 1
    
    # parse records one by one
    def parse(self, f):
        soup = BeautifulSoup(f, "html.parser")
        for meta in soup.find_all("meta"):
            if meta.get("property") == "DC.date.issued":
                ruling_date = meta.get("content")
                break
        for article in soup.find_all("article"):
            ruling = ""
            for span in article.find_all("span"):
                if span.get("itemprop") == "alternateName":
                    ruling = span.text
                    break
            if ruling == "":
                return 0
            self.href_num = 0
            for a in article.find_all("a"):
                href = a.get("href")
                """
                    if self.href_num > 1: # only parse first 2 social media found
                    break
                """
                if href:
                    # if it is a facebook link and contain id of digits and not a share link
                    if "facebook.com/" in href and len([1 for c in href if c.isdigit()]) > 5 and \
                    "snopes.com" not in href and "archive.org" not in href:
                        self.write(href, ruling, ruling_date, "facebook")
                    # if it is a twitter link and contain id of digits
                    elif "twitter.com/" in href and len([1 for c in href if c.isdigit()]) > 5 and \
                    "snopes.com" not in href and "archive.org" not in href:
                        self.write(href, ruling, ruling_date, "twitter")
                    # if it is a youtube video link
                    elif "youtube.com/watch" in href or "youtu.be/" in href and \
                    "snopes.com" not in href and "archive.org" not in href:
                        self.write(href, ruling, ruling_date, "youtube")
    
    # traverse all raw responses
    def traverse(self):
        for path_base, _, path_postfixes in os.walk(raw_path):
            for path_postfix in path_postfixes:
                if "articles" not in path_postfix:
                    continue
                with open(os.path.join(path_base, path_postfix), "r") as f:
                    self.parse(f)
                print(path_postfix)

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "snopes_raw")
    
    # list parser initilization
    save_path = os.path.join(file_path, "data", "snopes_raw", "url_list")
    if not os.path.exists(save_path):
        snopes = snopesListParser(raw_path, save_path)
        snopes.traverse()
    else:
        save_path = os.path.join(file_path, "data", "snopes.ttsv")
        snopes = snopesParser(raw_path, save_path)
        snopes.traverse()
