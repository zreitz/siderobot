#!/usr/bin/env python3
"""
Description:    Extract urls and relevant info from a twitter export `tweets.js`
Usage:          python parse_tweets.py tweets.js tweet_links.tsv
"""

import json
import csv
import re

from sys import argv


def parse_tweets(inpath, outpath):
    with open(inpath, 'r') as tweetf:
        js_text = tweetf.read()[25:]

    tweets = json.loads(js_text)

    tweet_info = []
    for tweet in tweets:
        tweet = tweet['tweet']

        # Get retweet info
        rt_pattern = r'RT @([^:]+)'
        match = re.search(rt_pattern, tweet['full_text'])
        if match:
            retweet = True
            url = f"https://twitter.com/{match.group(1)}/status/{tweet['id']}"
        else:
            urls = tweet['entities']['urls']
            if not urls:
                continue
            url = urls[0]['expanded_url']
            retweet = True if url.startswith("https://twitter.com") else False

        tweet_info.append({
                'date': tweet['created_at'],
                'retweet': retweet,
                'url': url,
                'text': tweet['full_text'].replace('\n', " ")
            })

    with open(outpath, 'w') as outf:
        fieldnames = ['date', 'retweet', 'url', 'text']
        writer = csv.DictWriter(outf, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(tweet_info)


if __name__ == "__main__":
    parse_tweets(argv[1], argv[2])
