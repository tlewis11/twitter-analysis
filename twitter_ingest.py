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

def main(hashtag):
  # config_file = 'config.yml'
  # config = read_config_file(config_file)
  creds = setup_credentials()
  auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
  auth.set_access_token(creds['access_token'], creds['access_secret'])
  filepath = '%s-tweets.json' %hashtag
  twitter_stream = Stream(auth, MyListener(filepath))
  twitter_stream.filter(track=['#%s'%hashtag])

class TweetBuffer(object):
    def __init__(self):
        self.tweets = []
        self.max_tweets = 100

    def add_tweet(tweet_json):
        self.tweets.append(tweet_json)
        if len(self.tweets) >= 10:
            self.flush()

    def flush(self):
        s3_client = boto3.client('s3') 
        tweets = bytes(json.dumps(self.tweets), encoding="ascii")
        bucket_name = 'sarabi-twitter'
        key_name = 'tweets-%s' %dtetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        s3_client.put_object(Body=tweets, Bucket=bucket_name, Key=key_name)
        
   
class MyListener(StreamListener):

    def __init__(self, filepath, tweet_buffer):
        self.filepath = filepath 
        self.tweet_buffer(tweet_buffer)
 
    def on_data(self, data):
       
        try:
            self.tweet_buffer.add_tweet(data)
            return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))

        return True
 
    def on_error(self, status):
        print(status)
        return True

if __name__ == '__main__':
  try:
    hashtag = sys.argv[1] 
    main(hashtag)

  except IndexError:
    print 'usage: %s hashtag' %sys.argv[0]
    sys.exit(1)
