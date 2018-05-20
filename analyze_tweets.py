import json

def read_tweets_from_file(filename):   
    tweets = []
    with open(filename, 'r') as fp:
        for line in fp:
            tweets.append(json.loads(line))

    return tweets

def main(**kwargs):
  cavs_tweets = read_tweets_from_file(kwargs['filepath'])

  for tweet in cavs_tweets:
      #print type(tweet)
      #print tweet.keys()
      print tweet['text']
      print '============================='

if __name__ == '__main__':
  kwargs = {'filepath': 'trump.json'}
  main(**kwargs)
