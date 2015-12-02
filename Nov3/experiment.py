__author__ = 'siyuqiu'
from paraphrase import *
from nltk.metrics.distance import edit_distance

'''
 the following code will calculate pink and jacquad score
 for labeled data
'''


def getXY(fname):
    Y = []
    X = []
    lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
    countGroup = 0
    countTweets = 0
    candiX = []
    candiY = []
    for line in lines:
        if line == "" and len(candiX) > 0:

            countTweets += len(candiX)
            X.append(candiX)
            Y.append(candiY)
            candiX = []
            candiY = []
            countGroup += 1
        elif line.strip() == "":
            continue
        else:
            [tw, label] = line.strip().split('\t')
            candiX.append(tw)
            candiY.append(int(label))
    if len(candiX) > 0:

        X.append(candiX)
        Y.append(candiY)
        countGroup += 1
        countTweets += len(candiX)

    print "group: ",countGroup, "tweets: ",countTweets
    return X,Y

def experiment1():
    matPink = defaultdict(list)
    matJac = defaultdict(list)
    matEdit = defaultdict(list)
    myParaHelper = ParaPrase()

    X,Y = getXY('oldFiles/files/train.txt')
    x,y = getXY('oldFiles/files/test.txt')
    X += x
    Y += y
    for idx in xrange(len(X)):
        curX = defaultdict(list)
        curXTokens = defaultdict(list)
        for i,y in enumerate(Y[idx]):
            curX[y].append(X[idx][i])
            curXTokens[y].append(tokenizeRawTweetText(X[idx][i]))
        for targetLabel in curX.keys():
            for referLabel in curX.keys():
                key = targetLabel*10+referLabel
                if targetLabel == referLabel:
                    matPink[key].append(myParaHelper.Pink(curX[targetLabel]))
                    matJac[key].append(myParaHelper.Jacquard(curXTokens[targetLabel]))

                else:
                    matPink[key].append(myParaHelper.arr2ArrPink(curX[targetLabel],curX[referLabel]))
                    matJac[key].append(myParaHelper.arrTokens2ArrTokensJacquard(curXTokens[targetLabel],
                                                                                curXTokens[referLabel]))
                matEdit[key].append(myParaHelper.arr2ArrEditDistance(curX[targetLabel],curX[referLabel]))

    for k in matEdit.keys():
        print k,'\t', sum(matEdit[k])*10/len(matEdit[k]),
        print '\t', sum(matPink[k])*10/len(matPink[k]),
        print '\t', sum(matJac[k])*10/len(matJac[k])

'''
in this experiment
we will grouping urls with the same range of half-life
meature in 24 hours data
'''


import re,util
from collections import defaultdict
p = re.compile(r'@(.*)_(.*)_(\d{2})_urlcounts.txt')
from os import listdir
from os.path import isfile, join
mypath = "files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
times_label = ['00','01','02','03','04','05','06','07','08','09','10',
               '11','12','13','14','15','16','17','18','19','20','21',
               '22','23']

'''
 at each time
 how many new urls appear
'''
time_urls = defaultdict(set)
time_counts = [0]*24
url_nofilt = defaultdict(list)
url_filt = defaultdict(list)

for idx,t in enumerate(times_label):
    findno = 0
    for fn in onlyfiles:
        m = p.match(fn)
        if m:
            if m.group(3) != t:
                continue
            acnt = m.group(1)
            findno += 1
            with open(join(mypath,fn)) as fhandler:
                for [x, y, z] in [l.strip().split('\t') for l in fhandler.readlines()]:
                    if z == '0':
                        continue
                    '''
                        use url_nofilt and url_filt
                        to record the impact of filtering
                    '''
                    if not url_filt.has_key(x):
                        url_filt[x] = [(0,1e-10)]*24
                        url_nofilt[x] = [(0,1e-10)]*24
                    url_filt[x][int(t)] = (url_filt[x][int(t)][0]+int(y),url_filt[x][int(t)][1]+1)
                    url_nofilt[x][int(t)] = (url_nofilt[x][int(t)][0]+int(z),url_nofilt[x][int(t)][1]+1)
                    time_urls[t].add(x)
    tmp = time_urls[t]
    for subidx in xrange(idx):
        tmp = tmp - time_urls[times_label[subidx]]
    time_counts[int(t)] = len(tmp)/(findno+1e-10)
