#!/usr/bin/env python3
"""
Description:    Attempt to find abstracts from URLs
Requirements:   BeautifulSoup (pip install bs4)
"""

import re
import requests

from bs4 import BeautifulSoup

def get_doi(url):
    doi_pattern = r"10.\d{4,9}\/[-._;()\/:A-Za-z0-9]+"

    # Follow a retweet to get the true url
    # TODO: waiting on twitter API access
    if url.startswith("https://twitter.com"):
        # true_url = ...
        # url = true_url
        return "TWITTER"

    # Often DOI is in the url
    match = re.search(doi_pattern, url)
    if match:
        return match.group(0)

    return "OTHER"
    # Try to follow the link and parse from HTML
    # response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    # if response.status_code == 403:
    #     # TODO: Bypass cloudfare, etc
    #     return ""
    #
    # match = re.findall(doi_pattern, response.text)
    # if match:
    #     pass
    #soup = BeautifulSoup(response.text, "html.parser")



import csv

urls = []
with open("scholar_links.tsv", "r") as inf:
    reader = csv.DictReader(inf, delimiter="\t")
    for row in reader:
        urls.append(row['url'])

dois = []
for url in set(urls):
    doi = get_doi(url)
    dois.append(doi)

print(len(dois))
print(f"Twitter: {len([u for u in dois if u == 'TWITTER'])}")
print(f"Other: {len([u for u in dois if u == 'OTHER'])}")
