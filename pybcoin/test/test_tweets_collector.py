"""
    Test cases for TwitterDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

import tweepy
from configparser import SafeConfigParser

from pybcoin.DataCollector.tweets_collector import TwitterDataCollector


class TwitterDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = TwitterDataCollector(self.config)

    """
    Test function for fetch_tweets.
    Asserts whether the api call is triggered or not.
    """
    @patch.object(tweepy, 'Cursor', autospec=True)
    def test_fetch_tweets(self, mock_get_tweets):
        self.collector.fetch_tweets()
        mock_get_tweets.assert_called_once()
