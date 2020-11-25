#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint

from src.api.reddit.collect import Elections
from src.sanitize.filter import PostFilter

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output directory name (ends with / )')
parser.add_argument('-inputdir', help='Input directory to filter posts', required=False, default='./data/new/')
parser.add_argument('-endpoint', help='new or hot', required=False, default='new')
parser.add_argument('-numposts', help='Number of posts to collect. Can be any integer', type=int)

args = parser.parse_args()

DEST = '{}'.format(args.o)
INPUT_DIR = '{}'.format(args.inputdir)

def main():
    print(f'Input files from {INPUT_DIR}')
    
    filter_posts = PostFilter(INPUT_DIR, DEST)
    filter_posts.sanitize()
    filter_posts.generate_csvs_for_open_coding()
    
    

if __name__ == "__main__":
    main()