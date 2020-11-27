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


class FormatFiltered:
    def __init__(self, input_dir, dest_dir):
        self.files = []
        self.get_files_from(input_dir)
        self.dest_dir = dest_dir
        self.post_ids = set()

    def get_files_from(self, input_dir):
        self.files = [(join(input_dir, f)) for f in listdir(input_dir) if (isfile(join(input_dir, f)) and f.endswith('.json') )]

    def verify_duplicates(self, records, post):
        post_name = post.get("data", {}).get("name", "")
        if (post_name not in self.post_ids):
            self.post_ids.add(post_name)
            records.append(post)
        return records


    def sanitize(self):
        for file_name in self.files:
            with open(file_name) as f:
                records = []
                for json_obj in f:
                    try:
                        post = json.loads(json_obj)
                        records = self.verify_duplicates(records, post)
                    except ValueError:
                        continue
                output_file = join(self.dest_dir, ("unique_filtered_" + (file_name.split("/")[-1])))
                self.write_output_file(output_file, records)
    #             self.filtered_files.append(output_file)

    def write_output_file(self, output_file, records):
        with open(output_file, 'w+') as fp:                
            for r in records:
                json.dump(r, fp)
                fp.write("\n")

        