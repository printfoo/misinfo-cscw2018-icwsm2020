#!/usr/local/bin/python3

import os, sys, json, time, re
from bs4 import BeautifulSoup
import unicodedata

# Snopes extractor.
class snopesExtractor:

    def __init__(self, raw_path, save_path, urls):
        self.index = 1
        self.raw_path = raw_path
        self.save_path = save_path
        self.urls = urls
        self.quotetoken = " QUOTETOKEN "
        self.mediatoken = " MEDIATOKEN "
        self.paratoken = " PARATOKEN "
        self.urltoken = " URLTOKEN "
        self.attoken = " USERTOKEN "
        self.quotetag = BeautifulSoup("<p>" + self.quotetoken + "</p>", "html.parser")
        self.mediatag = BeautifulSoup("<p>" + self.mediatoken + "</p>", "html.parser")
        self.f = open(self.save_path, "w")
        self.f.write("url\tdate\tverdict\tcontent\n")
    
    # Extract date.
    def extract_date(self, soup):
        for script in soup.find_all("script"):
            if script.get("type") == "application/ld+json":
                meta = json.loads(script.text)
                if "@graph" not in meta:
                    continue
                for info in meta["@graph"]:
                    if "datePublished" in info:
                        date = info["datePublished"]
                        return date
        return ""

    # Extract verdict.
    def extract_verdict(self, soup):
        for tag in soup.find_all("span"):  # Format for recent fact-checks.
            props = tag.get("class")
            if props and "h3" in props and "rating-label" in props[1]:
                return tag.text
        for tag in soup.find_all("div"):  # Format for old fact-checks.
            props = tag.get("class")
            if props and "claim-old" in props:
                return tag.text
        for tag in soup.find_all("span"):  # Format for even older fact-checks.
            props = tag.get("style")
            if props and "white-space:" in props:
                return tag.text
        for tag in soup.find_all("td"):  # Format for even older fact-checks.
            props = tag.get("valign")
            if props and "TOP" in props:
                return tag.text
        for tag in soup.find_all("p"):  # Format for even older fact-checks.
            if "Status:" in tag.text:
                return tag.text.replace("Status:", "")
        return ""
        
    # Extract content.
    def extract_content(self, soup):
        content = ""
        for tag in soup.find_all("div"):
            props = tag.get("class")
            if props and "single-body" in props:
                [t.replaceWith(self.quotetag) for t in tag("blockquote")]
                [t.replaceWith(self.mediatag) for t in tag("iframe")]
                [t.decompose() for t in tag("script")]
                [t.decompose() for t in tag("table")]
                [t.decompose() for t in tag("dt")]
                [t.decompose() for t in tag("dd")]
                for p in tag.find_all("p"):
                    classes = p.get("class")
                    paragraph = unicodedata.normalize("NFKC", p.text).strip()
                    if (not classes) and len(paragraph) >= 5 and \
                        not paragraph.startswith("Last updated:") and \
                        not paragraph.startswith("Example:") and \
                        not paragraph.startswith("Status:") and \
                        not paragraph.startswith("Claim:") and \
                        not paragraph.startswith("Sources:") and \
                        not paragraph.startswith("FACT CHECK:") and \
                        not "Additional information:" in paragraph and \
                        not "!function" in paragraph:
                        content += paragraph + "\n"
                content = re.sub("http\S+", self.urltoken, content).strip()
                content = re.sub("@\S+", self.attoken, content).strip()
                content = re.sub("\t+", " ", content).strip()
                content = re.sub("\n+", self.paratoken, content).strip()
                content = re.sub(" +", " ", content).strip()
                return content
        return ""

    # Traverse all raw responses.
    def traverse(self):
        file_name = "articles-{:05d}".format(self.index)
        file_path = os.path.join(self.raw_path, file_name)
        if not os.path.exists(file_path):  # Done, no next one.
            return False
        with open(file_path, "r") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        # Extract date.
        date = self.extract_date(soup)
        
        # Extract and clean verdict.
        verdict = self.extract_verdict(soup)
        verdict = re.sub("[^a-z ]+", " ", verdict.lower())
        verdict = re.sub(" +", " ", verdict).strip()
        if not verdict or verdict == " ":  # Verdict not found.
            self.index += 1
            return True

        # Extract and clean content.
        content = self.extract_content(soup)
        if not content:  # Content not found.
            self.index += 1
            return True

        # Write to file.
        url = self.urls[self.index-1]
        self.f.write("\t".join([url, date, verdict, content]) + "\n")
        print(self.index, "\t", date[:10], "\t", verdict)
        self.index += 1
        return True


if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "snopes_raw")
    url_path = os.path.join(raw_path, "url_list")
    with open(url_path, "r") as f:
        urls = f.read().split("\n")[:-1]
    save_path = os.path.join(file_path, "public_data", "snopes.tsv")
    snopes = snopesExtractor(raw_path, save_path, urls)
    flag = True
    while flag:
        flag = snopes.traverse()
        
