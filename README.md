# COMP 598 final project



### Requirements
`pip install python-dotenv`

### Collecting data

Run `cp .env.example .env` and provide the appropriate information of your Reddit user.
There are 5 values you need to input. These values refer to the Reddit API.
Run `python scripts/collect_posts.py -o data/20201120_new_politics.json  -subreddit "/r/politics" -endpoint new -numposts 400` to collect the the posts. Modify the parameters accordingly.

<!-- python scripts/collect_posts.py -o data/20201104_politics.json "/r/politics" -->