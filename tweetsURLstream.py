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
from dateutil import parser
import time
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

goal = 1000
curStage = 0
while curStage < goal:
    time.sleep(5)
    iter = curStage%100
    tweet_count = 100
    shorturlsets = set()
    for tweet in iterator:
        try:
            if tweet['lang'] == 'en':
                '''
                take only tweets at most 7 days away from today
                '''
            if abs((datetime.datetime.now() - parser.parse(tweet["created_at"]).now()).days) < 7:
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

    f = open('files/urltweets_stream_info_'+str(iter)+'.txt','w')
    rawfilename = 'files/urltweets_stream_'+str(iter)+'.txt'
    ff = open(rawfilename,'w')
    tweetsstatic =[]
    tokenstatic =[]
    mytextmanager = textManager()
    for k,v in data.items():
        f.write(k+'\n')
        for [id,vv] in v:
            tokens = mytextmanager.tokenizefromstring(vv)
            f.write(id+"\t")
            for t in tokens:
                try:
                    f.write(t.encode('utf-8')+" ")
                    ff.write(t.encode('utf-8')+" ")
                except:
                    # f.write(t+" ")
                    pass
            tweetsstatic.append(len(v))
            tokenstatic.append(len(tokens))
            f.write('\n')
            ff.write('\n')
        f.write('\n')
        ff.write('\n')
    f.close()
    ff.close()
    anylasis = util.statis(tweetsstatic)
    print anylasis.getreport()
    anylasis.setArray(tokenstatic)
    print anylasis.getreport()



    similarity = util.sentenceSimilarity()

    similarity.buildEmbedding()
    fout = open('files/filtered_'+str(iter)+'.txt','w')
    with open(rawfilename) as f:
            candi = []
            for line in f:
                line = line.strip()
                if len(line) != 0:
                    candi.append(line)
                else:
                    '''
                        first filting
                        filter out tweets look too same or too different
                    '''
                    candi = similarity.groupExcatWordscore(candi,0.9,0.3)
                    '''
                        second filting
                        filter by embedding
                    '''
                    candi = similarity.embeddingScore(0.5, candi)
                    '''
                        third filting
                        filter by wordNet
                    '''
                    candi = similarity.wordNetScore(0.5,candi)
                    if len(candi) < 2:
                        candi = []
                        continue
                    curStage += 1
                    for c in candi:
                        fout.write(c+'\n')
                    fout.write('\n')
                    candi = []












