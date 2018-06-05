"""
    Test cases for GTrendsDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

import pandas as pd

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
        self.response_dict = {
            'btc': pd.DataFrame([{'Date': '10/1/2017',
                                  'btc_price': 4394.6388}]
                                ).set_index('Date'),
            'count': pd.DataFrame([{'Date': '10/1/2017',
                                    'tweet_count': 56280}]
                                  ).set_index('Date'),
            'vol': pd.DataFrame([{'Date': '10/1/2017',
                                  'Value': 663214577.9}]
                                ).set_index('Date'),
            'gtrend': pd.DataFrame([{'Date': '10/1/2017',
                                     'btc': 81}]
                                   ).set_index('Date'),
            'forex': pd.DataFrame([{'Date': '10/1/2017',
                                    'forex_rate': 0.852369587}]
                                  ).set_index('Date'),
            'nyse': pd.DataFrame([{'Date': '10/1/2017',
                                   'NYA_Close': 12264.6649}]
                                 ).set_index('Date'),
            'oil': pd.DataFrame([{'Date': '10/1/2017',
                                  'oil_price': 54.6}]
                                ).set_index('Date'),
            'tweets': pd.DataFrame([{'Date': '10/1/2017',
                                     'text': 'Bitcoin, shooting to the moon'}]
                                   ),
            'reddit': pd.DataFrame([{'Date': '10/1/2017',
                                     'text': 'Bitcoin make me rich.'}])
        }

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
                                      mock_fetch_reddit_comments,
                                      mock_fetch_tweets,
                                      mock_fetch_oil_price,
                                      mock_fetch_nyse_index,
                                      mock_fetch_usd_exrate,
                                      mock_fetch_trends,
                                      mock_fetch_transaction_volume,
                                      mock_fetch_tweet_counts,
                                      mock_fetch_btc_price,
                                      ):
        mock_fetch_btc_price.return_value = self.response_dict['btc']
        mock_fetch_tweet_counts.return_value = self.response_dict['count']
        mock_fetch_transaction_volume.return_value = self.response_dict['vol']
        mock_fetch_trends.return_value = self.response_dict['gtrend']
        mock_fetch_usd_exrate.return_value = self.response_dict['forex']
        mock_fetch_nyse_index.return_value = self.response_dict['nyse']
        mock_fetch_oil_price.return_value = self.response_dict['oil']
        mock_fetch_tweets.return_value = self.response_dict['tweets']
        mock_fetch_reddit_comments.return_value = self.response_dict['reddit']
        val = self.collector.data_collection_pipeline()
        self.assertEquals(val, True)
