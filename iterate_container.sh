#!/bin/bash
if [ -z $1 ]; then
  echo "USAGE: twitter_ingestor.py hashtag"
  exit 1
fi
image_name='twitter_ingestor'
docker build -t $image_name .
docker run -it -e TWITTER_CONSUMER_KEY \
  -e TWITTER_CONSUMER_SECRET \
  -e TWITTER_ACCESS_TOKEN \
  -e TWITTER_ACCESS_SECRET \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  $image_name $1


