#!/usr/bin/env python3
"""
Description:    Extract urls and relevant info from a gmail mbox file
Usage:          python parse_mbox.py Scholar_Alerts.mbox scholar_links.tsv
Requirements:   Mailbox (pip install mailbox)
                BeautifulSoup (pip install bs4)
"""

import quopri
import re
import csv
from sys import argv

import mailbox
from bs4 import BeautifulSoup


def parse_mbox(path):
    mbox = mailbox.mbox(path)

    papers = []
    for i, message in enumerate(mbox):
        # Get main body
        if message.is_multipart():
            content = ''.join(part.get_payload() for part in message.get_payload())
        else:
            content = message.get_payload()

        # Decode the quoted-printable format
        content = quopri.decodestring(content).decode('latin-1')
        # Get paper links (<a class = gse_alrt_title>) from the html
        html = BeautifulSoup(content, 'html.parser')
        links = html.find_all("a", {"class": "gse_alrt_title"})

        url_pattern = r'url=([^&]+)'
        for link in links:
            match = re.search(url_pattern, link.get('href'))
            if match:
                url = match.group(1)
            else:
                continue  # Skips "See all recommendations" links
            papers.append({
                "date": message['date'],
                "subject": message['subject'],
                'archived': "Archived" in message['X-Gmail-Labels'],
                "url": url,
                "title": link.text
            })
    return papers


def main(inpath, outpath):
    papers = parse_mbox(inpath)
    if not papers:
        raise()
    fieldnames = ['date', 'subject', 'archived', 'url', 'title']

    with open(outpath, 'w') as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)


if __name__ == "__main__":
    inpath = argv[1]
    outpath = argv[2]

    main(inpath, outpath)

