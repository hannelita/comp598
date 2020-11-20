import os, sys
from pathlib import Path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import pandas as pd
import json
from datetime import date, datetime, timezone
import requests
import pdb
# pdb.set_trace()
from dotenv import load_dotenv
base = Path(__file__).parents[3] / '.env'
load_dotenv(dotenv_path=base)



DEFAULT_CHUNK_SIZE = 100


class Elections:
    def __init__(self, dest_file, num_posts):
        self.dest_file = dest_file
        self.num_posts = num_posts
        

    def authenticate(self, endpoint='/api/v1/me', payload={}):
        base_url = 'https://www.reddit.com/'
        data = {'grant_type': 'password', 'username': os.getenv("REDDIT_USERNAME"), 'password': os.getenv("REDDIT_PWD")}
        auth = requests.auth.HTTPBasicAuth(os.getenv("REDDIT_API_CLIENT_ID"), os.getenv("REDDIT_API_CLIENT_SECRET"))
        r = requests.post(base_url + 'api/v1/access_token',
                          data=data,
                          headers={'user-agent': f'{os.getenv("APP_NAME")} by {os.getenv("REDDIT_USERNAME")}'},
                          auth=auth)
        d = r.json()
        token = 'bearer ' + d['access_token']
        base_url = 'https://oauth.reddit.com'
        headers = {'Authorization': token, 'User-Agent': f'{os.getenv("APP_NAME")} by {os.getenv("REDDIT_USERNAME")}'}
        response = requests.get(base_url + endpoint, headers=headers, params=payload)
        return response


    def fetch_posts(self, subreddit, api_endpoint):
        print(f'Collecting posts for: {subreddit}')
        responses = []
        after_last = None
        if ((self.num_posts % 100) == 0):
            to_iterate = (self.num_posts // DEFAULT_CHUNK_SIZE)
        else:
            to_iterate = (self.num_posts // DEFAULT_CHUNK_SIZE) + 1
        for i in range(to_iterate):
            limit = DEFAULT_CHUNK_SIZE
            if (((i+1) * DEFAULT_CHUNK_SIZE) > self.num_posts):
                limit = self.num_posts % DEFAULT_CHUNK_SIZE

            endpoint = f'{subreddit}/{api_endpoint}'
            print(f'Collecting data from {endpoint}, pass {i}')
            if after_last is not None:
                payload = {'limit': limit, 'after': after_last}
            else:
                payload = {'limit': limit}
            response = self.authenticate(endpoint, payload)
            if response.status_code == 200:
                json_data = response.json()
                responses.append(json_data)
                posts = json_data.get('data', {}).get('children', [])
                if posts[-1] is not None:
                    after_last = posts[-1].get('data', {}).get('name', "")
        self.dump_to_file(responses)
            

    def dump_to_file(self, responses):
        with open(self.dest_file, 'w+') as fp:
            for json_raw_response in responses:
                posts = json_raw_response.get('data', {}).get('children', [])        
                for p in posts: 
                    json.dump(p, fp)
                    fp.write("\n")

