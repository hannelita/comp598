# COMP 598 final project



### Requirements
`pip install python-dotenv`

### Collecting data

Run `cp .env.example .env` and provide the appropriate information of your Reddit user.
There are 5 values you need to input. These values refer to the Reddit API.
Run `python scripts/collect_posts.py -o data/20201120_new_politics.json  -subreddit "/r/politics" -endpoint new -numposts 400` to collect the the posts. Modify the parameters accordingly.

<!-- python scripts/collect_posts.py -o data/20201104_politics.json "/r/politics" -->

To filter the content, run `python scripts/filter_mentions.py -o ./data/filtered/` , where `-o` is the output directory. You can specify `-inputdir` to point to the directory containing the posts to be filtered. The default is set to `./data/new/` .

On `scripts/filter_mentions.py`, if you uncomment line #30, you'll get the sample files generated for open coding. 


To remove duplicates, run 
`python scripts/prepare_filtred_mentions.py -o ./data/unique -inputdir ./data/filtered`. The default `inputdir` is `./data/filtered`

To generate the final version for labelling, ` python scripts/create_csv_labelling.py -o ./data/labelling/`. The default `inputdir` is `./data/unique/`

Valid entries
```
Trump won
hi biden
aaa Biden
Biden2020
anti-trump
abctrump
THE PRES TRUMP
TRUMPOO
tRuMp
biden
BiDeN2020
abiden
biden-123
anti-biden

```

Invalid entries
```
9trump9
9biden9
```

Categories and Enumeration
```
1 transition_and_new_government
2 internal_affairs
3 foreign_affairs
4 election_results_and_recounts
5 election_legal_affairs
6 NA
```


For TF-IDF
```
python scripts/compute_tf_idf.py -o ./data/results/out1.json
```