"""
    Test cases for MarketDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

import quandl
from configparser import SafeConfigParser
import forex_python.converter

from pybcoin.DataCollector.market_data_collector import MarketDataCollector


class MarketDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = MarketDataCollector()

    """
    Test function for test_fetch_usd_exrate.
    Asserts whether the api is called.
    """
    @patch.object(forex_python.converter.CurrencyRates, 'get_rate',
                  autospec=True)
    def test_fetch_usd_exrate(self, mock_fetch_usd_exrate):
        self.collector.fetch_usd_exrate()
        self.assertEqual(mock_fetch_usd_exrate.call_count, 1)

    """
    Test function for test_fetch_oil_price.
    Asserts whether the api is called.
    """

    @patch.object(quandl, 'get', autospec=True)
    def test_fetch_oil_price(self, mock_get):
        self.collector.fetch_oil_price()
        self.assertEqual(mock_get.call_count, 1)

    """
    Test function for test_fetch_nyse_index.
    Asserts whether the api is called.
    """

    @patch('pybcoin.DataCollector.market_data_collector.get_prices_data')
    def test_fetch_nyse_index(self, mock_get_prices_data):
        self.collector.fetch_nyse_index()
        self.assertEqual(mock_get_prices_data.call_count, 1)
