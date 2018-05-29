"""
    Test cases for BtcDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

import quandl
from configparser import SafeConfigParser
import forex_python.converter


from pybcoin.DataCollector.btc_data_collector import BtcDataCollector


class BtcDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = BtcDataCollector(self.config)

    """
    Test function for fetch_tweets.
    Asserts the shape of the returned dataframe.
    """
    @patch.object(forex_python.bitcoin.BtcConverter, 'get_previous_price',
                  autospec=True)
    def fetch_btc_price(self, mock_get_previous_price):
        self.collector.fetch_btc_price()
        mock_get_previous_price.assert_called_once()

    @patch('pybcoin.DataCollector.btc_data_collector.requests.get')
    def test_fetch_tweet_counts(self, mock_get):
        self.collector.fetch_tweet_counts()
        mock_get.assert_called_once()

    @patch.object(quandl, 'get', autospec=True)
    def test_fetch_transaction_volume(self, mock_get):
        self.collector.fetch_transaction_volume()
        mock_get.assert_called_once()
