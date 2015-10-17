try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth
import re, os
from configHelper import myconfig
from tweetsManager import textManager
import datetime
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
date = datetime.date.today().__str__()
targetdate = (datetime.date.today()- datetime.timedelta(days=7)).__str__()
def getOldUrl(fhander):
    try:
        fhander.seek(0, os.SEEK_SET)
        return dict(  (l.strip().split()) for l in fhander.readlines() )
    except:
        return dict()


def queryNewUrl(oldurls):

    query = twitter.search.tweets(q="from:"+acnt,
                                  count="100",
                                  lang="en",
                                  until=targetdate
                                  )


    shorturlsets = set()
    for result in query["statuses"]:
        try:
            for url in URLINTEXT_PAT.findall(result["text"]):
                if oldurls.has_key(url):
                    continue
                shorturlsets.add(url)
        except:
            pass

    for surl in shorturlsets:
        try:
            oldurls[surl] =requests.get(surl).url.split('?')[0]
        except:
            pass



def querywithFull(urldict,acnt):
    data = {}
    for surl, furl in urldict.items():
        # time.sleep(15*60)
        data[surl] = []
        cur = set()

        query = twitter.search.tweets(q=furl,
                                          count="100",
                                          lang="en",
                                      until=targetdate
                                          )
        for result in query["statuses"]:
            nre = re.sub(URLINTEXT_PAT,"",result["text"]).lower().strip()
            if nre not in cur:
                data[surl].append([result["id_str"],nre])
                cur.add(nre)


    f = open('files/urltweets_acnt_info_'+acnt+'_'+date+'_auto.txt','a')
    rawfilename = 'files/urltweets_acnt_'+acnt+'_'+date+'_auto.txt'
    ff = open(rawfilename,'a')
    statff = open('files/'+acnt+'_'+date+'_urlcounts.txt','a')
    mytextmanager = textManager()
    for k,v in data.items():
        f.write(k+'\n')
        statff.write(k+'\t'+str(len(v))+'\n')
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

            f.write('\n')
            ff.write('\n')
        f.write('\n')
        ff.write('\n')
        if len(v) < 50:
            del urldict[k]
    f.close()
    statff.close()
    ff.close()


for acnt in formalaccount:

    urlfiles = 'files/'+acnt+'_urls.txt'

    urlfile_handler= open(urlfiles,'a+')

    urldict = getOldUrl(urlfile_handler)
    queryNewUrl(urldict)
    if len(urldict) > 0:
        querywithFull(urldict,acnt)
    urlfile_handler.seek(0, os.SEEK_SET)
    urlfile_handler.truncate(0)
    for k,v in urldict.items():
        urlfile_handler.write(k+'\t'+v+'\n')
    urlfile_handler.close()
    # for iter in xrange(10):



        # anylasis = util.statis(tweetsstatic)
        # print anylasis.getreport()
        # anylasis.setArray(tokenstatic)
        # print anylasis.getreport()
        # similarity = util.sentenceSimilarity()
        #
        # similarity.buildEmbedding()
        # fout = open('files/filtered_acnt_'+acnt+'_auto.txt','w')
        # with open(rawfilename) as f:
        #         candi = []
        #         for line in f:
        #             line = line.strip()
        #             if len(line) != 0:
        #                 candi.append(line)
        #             else:
        #                 '''
        #                     first filting
        #                     filter out tweets look too same or too different
        #
        #                     TODO:
        #                     refact here: track not only the average
        #                     for one tweets that have high similarity with the some (upper)
        #                     or one tweet looks too different (lower) filter out
        #
        #                     automatically set upper and lower by using 1-sigma vairance
        #
        #                 '''
        #                 candi = similarity.groupExcatWordscore(candi)
        #                 '''
        #                     second filting
        #                     filter by embedding
        #
        #
        #                     TODO: automatically set bound by using avg
        #                 '''
        #                 candi = similarity.embeddingScore( candi)
        #                 '''
        #                     third filting
        #                     filter by wordNet
        #
        #                      TODO: automatically set bound by using avg + 1 sigma
        #                 '''
        #                 candi = similarity.wordNetScore(candi)
        #                 if len(candi) < 2:
        #                     candi = []
        #                     continue
        #                 for c in candi:
        #                     fout.write(c+'\n')
        #                 fout.write('\n')
        #                 candi = []
        # fout.close()






