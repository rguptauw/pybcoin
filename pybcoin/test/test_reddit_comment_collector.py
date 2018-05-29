"""
    Test cases for RedditDataCollector module.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from configparser import SafeConfigParser

from pybcoin.DataCollector.reddit_comment_collector import RedditDataCollector


class RedditDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = RedditDataCollector(self.config)

    """
    Test function for fetch_reddit_comments.
    Asserts the shape of the returned dataframe.
    """
    @patch('pybcoin.DataCollector.reddit_comment_collector.requests.get')
    def test_fetch_reddit_comments(self, mock_get):
        response = {"hits": {"hits": [{"_source": {
            "body": "Bitcoin is awesome!",
            "created_utc": 1526955295
        }
        },
            {
            "_source": {
                "body": "I am rich!",
                "created_utc": 1526956811
            }
        }]
        }}
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = response
        data = self.collector.fetch_reddit_comments()
        self.assertEqual(data.shape, (2, 2))
