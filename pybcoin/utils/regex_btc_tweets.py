#import pandas as pd
import pandas as pd
import os
import re
import datetime
import unicodedata


#setting directory
os.chdir('/home/rohit/Desktop/crypto_tweet')

#reading the data
data_frame = pd.read_csv('btc_tweets.txt', sep = "],", header=None, engine = 'python')

#defining the function to extract date
def date_func(pass_row):
    try:
        var_str = pass_row.to_string()
        pattern = r'"([A-Za-z0-9_\./\\-]*)"'
        m = re.search(pattern, var_str)
        date_str = m.group()
        date_str = date_str.replace('"', '')
        date_str = datetime.datetime.strptime(date_str, '%Y/%m/%d').date()
        return date_str
    except ValueError:
        print ('Date needs to be in a %Y/%m/%d format')
    except AttributeError:
        print ('Date needs to be supplied within double quotes as part of a string')

#defining the function to extract num tweets
#defining the function to extract num tweets
def num_tweets_func(pass_row):
    try:
        num_str = pass_row.to_string()
        num_str = re.findall(r',(\w+)', num_str)
        num_str = num_str[0]
        if num_str == 'null':
            num_str = 0
        else:
            num_str = int(num_str.encode('ascii'))
        return num_str
    except:
        print ('Number of tweets to be supplied between commas in a string object')

#creating the final dataframe
dates_s = data_frame.apply(date_func)
tweets_s = data_frame.apply(num_tweets_func)
final_df = pd.concat([dates_s, tweets_s], axis=1).reset_index()
final_df.columns = ['index','date','btc_tweets'] 
final_df = final_df[['date','btc_tweets']]