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
from enum import Enum


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
        # df = pd.read_csv('./data/labelling/label_slice_2.csv')
        # self.dfs.append(df)
        print(df.info())



    # def get_dfs_from(self, input_dir):
    #     files = [(join(input_dir, f)) for f in listdir(input_dir)]
    #     for f in files:
    #         df = pd.read_csv(f)
    #         self.dfs.append(df)
    #         print(df.info())


    def calculate(self):
        df1 = self.df[self.df.isna().any(axis=1)]
        print(df1)
        grouped = self.df.groupby(self.df.coding)
        ran_max = len(list(Category)) + 1
        for i in range(1, ran_max):
            print(grouped.get_group(i))

