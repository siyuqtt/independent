__author__ = 'siyuqiu'
from paraphrase import *


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

def experiment2():
    import re
    from collections import defaultdict
    p = re.compile(r'@(.*)_(.*_\d{2})_urlcounts.txt')
    from os import listdir
    from os.path import isfile, join
    from PlotView import PlotView
    mypath = "files"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


    '''
     at each time
     how many new urls appear
    '''

    url_nofilt = defaultdict(dict)
    url_filt = defaultdict(dict)


    for fn in onlyfiles:
        m = p.match(fn)
        if m:
            acnt = m.group(1)
            dateTimeKey = m.group(2)
            with open(join(mypath,fn)) as fhandler:
                for [x, y, z] in [l.strip().split('\t') for l in fhandler.readlines()]:
                    if z == '0':
                        continue
                    '''
                        use url_nofilt and url_filt
                        to record the impact of filtering
                    '''

                    url_filt[x][dateTimeKey] = int(y)
                    url_nofilt[x][dateTimeKey] = int(z)
    '''
     calculate half-life
    '''
    def accumulitiveSum(arr,start=0):
        for it in arr:
            start += it
            yield start
    def findHalfLife(arr):
        target = arr[-1]/2
        l, r ,m= 0, len(arr)-1,0
        while l < r:
            m = (l+r)/2
            if arr[m] == target:
                return m
            elif arr[m] > target:
                r = m
            else:
                l = m+1
        return m
    halfLifeCounterFilter = dict()
    halfLifeCounterNoFilter = dict()
    for k, v in url_filt.items():
        sorted_v = dict(sorted(v.items(),key=operator.itemgetter(0)))
        summed_v = list(accumulitiveSum(sorted_v.values()))
        half = findHalfLife(summed_v)
        halfLifeCounterFilter[half] = halfLifeCounterFilter.get(half,0)+1.0
    for k, v in url_nofilt.items():
        sorted_v = dict(sorted(v.items(),key=operator.itemgetter(0)))
        summed_v = list(accumulitiveSum(sorted_v.values()))
        half = findHalfLife(summed_v)
        halfLifeCounterNoFilter[half] = halfLifeCounterNoFilter.get(half,0)+1.0
    painter = PlotView()
    total = len(url_filt)
    painter.newFigure()
    painter.plotBar(halfLifeCounterFilter.keys(),[it/total for it in halfLifeCounterFilter.values()],None,"Percentage After Filtering",'b')
    painter.plotBar(halfLifeCounterNoFilter.keys(),[it/total for it in halfLifeCounterNoFilter.values()],None,"Percentage Before Filtering",'r')
    painter.showplot(halfLifeCounterNoFilter.keys())


'''
the following code explore the hourly data of
tweets per url
and new url at each time
'''

def experiment3():
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

    print len(url_nofilt)
    statis_helper = util.statis(None)
    avg_filt = [[t[0]/t[1] for t in xlist] for xlist in url_filt.values()]
    sum_filt = [reduce(lambda x,y: x+y[0], xlist,0 ) for xlist in url_filt.values()]
    statis_helper.setArray(sum_filt)
    print statis_helper.getreport()
    avg_nofilt =  [[t[0]/t[1] for t in xlist] for xlist in url_nofilt.values()]
    sum_nofilt = [reduce(lambda x,y: x+y[0], xlist,0 ) for xlist in url_nofilt.values()]
    statis_helper.setArray(sum_nofilt)
    print(statis_helper.getreport())


    from PlotView import PlotView

    painter = PlotView()

    '''
    first we want to find some pattern url_filt
    do classification using kmeans
    then plot the centra
    '''
    # from sklearn.cluster import KMeans
    # km = KMeans(n_clusters=3)
    # km.fit(avg_filt)
    # centras = km.cluster_centers_
    xlabel = [int(x) for x in times_label]
    # class_percentage = {}
    # for i in xrange(km.n_clusters):
    #     class_percentage[i] = 0
    # for i in km.labels_:
    #     class_percentage[i]+=1
    # for i in xrange(km.n_clusters):
    #     print class_percentage[i]*1.0/len(km.labels_)
    # for idx, data in enumerate(centras):
    #     painter.plotLine(xlabel,data,str(idx))
    for data in avg_nofilt:
        painter.plotLine(xlabel,data,None,'r*')
    painter.showplot(xlabel)
    #painter.showLegend()
    painter.newFigure()
    painter.plotLine(xlabel, time_counts,"number of new urls","r")
    def cumulativeSum(vlist,start = 0):
        for v in vlist:
            start+= v
            yield start

    painter.plotBar(xlabel,[len(t) for t in time_urls.values()],None,"Communicative URLs",'b')
    painter.showplot(xlabel)
experiment3()
