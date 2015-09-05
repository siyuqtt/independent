try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
import re
from configHelper import myconfig
URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

import requests
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = myconfig.accesstoken
ACCESS_SECRET = myconfig.accessscecret
CONSUMER_KEY = myconfig.consumertoken
CONSUMER_SECRET = myconfig.consumersecret

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter = Twitter(auth=oauth)
# Get a sample of the public data following through Twitter
# iterator = twitter_stream.statuses.filter(track="nytimes.com/interactive/projects/cp/summer-of-science-2015/latest/how-often-is-bmi-misleading", language="en")
query = twitter.search.tweets(q="from:@nytimes",
                              count="100",
                              lang="en"
                    )
shorturlsets = set()
for result in query["statuses"]:
    try:
        for url in URLINTEXT_PAT.findall(result["text"]):
            shorturlsets.add(url)
    except:
        pass
fullurlset = set()
for surl in shorturlsets:
    try:
        fullurlset.add(requests.get(surl).url.split('?')[0])
    except:
        pass
data = {}
for furl in fullurlset:
    data[furl] = set()
    query = twitter.search.tweets(q=furl,
                              count="100",
                              lang="en")
    for result in query["statuses"]:
        data[furl].add(result["text"])
# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
# tweet_count = 1000
# for tweet in iterator:
#     tweet_count -= 1
#     # Twitter Python Tool wraps the data returned by Twitter
#     # as a TwitterDictResponse object.
#     # We convert it back to the JSON format to print/score
#     data  = json.dumps(tweet)
#
#     # The command below will do pretty printing for JSON data, try it out
#     # print json.dumps(tweet, indent=4)
#
#     if tweet_count <= 0:
#         break
f = open('test_json.txt','w')
f.write(json.dumps(data, sort_keys=True,
            indent=4, separators=(',', ': ')))
# for k,v in data.items():
#     f.write(k+'\n')
#     for vv in v:
#         try:
#             f.write('\t'+vv+'\n')
#         except:
#             f.write('\t'+vv.encode('utf-8')+'\n')
f.close()
