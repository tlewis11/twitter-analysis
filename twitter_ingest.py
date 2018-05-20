#!/usr/bin/env python

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import os

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


def main():
  creds = setup_credentials()
  auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
  auth.set_access_token(creds['access_token'], creds['access_secret'])
  twitter_stream = Stream(auth, MyListener())
  twitter_stream.filter(track=['#trump'])

class MyListener(StreamListener):

    def __init__(self):
      self.filepath = 'trump.json'
 
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
  main()
