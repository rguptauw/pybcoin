# This module is to be used to generate the GTrends data file for select keywords

import pandas as pd
import time

from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_lists = ["btc", "bitcoin", "btc usd", "btcusd", "cypto","cryptocurrency", "eth", "ethereum", "blockchain"]
date_range_list = ['2016-01-01 2016-03-31','2016-04-01 2016-06-30','2016-07-01 2016-09-30','2016-10-01 2016-12-31']
date_range_list.extend(['2017-01-01 2017-03-31','2017-04-01 2017-06-30','2017-07-01 2017-09-30','2017-10-01 2017-12-31'])
date_range_list.extend(['2018-01-01 2018-03-31','2018-04-01 2018-06-30'])

df_final = pd.DataFrame()
for wordlist in kw_lists:
    df_temp = pd.DataFrame()
    for date in date_range_list:
        pytrends.build_payload([wordlist], cat=0, timeframe=date, geo='', gprop='')
        df_temp = pd.concat([df_temp,pytrends.interest_over_time()],axis=0)
    df_final = pd.concat([df_final,df_temp.iloc[:,:-1]],axis=1)

df_final.to_csv("GTrendsData.csv")