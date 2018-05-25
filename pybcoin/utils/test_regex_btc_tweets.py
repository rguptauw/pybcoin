import unittest
import regex_btc_tweets
import datetime
import pandas as pd

class TestCreateDF(unittest.TestCase):
    """ Defining a class that contains all tests that need to be run."""

    def test_date(self):
        string_c = pd.Series(['random_musing"2018/08/02"ends'])
        returned_res = regex_btc_tweets.date_func(string_c)
        res = isinstance(returned_res, datetime.date)
        self.assertTrue(res)

    def test_tweets(self):
    	string_c = pd.Series(['random_musing,099,ends'])
    	returned_res = regex_btc_tweets.num_tweets_func(string_c)
        res = isinstance(returned_res, int)
        self.assertTrue(res)

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestCreateDF)
_ = unittest.TextTestRunner().run(SUITE)
