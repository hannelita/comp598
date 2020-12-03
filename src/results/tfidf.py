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


class TfIdf:
    def __init__(self, input_dir):
        self.dfs = []
        self.get_dfs_from(input_dir)
        
    def get_dfs_from(self, input_dir):
        files = [(join(input_dir, f)) for f in listdir(input_dir)]
        df = pd.read_csv('./data/labelling/label_slice_0.csv')
        self.dfs.append(df)
        print(df.info())

    # def get_dfs_from(self, input_dir):
    #     files = [(join(input_dir, f)) for f in listdir(input_dir)]
    #     for f in files:
    #         df = pd.read_csv(f)
    #         self.dfs.append(df)
    #         print(df.info())

        
    # def check_mention(self, title, rregex):
    #     re_title = rregex.match(title)
    #     return (re_title is not None)

    # def meet_criteria(self, json_obj, records):
    #     return self.check_biden_trump(json.loads(json_obj), records)

    # def write_output_file(self, output_file, records):
    #     with open(output_file, 'w+') as fp:                
    #         for r in records:
    #             json.dump(r, fp)
    #             fp.write("\n")


    # def split_from_file(self, file_name, records):
    #     with open(file_name) as f:
    #         for json_obj in f:
    #             records.append(json.loads(json_obj))
    #     return records
        

    # def output_records(self, records, csv_writer):
    #     for line in records:
    #         name = line.get("data", {}).get("name", "")
    #         subreddit = line.get("data", {}).get("subreddit", "")
    #         title = line.get("data", {}).get("title", "")
    #         trump_re = re.compile("\D*[Tt][Rr][Uu][Mm][Pp].*")
    #         m_trump = self.check_mention(title, trump_re) 
    #         biden_re = re.compile("\D*[Bb][Ii][Dd][Ee][Nn].*")
    #         m_biden = self.check_mention(title, biden_re) 
    #         res = [name, subreddit, m_trump, m_biden, title, ""]
    #         csv_writer.writerow(res)


    # def print_statistics(self, politics_records, conservatives_records):
        

    #     print(f"There are {len(politics_records)} unique posts for politics")
    #     print(f"There are {len(conservatives_records)} unique posts for conservative")

    #     total_posts_len = len(politics_records) + len(conservatives_records)
    #     print(f"Total Posts (Unique) mentioning Trump or Biden {total_posts_len}")

    # def generate_csvs_for_labelling(self):
    #     politics_records = []
    #     conservatives_records = []
    #     for file_name in self.politics_files:
    #         politics_records = self.split_from_file(file_name, politics_records)
    #     for file_name in self.conservative_files:
    #         conservatives_records = self.split_from_file(file_name, conservatives_records)
        
    #     self.print_statistics(politics_records, conservatives_records)

    #     politics_posts_len = len(politics_records)
    #     politics_default_chunk_size = politics_posts_len // NUM_FILES
    #     politics_chunk_list = [politics_default_chunk_size] * (NUM_FILES - 1)
    #     politics_chunk_list.append( (politics_default_chunk_size + (politics_posts_len % NUM_FILES)) )
    #     conservative_posts_len = len(conservatives_records)
    #     conservative_default_chunk_size = conservative_posts_len // NUM_FILES
    #     conservative_chunk_list = [conservative_default_chunk_size] * (NUM_FILES - 1)
    #     conservative_chunk_list.append( (conservative_default_chunk_size + (conservative_posts_len % NUM_FILES)) )
        
    #     for idx, chunk in enumerate(politics_chunk_list):

    #         r = politics_records[(idx*politics_default_chunk_size): ((idx+1)*chunk) ]
    #         c = conservatives_records[(idx*conservative_default_chunk_size): ((idx+1)*(conservative_chunk_list[idx]))]
            
    #         r.extend(c)
    #         file_str = "label_slice_" + str(idx) + ".csv"
    #         output_file = join("./data/labelling/", file_str)
    #         with open(output_file, 'w+') as destination:
    #             csv_writer = csv.writer(destination, delimiter=',')
    #             csv_writer.writerow(['name', 'subreddit', 'm_trump', 'm_biden', 'title', 'coding'])
    #             self.output_records(r, csv_writer)
 

        
            

