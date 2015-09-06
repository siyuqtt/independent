__author__ = 'siyuqiu'
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import OAuth, TwitterStream
from configHelper import myconfig
# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = myconfig.accesstoken
ACCESS_SECRET = myconfig.accessscecret
CONSUMER_KEY = myconfig.consumertoken
CONSUMER_SECRET = myconfig.consumersecret

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
tweet_count = 1000
replys =[]
for tweet in iterator:
    try:
        if tweet['in_reply_to_user_id'] is not None and tweet['lang'] == 'en':
            replys.append(tweet['text'])
            tweet_count -= 1
    except:
        continue
    if tweet_count <= 0:
        break
f = open('informaltweets.txt','w')

for it in replys:
    try:
        f.write(it+'\n')
    except:
        f.write(it.encode('utf-8')+'\n')
f.close()
