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
    from util import savitzky_golay
    mypath = "ServerFile/files"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    formalaccount = ['@nytimes','@cnnbrk','@BBCBreaking','@CNN','@ABC','@NBCNews']

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
                    if int(y) == 0:
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
    from ctypes import c_int64
    timeNewUrl = [(c_int64(0),set()) for _ in xrange(24)]

    for k, v in url_filt.items():
        sorted_v = dict(sorted(v.items(),key=operator.itemgetter(0)))
        summed_v = list(accumulitiveSum(sorted_v.values()))
        half = findHalfLife(summed_v)
        halfLifeCounterFilter[half] = halfLifeCounterFilter.get(half,0)+1.0
        [date, idx]= sorted_v.keys()[0].split('_')
        timeNewUrl[int(idx)][0].value += 1
        timeNewUrl[int(idx)][1].add(date)


    for k, v in url_nofilt.items():
        sorted_v = dict(sorted(v.items(),key=operator.itemgetter(0)))
        summed_v = list(accumulitiveSum(sorted_v.values()))
        half = findHalfLife(summed_v)
        halfLifeCounterNoFilter[half] = halfLifeCounterNoFilter.get(half,0)+1.0
    painter = PlotView()
    total = len(url_filt)
    painter.newFigure()
    plt = painter.getPLT()
    ax = painter.subPlots()
    #plotBar(self, xlable, means, std, lab,color, ax = None, no = None)
    painter.plotBar(halfLifeCounterFilter.keys(),
                    [it/total for it in halfLifeCounterFilter.values()],None,"Percentage After Filtering",'b',ax,0)
    painter.plotBar(halfLifeCounterNoFilter.keys(),
                    [it/total for it in halfLifeCounterNoFilter.values()],None,"Percentage Before Filtering",'r',ax,1)

    plt.xlabel("number of hours")
    plt.ylabel("percentage of new tweets")

    painter.showplot(halfLifeCounterNoFilter.keys())
    # painter.newFigure()
    # #smoothTimeUrl = savitzky_golay([x.value/(len(y)+1e-10) for (x,y) in timeNewUrl],5, 3)
    # painter.plotLine([x for x in xrange(24)], [x.value/(len(y)+1e-10) for (x,y) in timeNewUrl],"No Smooth")
    # #painter.plotLine([x for x in xrange(24)], smoothTimeUrl,"Savitzky Golay Smooth")
    # plt = painter.getPLT()
    # plt.xlabel("time clock")
    # plt.ylabel("number of new URLs")
    # plt.title("New URL at each Time")
    # plt.legend(loc=2)
    # painter.showplot([x for x in xrange(24)])
    print 'finish'


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
    mypath = "ServerFile/files"
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
    accu_time_counts = [0]*24
    url_nofilt = defaultdict(list)
    url_filt = defaultdict(list)
    count_total = 0
    count_over = 0
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
                        if int(z) == 0:
                            continue
                        count_total += 1
                        if int(z) >= 100:
                            count_over += 1
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
        accu_time_counts[int(t)] = len(time_urls[t])/(findno+1e-10)

    print len(url_nofilt),count_total,count_over
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
    plt = painter.getPLT()
    for data in avg_filt:
        #plt.scatter(xlabel,data,marker='o',facecolors='none')
        plt.plot(xlabel,data,'r.',alpha=0.2)
    for data in avg_nofilt:
        #plt.scatter(xlabel,data,marker='o',facecolors='none')
         plt.plot([x+0.3 for x in xlabel],data,'b.',alpha=0.2)
    def elementAdd(arr1, arr2):
        return [x[0]+x[1] for x in zip(arr1,arr2)]

    avg_avg_filt = [x/len(avg_filt) for x in reduce(elementAdd, avg_filt)]
    avg_avg_nofilt = [x/len(avg_nofilt) for x in reduce(elementAdd, avg_nofilt)]
    painter.plotLine(xlabel,avg_avg_filt,'Mean of New Tweets(filtered)','black')
    painter.plotLine([x+0.3 for x in xlabel],avg_avg_nofilt,'Mean of New Tweets','g')
    plt.xlabel("time clock")
    plt.ylabel("number of new tweets")
    plt.legend()
    painter.showplot(xlabel)



'''
in this experiment
we will calculate the time when new url comes for each accout
'''

def experiment4():
    import re
    from collections import defaultdict
    p = re.compile(r'@(.*)_(.*_\d{2})_urlcounts.txt')
    from os import listdir
    from os.path import isfile, join
    from PlotView import PlotView
    from ctypes import c_int64
    mypath = "files"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    formalaccount = ['nytimes','cnnbrk','BBCBreaking','CNN','ABC','NBCNews']
    colors = ['r','g','b','c','m','y']

    '''
     at each time
     how many new urls appear
    '''

    painter = PlotView()
    plt = painter.getPLT()
    ax = painter.subPlots()
    timeNewUrlAll = [(c_int64(0),set()) for _ in xrange(24)]
    for acnIdx,targetAcn in enumerate(formalaccount):
        url_nofilt = defaultdict(dict)
        url_filt = defaultdict(dict)
        for fn in onlyfiles:
            m = p.match(fn)
            if m:
                acnt = m.group(1)
                if acnt != targetAcn:
                    continue
                dateTimeKey = m.group(2)
                with open(join(mypath,fn)) as fhandler:
                    for [x, y, z] in [l.strip().split('\t') for l in fhandler.readlines()]:
                        if int(y) == 0:
                            continue
                        '''
                            use url_nofilt and url_filt
                            to record the impact of filtering
                        '''

                        url_filt[x][dateTimeKey] = int(y)
                        url_nofilt[x][dateTimeKey] = int(z)


        timeNewUrl = [(c_int64(0),set()) for _ in xrange(24)]

        shift = -5 if targetAcn == 'BBCBreaking' else 0
        for k, v in url_filt.items():
            sorted_v = dict(sorted(v.items(),key=operator.itemgetter(0)))
            [date, idx]= sorted_v.keys()[0].split('_')
            timeNewUrl[int(idx)+shift][0].value += 1
            timeNewUrl[int(idx)+shift][1].add(date)
            timeNewUrlAll[int(idx)+shift][0].value += 1
            timeNewUrlAll[int(idx)+shift][1].add(date)



        painter.plotBar([x for x in xrange(24)],
                        [x.value/(len(y)+1e-10) for (x,y) in timeNewUrl],None,targetAcn,colors[acnIdx],ax, acnIdx)
        plt.legend(loc=2)
    painter.plotLine([x for x in xrange(24)], [x.value/(len(y)+6+1e-10) for (x,y) in timeNewUrlAll],"Average")
    print 'sum', sum([x.value/(len(y)+1e-10) for (x,y) in timeNewUrlAll])
    plt.xlabel("time clock")
    plt.ylabel("number of new URLs")
    #plt.title("New URL at each Time")
    painter.showplot([x for x in xrange(24)])
    print 'finish'

experiment4()
