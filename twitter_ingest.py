#!/usr/bin/env python

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import os
import yaml

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

class MyListener(StreamListener):

    def __init__(self, filepath):
      self.filepath = filepath 
 
    def on_data(self, data):
        try:
          with open(self.filepath, 'a') as f:
            f.write(data)
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
