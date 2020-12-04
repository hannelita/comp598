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
from src.results.tfidf import Category, OtherCategory, TfIdf


class PlotGen:
    def __init__(self, input_dir):
        self.files = []
        self.input_dir = input_dir
    

    def compute(self, idf_file, method=1, candidate=None, subreddit=None):
        most_common_w = {}
        with open(idf_file, 'r') as fp:
            most_common_w = json.load(fp)
        
        for key in most_common_w.keys():
            most_com = dict(Counter(most_common_w[key]).most_common(10))
            most_common_w[key] = most_com
        if (method == 1):
            df = pd.read_csv('./data/raw_dataset_csv/mentioned.csv')
        else:
            df_mention = pd.read_csv('./data/raw_dataset_csv/mentioned.csv')
            df_no_mention = pd.read_csv('./data/raw_dataset_csv/no_mention.csv')
            df = pd.concat([df_mention, df_no_mention])
        res = df

        if candidate is not None:
            res = df[df[candidate] == True]
            
        if subreddit is not None:
            res = df[df['subreddit'].str.contains(subreddit)]

        wcount = self.compute_words_dict_per_cateogy(res, most_common_w)
        proportional_res = self.compute_tfidf_ratio(wcount, most_common_w)
        proportional = {}
        for key in proportional_res.keys():
            proportional[key] = {}
            base_words = most_common_w[key]
            base_words = base_words.keys()
            for base_w in base_words:
                proportional[key][base_w] = proportional_res.get(key, {}).get(base_w, 0.0)
        return proportional


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
    

    def compute_words_dict_per_cateogy(self, df, base_tfidf):
        grouped = df.groupby(df.coding)
        
        ran_max = len(base_tfidf.keys()) + 1
        iterate = len(set(df['coding'].to_list())) + 1
        df_rows = len(df.index)
        local_count = {}
        for i in range(1, iterate):
            df1 = grouped.get_group(i)
            sanitized_str = self.sanitize_title(df1['title'].to_list())

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
            if (ran_max == 7):
                local_count[Category(i).name] = sorted_ranked
            else:
                local_count[OtherCategory(i).name] = sorted_ranked
        return local_count 

    def compute_tfidf_ratio(self, wcount, base_tfidf):
        ran_max = len(base_tfidf.keys())
        total_n = {}
        for catergory in wcount:
            cat_dict = wcount[catergory]
            for w in cat_dict:
                total_n[w] = 1 + total_n.get(w, 0)
        if (ran_max == 6):
            total_topics = len(list(Category))
        else:
            total_topics = len(list(OtherCategory))
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
            res_idf = dict(Counter(tmp))
            # res_idf = dict(Counter(tmp).most_common(10))
            res[cat] = res_idf
        return res


        

