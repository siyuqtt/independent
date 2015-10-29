try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth
from tokenize import *
import re, os,time,sys
from configHelper import myconfig
import datetime
URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
import schedule
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

def getDate():
    return datetime.date.today().__str__()

def getTargetDate():
    targetdate = (datetime.date.today()- datetime.timedelta(days=7)).__str__()
    return targetdate
def getOldUrl(fhander):
    try:
        fhander.seek(0, os.SEEK_SET)
        return dict(  (l.strip().split()) for l in fhander.readlines() )
    except:
        return dict()


def queryNewUrl(oldurls,acnt):
    targetdate = getTargetDate()
    try:
        query = twitter.search.tweets(q="from:"+acnt,
                                  count="100",
                                  lang="en",
                                  until=targetdate
                                  )
    except:
        return
    else:
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



def RateLimited(maxPerSecond,lastTimeCalled):
    """
    :param maxPerSecond: 0.2
    :param lastTimeCalled:
    :return:
    """

    minInterval = 1.0 / float(maxPerSecond)
    elapsed = time.clock() - lastTimeCalled
    leftToWait = int(minInterval - elapsed)+1
    if leftToWait>0:
        time.sleep(leftToWait)
    return time.clock()

def getQuery(maxid, minid, furl):

    if maxid is not None and minid is not None:
        try:
            query = twitter.search.tweets(q=furl,
                                      count="100",
                                      lang="en",
                                      max_id=minid
                                      )
        except:
            return None
        else:
            if len(query["statuses"])==0:
                try:
                    query = twitter.search.tweets(q=furl,
                                      count="100",
                                      lang="en",
                                      since_id=maxid
                                      )
                except:
                    return None
                else:
                    if len(query["statuses"])==0:
                        try:
                            query = twitter.search.tweets(q=furl,
                                                  count="100",
                                                  lang="en"
                                                  )
                        except:
                            return None

    return query


def querywithFull(urldict,acnt,urlid_dict):
    date = getDate()
    data = {}
    lastTimeCalled = time.clock()
    for surl, furl in urldict.items():
        data[surl] = []
        cur = set()
        lastTimeCalled = RateLimited(0.2,lastTimeCalled)
        if urlid_dict.has_key(surl):
            maxid = urlid_dict[surl][0]
            minid = urlid_dict[surl][1]
        else:
            maxid, minid = None, None

        query = getQuery(maxid,minid,furl)
        if query is None:
            continue
        for result in query["statuses"]:
            nre = re.sub(URLINTEXT_PAT,"",result["text"]).lower().strip()
            if nre not in cur:
                data[surl].append([result["id_str"],nre])
                maxid = max(maxid, result["id_str"])
                if minid is None:
                    minid = result["id_str"]
                else:
                    minid = min(minid, result["id_str"])
                cur.add(nre)
        urlid_dict[surl] = (maxid, minid)


    f = open('files/urltweets_acnt_info_'+acnt+'_'+date+'_auto.txt','a')
    rawfilename = 'files/urltweets_acnt_'+acnt+'_'+date+'_auto.txt'
    ff = open(rawfilename,'a')
    statff = open('files/'+acnt+'_'+date+'_urlcounts.txt','a')
    # mytextmanager = textManager()
    for k,v in data.items():
        f.write(k+'\n')
        statff.write(k+'\t'+str(len(v))+'\n')
        for [id,vv] in v:
            tokens = tokenizeRawTweetText(vv)
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
            del urlid_dict[k]
    f.close()
    statff.close()
    ff.close()

def buildurlDictfromFile(handler):
    handler.seek(0, os.SEEK_SET)
    def item(l):
        ts = l.strip().split()
        try:
            return (ts[0],(ts[1], ts[2]))
        except:
            return None
    try:
        return dict(item(l) for l in handler.readlines())
    except:
        return dict()

def job():
    for acnt in formalaccount:
        print acnt, time.asctime()
        sys.stdout.flush()
        urlfiles = 'files/'+acnt+'_urls.txt'
        urlfile_handler= open(urlfiles,'a+')
        urldict = getOldUrl(urlfile_handler)

        urlidfiles = "files/"+ acnt+"_urlID.txt"
        urlid_handler = open(urlidfiles,'a+')
        urlid_dict = buildurlDictfromFile(urlid_handler)
        queryNewUrl(urldict,acnt)
        if len(urldict) > 0:
            querywithFull(urldict,acnt,urlid_dict)
        urlfile_handler.seek(0, os.SEEK_SET)
        urlfile_handler.truncate(0)
        for k,v in urldict.items():
            urlfile_handler.write(k+'\t'+v+'\n')
        urlfile_handler.close()

        urlid_handler.seek(0,os.SEEK_SET)
        urlid_handler.truncate(0)
        for k,v in urlid_dict.items():
            urlid_handler.write(k+'\t'+v[0]+'\t'+v[1]+'\n')
        urlid_handler.close()



schedule.every().hour.do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(1)
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






