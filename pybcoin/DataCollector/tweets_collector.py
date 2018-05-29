"""
    Module name: tweets_collector
    Description: Module for collecting tweets with hashtag
    bitcoin for performing sentiment analysis.
"""

from datetime import datetime, timedelta
import logging
import tweepy
import pandas as pd


class TwitterDataCollector(object):

    """
        The object for retrieving daily tweets with #bitcoin
        A maximum of 10000 tweets will retrieved.
            :member attributes: logger: logger instance
                                app_name: App name

            :member functions:  fetch_tweets

    """

    def __init__(self, config):
        self.logger = logging.getLogger('simpleExample')
        self.consumer_key = config['Twitter']['consumer_key']
        self.consumer_secret = config['Twitter']['consumer_secret']
        self.access_token = config['Twitter']['access_token']
        self.access_token_secret = config['Twitter']['access_token_secret']

    def fetch_tweets(self, params=None):
        """
            Method to fetch tweets with bitcoin hashtag.
            The max limit for the number of tweets is 10000.
            : param self
            : return bitcoin_tweets(pandas DataFrame)
                     error_val(int)
        """
        error_val = -1
        try:
            day_count = 1
            today = datetime.now()
            start_date = today - timedelta(days=day_count)
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            api = tweepy.API(auth, wait_on_rate_limit=True)
            bitcoin_tweets = pd.DataFrame(columns=['Date', 'text'])
            for tweet in tweepy.Cursor(
                    api.search, q="#bitcoin", count=100,
                    lang="en",
                    since=start_date.strftime("%Y-%m-%d"),
                    until=today.strftime("%Y-%m-%d")).items(10000):
                bitcoin_tweets = bitcoin_tweets.append({
                    'Date': tweet.created_at.date(),
                    'text': tweet.text.encode('utf-8')},
                    ignore_index=True)
            return bitcoin_tweets
        except Exception as e:
            # self.logger.error(e)
            print(e)
            return error_val
