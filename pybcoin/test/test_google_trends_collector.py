"""
    Test cases for GTrendsDataCollector module.
"""

from unittest import TestCase
from unittest.mock import patch

import pytrends
from configparser import SafeConfigParser

from pybcoin.DataCollector.google_trends_collector import GTrendsDataCollector


class GTrendsDataCollectorTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = GTrendsDataCollector(self.config)

    """
    Test function for fetch_trends.
    Asserts whether the api function is called.
    """
    @patch.object(pytrends.request.TrendReq, 'build_payload',
                  autospec=True)
    @patch.object(pytrends.request.TrendReq, 'interest_over_time',
                  autospec=True)
    def test_fetch_trends(self, mock_build_payload,
                          mock_interest_over_time):
        self.collector.fetch_trends()
        self.assertEqual(mock_interest_over_time.call_count, 1)
