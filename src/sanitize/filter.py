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

class PostFilter:
    def __init__(self, input_dir, dest_dir):
        self.files = []
        self.get_files_from(input_dir)
        self.dest_dir = dest_dir
        self.filtered_files = []

    def get_files_from(self, input_dir):
        self.files = [(join(input_dir, f)) for f in listdir(input_dir) if (isfile(join(input_dir, f)) and f.endswith('.json') )]

        
    def check_biden_trump(self, post, records):
        title = post.get("data", {}).get("title", "")
        trump_re = re.compile("\D*[Tt][Rr][Uu][Mm][Pp].*")
        biden_re = re.compile("\D*[Bb][Ii][Dd][Ee][Nn].*")
        res_trump_title = trump_re.match(title)
        res_biden_title = biden_re.match(title)
        if (res_trump_title or res_biden_title) is not None:
            records.append(post)
        return records
        

    def meet_criteria(self, json_obj, records):
        return self.check_biden_trump(json.loads(json_obj), records)

    def write_output_file(self, output_file, records):
        with open(output_file, 'w+') as fp:                
            for r in records:
                json.dump(r, fp)
                fp.write("\n")


    def sanitize(self):
        for file_name in self.files:
            with open(file_name) as f:
                records = []
                for json_obj in f:
                    try:
                        records = self.meet_criteria(json_obj, records)
                    except ValueError:
                        continue
                output_file = join(self.dest_dir, ("filtered_" + (file_name.split("/")[-1])))
                self.write_output_file(output_file, records)
                self.filtered_files.append(output_file)

    def split_from_file(self, file_name, records):
        with open(file_name) as f:
            for json_obj in f:
                try:
                    records.append(json.loads(json_obj))
                except ValueError:
                    continue
        return records
        

    def sample_from_collection(self, destination, records, csv_writer):
        filtered_entries_len = len(records)
        entries_to_extract = random.sample(range(1, filtered_entries_len), NUM_POSTS)
        
        for entry in entries_to_extract:
            line = records[entry]
            name = line.get("data", {}).get("name", "")
            title = line.get("data", {}).get("title", "")
            res = [name, title, ""]
            csv_writer.writerow(res)



    def generate_csvs_for_open_coding(self):
        politics_records = []
        conservatives_records = []
        records = []
        for file_name in self.filtered_files:
            if file_name.endswith('politics.json'):
                politics_records = self.split_from_file(file_name, politics_records)
            else:
                conservatives_records = self.split_from_file(file_name, conservatives_records)

        output_file = join("./data/sampled2/", "sampled.csv")
        with open(output_file, 'w+') as destination:
            csv_writer = csv.writer(destination, delimiter=',')
            csv_writer.writerow(['name', 'title', 'coding'])
            self.sample_from_collection(destination, politics_records, csv_writer)
            self.sample_from_collection(destination, conservatives_records, csv_writer)


        
        
            

