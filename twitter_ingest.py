#!/usr/bin/env python

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import os
import yaml
import boto3
import json
import logging
import datetime

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def setup_credentials():  
  try: 
   credentials = {
      'consumer_key' : os.environ['TWITTER_CONSUMER_KEY'],
      'consumer_secret' : os.environ['TWITTER_CONSUMER_SECRET'],
      'access_token' : os.environ['TWITTER_ACCESS_TOKEN'],
      'access_secret' : os.environ['TWITTER_ACCESS_SECRET']
    }
  except KeyError as e:
    sys.stderr.write('Environment variable is not set. Please set with: export %s="your-value"' %e.message)
    sys.exit(1)
  return credentials
  
def read_config_file():
  with open('config.yml', 'r') as fp:
    yaml_string = fp.read()
    config = yaml.load(yaml_string)
  return config

class TweetBuffer(object):
    def __init__(self, hashtag):
        self.tweets = []
        self.max_tweets = 1000
        self.hashtag = hashtag

    def add_tweet(self, tweet_json):
        self.tweets.append(tweet_json)
        if len(self.tweets) >= self.max_tweets:
            self.flush()

    def flush(self):
        s3_client = boto3.client('s3') 
        tweets = json.dumps(self.tweets)
        bucket_name = 'sarabi-twitter'
        key_name = '%s/%s-tweets-%s' %(self.hashtag, self.hashtag, datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        s3_client.put_object(Body=tweets, Bucket=bucket_name, Key=key_name)
        
class MyListener(StreamListener):

    def __init__(self, filepath, tweet_buffer):
        self.filepath = filepath 
        self.tweet_buffer = tweet_buffer
 
    def on_data(self, data):
        root.info('data received') 
        try:
          root.info('before add_tweet')
          self.tweet_buffer.add_tweet(data)
          root.info('added tweet to buffer')
          return True

        except BaseException as e:
            root.info('in excpetion')

            root.error("Error on_data: %s" % str(e))

        return True
 
    def on_error(self, status):
        print 'an error happened'
        print(status)
        return True

def main(hashtag):
  # config_file = 'config.yml'
  # config = read_config_file(config_file)
  root.info('starting twitter-ingestor for: %s' %hashtag)
  creds = setup_credentials()
  auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
  auth.set_access_token(creds['access_token'], creds['access_secret'])
  filepath = '%s-tweets.json' %hashtag
  tweet_buffer = TweetBuffer(hashtag)
  twitter_stream = Stream(auth, MyListener(filepath, tweet_buffer))
  twitter_stream.filter(track=['#%s'%hashtag])

if __name__ == '__main__':
  try:
    hashtag = sys.argv[1] 
    main(hashtag)

  except IndexError:
    print 'usage: %s hashtag' %sys.argv[0]
    sys.exit(1)
