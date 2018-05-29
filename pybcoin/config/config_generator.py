"""
    Module name: config_generator
    Description: Script to generate the config file for the application.
    Be careful while altering the urls as the module implementations
    are specific to the structure of the retrieved data.
"""

from configparser import SafeConfigParser

api_uri = ('https://elastic.pushshift.io/rc/comments/_search?'
           'source={"query":{"bool":{"must":[{"simple_query_string":{'
           '"query":"bitcoin|btc|crypto","fields":["body"],'
           '"default_operator":"and"}}],"filter":[{"range":{"created_utc":'
           '{"gte":START_UTC,"lte":END_UTC}}},'
           '{"terms":{"subreddit":["bitcoin","btc","cryptocurrency"]}}],'
           '"should":[],"must_not":[]}},"size":10000,'
           '"sort":{"created_utc":"desc"}}')

tweet_count_url = 'https://bitinfocharts.com/comparison/tweets-btc.html'

config = SafeConfigParser()
config.read('config.ini')
config.add_section('Twitter')
config.set('Twitter', 'consumer_key', '')
config.set('Twitter', 'consumer_secret','')
config.set('Twitter', 'access_token','')
config.set('Twitter', 'access_token_secret','')
config.set('Twitter', 'tweet-count-url', tweet_count_url)

config.add_section('Reddit')
config.set('Reddit', 'api-uri', api_uri)
config.set('Reddit', 'json_path','./pybcoin/test/data/output.json')

config.add_section('Forecast')
config.set('Forecast', 'in_path_btc', './pybcoin/test/data/btc/')
config.set('Forecast', 'in_path_comm','./pybcoin/test/data/commodity/')
config.set('Forecast', 'in_path_gtrends','./pybcoin/test/data/gtrends/')
config.set('Forecast', 'out_path','./pybcoin/test/data/')

config.add_section('Quandl')
config.set('Quandl', 'quandl-key', '')

with open('./pybcoin/config/config_test.ini', 'w') as f:
    config.write(f)
