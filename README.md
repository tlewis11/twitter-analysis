# twitter-analysis
# How to run locally: 
1. clone this repo and build the Docker image

```
  git clone git@github.com:tlewis11/twitter-analysis.git
  cd twitter-analysis
  docker build -i twitter-ingestor .
```

2. Set twitter credentials
```
  export TWITTER_CONSUMER_KEY='your-value'
  export TWITTER_CONSUMER_SECRET='your-value'
  export TWITTER_ACCESS_TOKEN='your-value'
  export TWITTER_ACCESS_SECRET='your-value'
```

3.  Run the Docker image
```
  docker run -it -e TWITTER_CONSUMER_KEY \
    -e TWITTER_CONSUMER_SECRET \
    -e TWITTER_ACCESS_TOKEN \
    -e TWITTER_ACCESS_SECRET \
    $image_name
```
