"""
    Test cases for SentimenetAnalyzer module.
"""

from unittest import TestCase

import os
import pandas as pd
from configparser import SafeConfigParser

from pybcoin.SentimentAnalyzer.sentiment_scorer import SentimentAnalyzer
from utils.pre_processing import create_word_cloud


class SentimenetAnalyzerTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = SentimentAnalyzer(self.config)
        self.text = ['neo', 'bitcoin', 'bitcoin', 'fork']
        self.date = ['22/05/2016']
        self.path = './pybcoin/test/data/'
        self.tweets_path = 'tweets_sentiment.csv'
        self.image_path = './pybcoin/static/date_22-05-2016.png'
        self.static_path = './pybcoin/static/'
        self.image_name = 'date_22-05-2016.png'

    """
    Test function for text sentiments.
    Checks that csv is written on test folder.
    """

    def test_sentiment_score(self):

        """
        Checks that twitter csv is written on test folder is non empty.
        """
        self.collector.sentiment_scorer(keyword='tweets')
        test_sentiment = pd.read_csv(self.collector.path +
                                     self.tweets_path)
        flag = test_sentiment.empty
        self.assertEqual(flag, False)
        os.remove(self.image_path)

    def test_sentiment_column_names(self):

        """
        Checks that twitter csv has correct column names.
        """
        self.collector.sentiment_scorer(keyword='tweets')
        test_col_names = pd.read_csv(self.collector.path +
                                     self.tweets_path).columns
        self.assertEqual(sorted(test_col_names),
                         ['Date', 'Negative', 'Positive'])
        os.remove(self.image_path)

    def test_sentiment_wordcloud(self):

        """
        Checks that wordcloud is generated.
        """
        create_word_cloud(self.text, self.date)
        self.assertEqual(os.path.isfile(self.static_path +
                                        self.image_name), True)
        os.remove(self.image_path)
