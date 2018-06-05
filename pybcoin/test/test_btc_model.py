"""
Test cases for Modeling module.

Classes defined:
ModelForecastTest

Function available:
test_time_value()
test_reg_value()
test_final_value()

Module consists of 3 tests: to check for the return values from all the
functions, and their expected values.
"""

# importing packages
import unittest
from configparser import SafeConfigParser
from pybcoin.ModelForecast.btc_model import BtcModelPrediction


class ModelForecastTest(unittest.TestCase):

    """
        Defining a class that contains all tests to be run.
    """

    def setUp(self):
        """
            Defining a setup function that reads the configuration file,
            and initialize an instance of the object.
        """

        self.config = SafeConfigParser()
        self.config.read('./pybcoin/config/config_test.ini')
        self.sample = BtcModelPrediction(self.config)

    def test_time_value(self):
        """
            Defining a function that tests the return value type from
            time-series	prediction function.
        """
        time_res = self.sample.time_prediction()
        time_res = time_res[0]
        res = isinstance(time_res, float)
        self.assertTrue(res)

    def test_reg_value(self):
        """
            Defining a function that tests the return value type from
            regression function.
        """
        reg_res = self.sample.linear_prediction()
        res = isinstance(reg_res, float)
        self.assertTrue(res)

    def test_final_value(self):
        """
            Defining a function that tests the final return value, its type
            and the possible range of values.
        """
        final_res = self.sample.final_prediction()
        res = (isinstance(final_res, float) and
               (final_res > 0.00 and final_res < 0.99))
        self.assertTrue(res)
