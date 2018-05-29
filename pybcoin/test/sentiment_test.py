"""
    Test cases for SentimenetAnalyzer module.
"""

from unittest import TestCase

import pandas as pd
from configparser import SafeConfigParser

from pybcoin.SentimentAnalyzer.sentiment_scorer import SentimentAnalyzer


class SentimenetAnalyzerTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = SentimentAnalyzer(self.config)

    """
    Test function for text sentiments.
    Checks that csv is written on test folder.
    """

    def test_sentiment_score(self):

        """
        Checks that twitter csv is written on test folder.
        """
        self.collector.sentiment_scorer(keyword='tweets')
        test_sentiment = pd.read_csv(self.collector.path +
                                     'tweets_sentiment.csv')
        flag = test_sentiment.empty
        self.assertEqual(flag, False)
