#!/bin/bash
if [ $# -ne 1 ]; then
  echo "Usage: twitter_ingest.py hashtag"
  exit 1
fi
python2.7 ./twitter_ingest.py $1
