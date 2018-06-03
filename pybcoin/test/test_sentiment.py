"""
    Test cases for SentimenetAnalyzer module.
"""

from unittest import TestCase

import os
import pandas as pd
from configparser import SafeConfigParser

from pybcoin.SentimentAnalyzer.sentiment_scorer import SentimentAnalyzer
from utils.pre_processing import pre_process_data, create_word_cloud


class SentimenetAnalyzerTest(TestCase):

    def setUp(self):
        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.collector = SentimentAnalyzer(self.config)
        self.text = ['neo', 'bitcoin', 'bitcoin', 'fork']
        self.date = ['22/05/2018']

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
                                     'tweets_sentiment.csv')
        flag = test_sentiment.empty
        self.assertEqual(flag, False)

    def test_sentiment_column_names(self):

        """
        Checks that twitter csv has correct column names.
        """
        self.collector.sentiment_scorer(keyword='tweets')
        test_col_names = pd.read_csv(self.collector.path +
                                     'tweets_sentiment.csv').columns
        self.assertEqual(sorted(test_col_names),['Date', 'neg_count', 'pos_count'])

    def test_sentiment_wordcloud(self):

        """
        Checks that wordcloud is generated.
        """
        create_word_cloud(self.text,self.date)
        self.assertEqual(os.path.isfile('./pybcoin/test/data/' +
                                        'date_22-05-2018.png'), False)
