__author__ = 'siyuqiu'
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import TwitterStream, OAuth,Twitter
import re,util
from configHelper import myconfig
from tweetsManager import textManager
import datetime
import time
from dateutil import parser
URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

import requests
# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = myconfig.accesstoken
ACCESS_SECRET = myconfig.accessscecret
CONSUMER_KEY = myconfig.consumertoken
CONSUMER_SECRET = myconfig.consumersecret

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
tweet_count = 100
shorturlsets = set()
for tweet in iterator:
    try:
        if tweet['lang'] == 'en':
            '''
            take only tweets at most 7 days away from today
        '''
        if abs((datetime.datetime.now() -parser.parse(tweet["created_at"]).now()).days) < 7:
            urls = URLINTEXT_PAT.findall(tweet["text"])
            if len(urls) ==0:
                continue
            for url in urls:
                shorturlsets.add(url)

            tweet_count -= 1
    except:
        continue
    if tweet_count <= 0:
        break



fullurlset = set()
for surl in shorturlsets:
    try:
        fullurlset.add(requests.get(surl).url.split('?')[0])
    except:
        pass

data = {}
twitter = Twitter(auth=oauth)
for furl in fullurlset:
    data[furl] = []
    cur = set()
    query = twitter.search.tweets(q=furl,
                              count="100",
                              lang="en")
    for result in query["statuses"]:

        nre = re.sub(URLINTEXT_PAT,"",result["text"]).lower().strip()
        if nre not in cur:
            data[furl].append([result["id_str"],nre])
            cur.add(nre)

f = open('files/urltweets_stream.txt','w')
tweetsstatic =[]
tokenstatic =[]
mytextmanager = textManager()
for k,v in data.items():
    f.write(k+'\n')
    # tokens= []
    # f.write(k+'\n')
    #
    # for vv in v:
    #     try:
    #         f.write('\t'+vv+'\n')
    #         tokens += mytextmanager.tokenizefromstring(vv)
    #     except:
    #         f.write('\t'+vv.encode('utf-8')+'\n')
    #         tokens += mytextmanager.tokenizefromstring(vv.encode('utf-8'))
    # tweetsstatic.append(len(v))
    # tokenstatic.append(len(tokens))
    # (total, wordfre) = mytextmanager.getfreword(tokens)
    # (total_bi, bifre) = mytextmanager.getfrebigram(tokens)
    # mytextmanager.writetofile(f,wordfre,total,bifre,total_bi)
    for [id,vv] in v:
        tokens = mytextmanager.tokenizefromstring(vv)
        f.write(id+"\t")
        for t in tokens:
            try:
                f.write(t.encode('utf-8')+" ")
            except:
                # f.write(t+" ")
                pass
        tweetsstatic.append(len(v))
        tokenstatic.append(len(tokens))
        f.write('\n')
    f.write('\n')
f.close()
anylasis = util.statis(tweetsstatic)
print anylasis.getreport()
anylasis.setArray(tokenstatic)
print anylasis.getreport()






