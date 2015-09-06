try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
import re
from configHelper import myconfig
from tweetstext import textManager
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
        nre = re.sub(URLINTEXT_PAT,"",result["text"]).lower().strip()
        data[furl].add(nre)

f = open('urltweets.txt','w')

mytextmanager = textManager()
for k,v in data.items():
    tokens= []
    f.write(k+'\n')
    for vv in v:
        try:
            f.write('\t'+vv+'\n')
            tokens += mytextmanager.tokenizefromstring(vv)
        except:
            f.write('\t'+vv.encode('utf-8')+'\n')
            tokens += mytextmanager.tokenizefromstring(vv.encode('utf-8'))
    (total, wordfre) = mytextmanager.getfreword(tokens)
    (total_bi, bifre) = mytextmanager.getfrebigram(tokens)
    mytextmanager.writetofile(f,wordfre,total,bifre,total_bi)
    f.write('\n')
f.close()


