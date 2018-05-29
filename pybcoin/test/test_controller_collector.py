"""
    Test cases for GTrendsDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

from pybcoin.DataCollector.btc_data_collector import BtcDataCollector
from pybcoin.DataCollector.google_trends_collector import GTrendsDataCollector
from pybcoin.DataCollector.market_data_collector import MarketDataCollector
from pybcoin.DataCollector.reddit_comment_collector import RedditDataCollector
from pybcoin.DataCollector.tweets_collector import TwitterDataCollector
from pybcoin.DataCollector.controller_collector import ControllerCollector


class ControllerCollectorTest(TestCase):

    def setUp(self):
        self.collector = ControllerCollector('./pybcoin/config/'
                                             'config_test.ini')

    """
    Test function for fetch_trends.
    Asserts whether the api function is called.
    """
    @patch.object(BtcDataCollector, 'fetch_btc_price',
                  autospec=True)
    @patch.object(BtcDataCollector, 'fetch_tweet_counts',
                  autospec=True)
    @patch.object(BtcDataCollector, 'fetch_transaction_volume',
                  autospec=True)
    @patch.object(GTrendsDataCollector, 'fetch_trends',
                  autospec=True)
    @patch.object(MarketDataCollector, 'fetch_usd_exrate',
                  autospec=True)
    @patch.object(MarketDataCollector, 'fetch_nyse_index',
                  autospec=True)
    @patch.object(MarketDataCollector, 'fetch_oil_price',
                  autospec=True)
    @patch.object(TwitterDataCollector, 'fetch_tweets',
                  autospec=True)
    @patch.object(RedditDataCollector, 'fetch_reddit_comments',
                  autospec=True)
    def test_data_collection_pipeline(self,
                                      mock_fetch_btc_price,
                                      mock_fetch_tweet_counts,
                                      mock_fetch_transaction_volume,
                                      mock_fetch_trends,
                                      mock_fetch_usd_exrate,
                                      mock_fetch_nyse_index,
                                      mock_fetch_oil_price,
                                      mock_fetch_tweets,
                                      mock_fetch_reddit_comments
                                      ):
        val = self.collector.data_collection_pipeline()
        self.assertEquals(val, True)
