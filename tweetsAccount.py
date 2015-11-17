try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
from configHelper import myconfig
import datetime,re
from dateutil import parser
URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')



ACCESS_TOKEN = myconfig.accesstoken
ACCESS_SECRET = myconfig.accessscecret
CONSUMER_KEY = myconfig.consumertoken
CONSUMER_SECRET = myconfig.consumersecret

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter = Twitter(auth=oauth)


formalaccount = ['@nytimes','@cnnbrk','@BBCBreaking','@CNN','@ABC','@NBCNews']
formaltweets = []
for acnt in formalaccount:
    query = twitter.search.tweets(q="from:"+acnt,
                                  count="150",
                                  lang="en")
    # formaltweets += [y["text"] for y in [x for x in query['statuses']]]
    goal = 100
    tweet_count = 0
    shorturlsets = set()
    nourls = 0
    urls_count = 0
    for tweet in query['statuses']:
        try:
            if abs((datetime.datetime.now() - parser.parse(tweet["created_at"]).now()).days) < 15:
                urls = URLINTEXT_PAT.findall(tweet["text"])
                if len(urls) ==0:
                    nourls += 1
                else:
                    for url in urls:
                        shorturlsets.add(url)
                        urls_count += 1

                tweet_count += 1
        except:
            continue
        if tweet_count >= goal:
            break
    print acnt,
    print '\t',
    print len(shorturlsets),
    print '\t',
    print nourls,
    print '\t',
    print urls_count,
    print tweet_count
# f = open('formaltweets.txt','w')
#
# for it in formaltweets:
#     try:
#         f.write(it+'\n')
#     except:
#         f.write(it.encode('utf-8')+'\n')
# f.close()
