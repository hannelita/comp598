#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint


from src.sanitize.raw import Raw, RawClean
from src.results.tfidf import TfIdf

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file name')
parser.add_argument('-inputdir', help='Input directory to filter posts', required=False, default='./data/new/')
parser.add_argument('-labeldir', help='Input directory to calculate TF-IDF', required=False, default='./data/labelling/')

args = parser.parse_args()

DEST = '{}'.format(args.o)
INPUT_DIR = '{}'.format(args.inputdir)
LABEL_DIR = '{}'.format(args.labeldir)

def main():
    print(f'Input files from {INPUT_DIR}')
    
    raw_posts = Raw(INPUT_DIR, DEST)
    dest = raw_posts.generate_csvs()

    tfidf = TfIdf(LABEL_DIR)
    df = tfidf.ret_df()

    raw_posts_non_mention = RawClean(dest, df)
    raw_posts_non_mention.clean()

    
    

if __name__ == "__main__":
    main()