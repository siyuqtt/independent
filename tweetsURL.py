try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
import re,util
from configHelper import myconfig
from tweetsManager import textManager
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


twitter = Twitter(auth=oauth)
# Get a sample of the public data following through Twitter
formalaccount = ['@nytimes','@cnnbrk','@BBCBreaking','@CNN','@ABC','@NBCNews']
for acnt in formalaccount:
    query = twitter.search.tweets(q="from:"+acnt,
                                  count="150",
                                  lang="en")

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
        time.sleep(5)
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


    f = open('files/urltweets_acnt_info_'+acnt+'.txt','w')
    rawfilename = 'files/urltweets_acnt_'+acnt+'.txt'
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
    fout = open('files/filtered_acnt_'+acnt+'.txt','w')
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

                        TODO:
                        refact here: track not only the average
                        for one tweets that have high similarity with the some (upper)
                        or one tweet looks too different (lower) filter out

                        automatically set upper and lower by using 1-sigma vairance

                    '''
                    candi = similarity.groupExcatWordscore(candi,0.8,0.3)
                    '''
                        second filting
                        filter by embedding


                        TODO: automatically set bound by using avg + 1 sigma
                    '''
                    candi = similarity.embeddingScore(0.6, candi)
                    '''
                        third filting
                        filter by wordNet

                         TODO: automatically set bound by using avg + 1 sigma
                    '''
                    candi = similarity.wordNetScore(0.6,candi)
                    if len(candi) < 2:
                        candi = []
                        continue
                    for c in candi:
                        fout.write(c+'\n')
                    fout.write('\n')
                    candi = []
    fout.close()






