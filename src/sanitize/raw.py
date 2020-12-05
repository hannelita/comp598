import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import pandas as pd
import json
from datetime import date, datetime, timezone
import pdb
# pdb.set_trace()
import csv
from os import listdir
from os.path import isfile, join
import re
import random

NUM_POSTS = 100

class Raw:
    def __init__(self, input_dir, dest):
        self.files = []
        self.get_files_from(input_dir)
        self.dest = dest
        self.filtered_files = []

    def get_files_from(self, input_dir):
        self.files = [(join(input_dir, f)) for f in listdir(input_dir) if (isfile(join(input_dir, f)) and f.endswith('.json') )]

    def generate_csvs(self):
        with open(self.dest, 'w+') as destination:
            csv_writer = csv.writer(destination, delimiter=',')
            # csv_writer.writerow(['name', 'title', 'coding'])
            csv_writer.writerow(['name', 'subreddit', 'm_trump', 'm_biden', 'title', 'coding'])
            for file_name in self.files:
                with open(file_name) as f:
                    for json_obj in f:
                        try:
                            line = json.loads(json_obj)
                            name = line.get("data", {}).get("name", "")
                            title = line.get("data", {}).get("title", "")
                            subreddit = line.get("data", {}).get("subreddit", "")
                            res = [name, subreddit, False, False, title, 7]

                            csv_writer.writerow(res)
                        except ValueError:
                            continue

        all_df = pd.read_csv(self.dest)
        return all_df
        
            

class RawClean:
    def __init__(self, dest, df):
        self.files = []
        self.all_df = dest
        self.filtered_files = []
        self.mention_df = df


    def clean(self):
        self.verify_duplicates()


    def verify_duplicates(self):
        res = self.all_df[(~self.all_df.name.isin(self.mention_df.name))]
        res.to_csv('./data/raw_dataset_csv/no_mention.csv', index=False)


    # def verify_duplicates(self, records, post):
    #     post_name = post.get("data", {}).get("name", "")
    #     if (post_name not in self.post_ids):
    #         self.post_ids.add(post_name)
    #         records.append(post)
    #     return records




