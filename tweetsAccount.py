try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
import re
from configHelper import myconfig

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
                                  count="50",
                                  lang="en"
                        )
    formaltweets += [y["text"] for y in [x for x in query['statuses']]]

f = open('formaltweets.txt','w')

for it in formaltweets:
    try:
        f.write(it+'\n')
    except:
        f.write(it.encode('utf-8')+'\n')
f.close()
