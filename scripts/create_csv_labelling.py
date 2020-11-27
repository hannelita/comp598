#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint


from src.sanitize.create_csv import CsvLabelling

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output directory name (ends with / )')
parser.add_argument('-inputdir', help='Input directory to filter posts', required=False, default='./data/unique/')

args = parser.parse_args()

DEST = '{}'.format(args.o)
INPUT_DIR = '{}'.format(args.inputdir)

def main():
    print(f'Input files from {INPUT_DIR}')
    
    format_filtered_posts = CsvLabelling(INPUT_DIR, DEST)
    format_filtered_posts.generate_csvs_for_labelling()
    
    

if __name__ == "__main__":
    main()