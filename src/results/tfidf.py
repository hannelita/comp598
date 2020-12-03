import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import pandas as pd
import json
import pdb
# pdb.set_trace()
import csv
from os import listdir
from os.path import isfile, join
import re
from enum import Enum
from collections import Counter
import math

class Category(Enum):
    TRANSITION_AND_NEW_GOVERNMENT = 1
    INTERNAL_AFFAIRS = 2
    FOREIGN_AFFAIRS = 3
    ELECTION_RESULTS_AND_RECOUNTS = 4
    ELECTION_LEGAL_AFFAIRS = 5
    NA = 6


class TfIdf:
    def __init__(self, input_dir):
        self.dfs = []
        self.get_dfs_from(input_dir)
        self.df = pd.concat(self.dfs)
        self.df.astype({'coding': 'int32'}).dtypes
        
    def get_dfs_from(self, input_dir):
        files = [(join(input_dir, f)) for f in listdir(input_dir)]
        df = pd.read_csv('./data/labelling/label_slice_0.csv')
        self.dfs.append(df)
        df = pd.read_csv('./data/labelling/label_slice_2.csv')
        self.dfs.append(df)
        print(df.info())



    # def get_dfs_from(self, input_dir):
    #     files = [(join(input_dir, f)) for f in listdir(input_dir)]
    #     for f in files:
    #         df = pd.read_csv(f)
    #         self.dfs.append(df)
            


    def sanitize_title(self, title_list):
        title = []
        for phrase in title_list:
            pattern = r'\[.*?\]'
            no_sq_brackets = re.sub(pattern, '', phrase)
            pattern = r'\w*<.*?>\w*'
            no_unicode = re.sub(pattern, ' ', no_sq_brackets)
            pattern = r'\w+\'\w*'
            no_abbrev = re.sub(pattern, ' ', no_unicode)
            pattern = r'[^a-zA-Z]'
            no_alpha = re.sub(pattern, ' ', no_abbrev)
            no_double_space = re.sub(' +', ' ', no_alpha.strip())
            title.append(''.join(no_double_space))
        return title

    def create_raw_word_list(self, sanitized_str):
        word_list = " ".join(sanitized_str).split(" ")
        sorted_word_list = sorted(word_list)
        return sorted_word_list

    def calculate(self, methodc):
            wdict = self.compute_words_dict_per_cateogy()
            res = {}
            if (methodc == 1):
                res = self.compute_local(wdict)
            return res

    def compute_words_dict_per_cateogy(self):
        # df1 = self.df[self.df.isna().any(axis=1)]
        # print(df1)

        grouped = self.df.groupby(self.df.coding)
        ran_max = len(list(Category)) + 1
        df_rows = len(self.df.index)
        local_count = {}
        for i in range(1, ran_max):
            df = grouped.get_group(i)
            sanitized_str = self.sanitize_title(df['title'].to_list())

            raw_word_list = self.create_raw_word_list(sanitized_str)
            raw_word_list = list(map(str.lower, raw_word_list))
            frequency = Counter(raw_word_list)
            
            words_diff = raw_word_list
            ranked_words = {}
            for x in words_diff:
                if (x != ""):
                    ranked_words[x] = frequency[x]
            sorted_ranked = Counter(ranked_words)
            sorted_ranked = dict(sorted_ranked)
            local_count[Category(i).name] = sorted_ranked
        return local_count 

    def compute_local(self, wcount):
        total_n = {}
        for catergory in wcount:
            cat_dict = wcount[catergory]
            for w in cat_dict:
                total_n[w] = 1 + total_n.get(w, 0) 
        total_topics = len(list(Category))
        calculated_idf = {}
        for w in total_n:
            calculated_idf[w] = math.log(total_topics / (total_n[w]))


        cat_freq = {}
        res = {}
        for cat in wcount:
            cat_dict = wcount[cat]
            tmp = {}
            for words_key in cat_dict:
                tmp[words_key] = cat_dict[words_key] * calculated_idf[words_key]
            
            # res_idf = dict(Counter(tmp))
            res_idf = dict(Counter(tmp).most_common(10))
            # res[cat] = list(res_idf.keys())
            res[cat] = res_idf
        return res




        

