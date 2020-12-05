#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint


from src.results.tfidf import TfIdf

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file name')
parser.add_argument('-inputdir', help='Input directory to calculate TF-IDF', required=False, default='./data/labelling/')

args = parser.parse_args()

DEST = '{}'.format(args.o)
INPUT_DIR = '{}'.format(args.inputdir)

def generate_json_output(res):
    with open(DEST, 'w+') as fp:
        json.dump(res, fp)

def main():
    print(f'Input files from {INPUT_DIR}')
    
    tfidf = TfIdf(INPUT_DIR)
    res = tfidf.calculate(2)
    generate_json_output(res)
    
    

if __name__ == "__main__":
    main()