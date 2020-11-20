#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint

from src.api.reddit.collect import Elections

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='JSON output file name')
parser.add_argument('-subreddit', help='Subreddit to collect posts', required=False, default='/r/politics')
parser.add_argument('-endpoint', help='new or hot', required=False, default='new')
parser.add_argument('-numposts', help='Number of posts to collect. Can be any integer', type=int)

args = parser.parse_args()

DEST = '{}'.format(args.o)
SUBREDDIT = '{}'.format(args.subreddit) 
ENDPOINT='{}'.format(args.endpoint) 
NUM_POSTS=args.numposts


def main():
    print(SUBREDDIT)
    print(NUM_POSTS)
    elections = Elections(DEST, NUM_POSTS)
    posts = elections.fetch_posts(SUBREDDIT, ENDPOINT)
    

if __name__ == "__main__":
    main()