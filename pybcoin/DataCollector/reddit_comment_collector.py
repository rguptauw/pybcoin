"""
    Module name: reddit_comment_collector
    Description: Module for collecting reddit comments related to bitcoin
    and cryptocurrency for performing sentiment analysis.
"""

from datetime import datetime, timedelta
import time
import json
import logging

import requests
import pandas as pd


class RedditDataCollector(object):

    """
        The object for retrieving daily bitcoin related comments
        from Reddit.The comments are retrieved accross all subreddits.
            :member attributes: logger: logger instance

            :member functions:  fetch_reddit_comments

    """

    def __init__(self, config):
        self.logger = logging.getLogger('simpleExample')
        self.api_uri = config['Reddit']['api-uri']
        self.output_path = config['Reddit']['data_path']

    def fetch_reddit_comments(self):
        """
            Method to fetch the bitcoin related comments from reddit.
            The max limit for the number of comments is 10000
            the CoinDesk index.
            : param self
            : return reddit_comments(DataFrame)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 1
            today = datetime.now().replace(hour=0, minute=0,
                                           second=0, microsecond=0)
            for single_date in (today - timedelta(n)
                                for n in range(day_count)):
                # self.logger.error('Fetching Reddit comments for:'
                #                   , single_date)
                single_date_utc = single_date.timetuple()
                single_date_utc = time.mktime(single_date_utc)
                url = self.api_uri
                url = url.replace('START_UTC',
                                  str(int(single_date_utc - 86400)))
                url = url.replace('END_UTC', str(int(single_date_utc)))
                res = requests.get(url)
                data = res.json()
                data = data['hits']['hits']
                comments = []
                for meta_data in data:
                    comment = meta_data['_source']
                    comments.append({
                                    'text': comment['body'],
                                    'Date': comment['created_utc']
                                    })
                with open(self.output_path + 'output.json',
                          'w+', encoding='utf-8') as f:
                    json.dump(comments, f)
            reddit_comments = pd.read_json(self.output_path + 'output.json',
                                           orient='records')
            reddit_comments['Date'] = (today - timedelta(1)).date()
            return reddit_comments
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val
