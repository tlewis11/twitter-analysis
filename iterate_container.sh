#!/bin/bash
image_name='twitter_ingestor'
docker build -t $image_name .
#docker run -it twitter_ingestor
echo $TWITTER_CONSUMER_KEY
docker run -it -e TWITTER_CONSUMER_KEY \
  -e TWITTER_CONSUMER_SECRET \
  -e TWITTER_ACCESS_TOKEN \
  -e TWITTER_ACCESS_SECRET \
  $image_name
