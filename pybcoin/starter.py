"""
    Module name: starter
    Description: Script to trigger the data flow and start the ui server.
"""

import os
import sys

import psutil
import time
import subprocess
from configparser import SafeConfigParser

__directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__directory + "/..")
sys.path.append(__directory + "/../..")

from pybcoin.DataCollector.controller_collector import ControllerCollector  # noqa
from pybcoin.SentimentAnalyzer.sentiment_scorer import SentimentAnalyzer  # noqa
from pybcoin.ModelForecast.btc_model import BtcModelPrediction  # noqa


def start_data_collection(config):
    try:
        controller = ControllerCollector(config)
        controller.data_collection_pipeline()
    except Exception as e:
        # self.logger.error(e)
        print(e)


def start_sentiment_analyzer(config):
    try:
        analyzer = SentimentAnalyzer(config)
        analyzer.sentiment_scorer(keyword='tweets')
        analyzer.sentiment_scorer(keyword='reddit_comments')
    except Exception as e:
        # self.logger.error(e)
        print(e)


def start_forecast(config):
    try:
        model = BtcModelPrediction(config)
        model.final_prediction()
    except Exception as e:
        # self.logger.error(e)
        print(e)


def kill(pid):
    process = psutil.Process(pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


if __name__ == "__main__":

    config_file = './pybcoin/config/config.ini'
    config = SafeConfigParser()
    config.read(config_file)

    while True:
        print('Collecting data...')
        start_data_collection(config_file)

        print('Starting sentiment analyzer...')
        start_sentiment_analyzer(config)

        print('Predicting the next 24hr movement...')
        start_forecast(config)

        p = subprocess.Popen('python pybcoin/home.py', shell=True)
        time.sleep(86400)
        kill(p.pid)
        time.sleep(10)
