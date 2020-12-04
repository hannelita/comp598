#!/usr/bin/python3

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import argparse
import json
import pprint
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


from src.results.plotgen import PlotGen

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output directory name (ends with / )')
parser.add_argument('-inputdir', help='Input directory to filter posts', required=False, default='./data/results/')

args = parser.parse_args()

DEST = '{}'.format(args.o)
INPUT_DIR = '{}'.format(args.inputdir)

def generate_json_output(res):
    with open(DEST, 'w+') as fp:
        json.dump(res, fp)

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def plot_chart_by_category_candidates(category, std_tf_idf, trump, biden, words, fname, classifier):
    n_groups = 10

    # create plot
    fig, ax = plt.subplots()
    fig.set_size_inches(14.5, 9.5)
    bar_width = 0.3
    opacity = 0.8

    r1 = np.arange(len(words))
    # r1 = np.arange(len(bars1))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]


    rects1 = ax.bar(r1, std_tf_idf, bar_width,
    alpha=opacity,
    color='g',
    label='Standard TF-IDF')
    

    rects2 = ax.bar(r2, trump, bar_width,
    alpha=opacity,
    color='r',
    label='Trump')

    rects3 = ax.bar(r3, biden, bar_width,
    alpha=opacity,
    color='b',
    label='Biden')

    ax.autoscale(enable=True, axis="both", tight=False)

    ax.set_ylabel('TF-IDF')
    ax.set_title(f'TF-IDF by {classifier} for category {category}')
    ax.set_xticks(r1)
    ax.set_xticklabels(words, Rotation=90)
    ax.legend()

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    fig.tight_layout()
    # plt.show() 
    plt.savefig(f'./data/charts/{fname}.png')
    

def main():
    print(f'Input files from {INPUT_DIR}')
    
    plotter = PlotGen(INPUT_DIR)
    default_local = {}
    with open('./data/results/out_local1.json', 'r') as fp:
        default_local = json.load(fp)
    for key in default_local.keys():
        most_com = dict(Counter(default_local[key]).most_common(10))
        default_local[key] = most_com
    biden_local = plotter.compute('./data/results/out_local1.json', 1, candidate='m_biden')
    trump_local = plotter.compute('./data/results/out_local1.json', 1, candidate='m_trump')
      
    dlk = list(default_local.keys())
    for key in dlk:
        std =  [float(i) for i in list(map("{:.2f}".format, (list(default_local.get(key, {}).values()))))]
        biden = [float(i) for i in list(map("{:.2f}".format, (list(biden_local.get(key, {}).values())) ))]
        trump = [float(i) for i in list(map("{:.2f}".format, (list(trump_local.get(key, {}).values())) ))]
        words = list(default_local.get(key, {}).keys())
        fname = str(key) + "_candidates" + "_method_1_local"
        plot_chart_by_category_candidates(key, std, trump, biden, words, fname, "candidate")
    
    politics_local = plotter.compute('./data/results/out_local1.json', 1, subreddit='politics')
    conservative_local = plotter.compute('./data/results/out_local1.json', 1, subreddit='Conservative')

    for key in dlk:
        std =  [float(i) for i in list(map("{:.2f}".format, (list(default_local.get(key, {}).values()))))]
        politics = [float(i) for i in list(map("{:.2f}".format, (list(politics_local.get(key, {}).values())) ))]
        conservative = [float(i) for i in list(map("{:.2f}".format, (list(conservative_local.get(key, {}).values())) ))]
        words = list(default_local.get(key, {}).keys())
        fname = str(key) + "_subreddit" + "_method_1_local"
        plot_chart_by_category_candidates(key, std, conservative, politics, words, fname, "subreddit")
    

    default_global = {}
    with open('./data/results/out_global1.json', 'r') as fp:
        default_global = json.load(fp)
    for key in default_global.keys():
        most_com = dict(Counter(default_global[key]).most_common(10))
        default_global[key] = most_com

    default_global.pop('OTHER', None)
    biden_global = plotter.compute('./data/results/out_global1.json', 2, candidate='m_biden')
    trump_global = plotter.compute('./data/results/out_global1.json', 2, candidate='m_trump')

    dlk = list(default_global.keys())
    for key in dlk:
        std =  [float(i) for i in list(map("{:.2f}".format, (list(default_global.get(key, {}).values()))))]
        biden = [float(i) for i in list(map("{:.2f}".format, (list(biden_global.get(key, {}).values())) ))]
        trump = [float(i) for i in list(map("{:.2f}".format, (list(trump_global.get(key, {}).values())) ))]
        words = list(default_global.get(key, {}).keys())
        fname = str(key) + "_candidates" + "_method_2_global"
        plot_chart_by_category_candidates(key, std, trump, biden, words, fname, "candidate")

    politics_global = plotter.compute('./data/results/out_global1.json', 2, subreddit='politics')
    conservative_global = plotter.compute('./data/results/out_global1.json', 2, subreddit='Conservative')

    for key in dlk:
        std =  [float(i) for i in list(map("{:.2f}".format, (list(default_global.get(key, {}).values()))))]
        politics = [float(i) for i in list(map("{:.2f}".format, (list(politics_global.get(key, {}).values())) ))]
        conservative = [float(i) for i in list(map("{:.2f}".format, (list(conservative_global.get(key, {}).values())) ))]
        words = list(default_global.get(key, {}).keys())
        fname = str(key) + "_subreddit" + "_method_2_global"
        plot_chart_by_category_candidates(key, std, conservative, politics, words, fname, "subreddit")
    
    
    
    

if __name__ == "__main__":
    main()