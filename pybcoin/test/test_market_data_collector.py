"""
    Test cases for MarketDataCollector module.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

import nose
import quandl
from configparser import SafeConfigParser
import googlefinance.client as client
import forex_python.converter


from pybcoin.DataCollector.market_data_collector import MarketDataCollector

class MarketDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = MarketDataCollector()

    """
    Test function for fetch_tweets.
    Asserts the shape of the returned dataframe.
    """
    @patch.object(forex_python.converter.CurrencyRates,'get_rate',
                  autospec=True)
    def test_fetch_usd_exrate(self, mock_fetch_usd_exrate):
        self.collector.fetch_usd_exrate()
        mock_fetch_usd_exrate.assert_called_once()

    @patch.object(quandl,'get', autospec=True)
    def test_fetch_oil_price(self, mock_get):
        self.collector.fetch_oil_price()
        mock_get.assert_called_once()

    @patch('pybcoin.DataCollector.market_data_collector.get_prices_data')
    def test_fetch_nyse_index(self, mock_get_prices_data):
        self.collector.fetch_nyse_index()
        mock_get_prices_data.assert_called_once()
        