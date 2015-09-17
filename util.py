__author__ = 'siyuqiu'
import numpy as np
from tweetsManager import textManager
from random import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn import neighbors
from sklearn import cross_validation
import operator
class statis:
    def __init__(self, arr):
        self.array = np.array(arr)
    def setArray(self,arr):
        self.array = np.array(arr)
    def getavg(self):
        return np.mean(self.array)
    def getstd(self):
        return np.std(self.array)
    def getmin(self):
        return np.min(self.array)
    def getmax(self):
        return np.max(self.array)
    def getreport(self):
        f ={'avg':self.getavg, 'std':self.getstd, 'max':self.getmax, 'min':self.getmin}
        ret = ""
        for k, v in f.items():
            ret += k+": "+ str(v())+'\n'
        return ret

class dataprepare:
    def __init__(self):
        self.tweetmanager = textManager()
    def cleantext(self, fname):

        ff = open(fname.split('.')[0]+'_cleaned.txt','w')
        with open(fname) as f:
            for l in f.readlines():
                tokens = self.tweetmanager.tokenizefromstring(l)
                for t in tokens:
                    try:
                        ff.write(t.encode('utf-8')+" ")
                    except:
                        pass
                ff.write('\n')
        f.close()
        ff.close()
    def labeldata(self,f1,f2):
        ls = [(l[:-1],1) for l in open(f1,'r').readlines()] + [(l[:-1],0) for l in open(f2,'r').readlines()]
        shuffle(ls)
        f = open('train.txt','w')
        for l in ls:
            f.write(l[0]+'\t'+str(l[1])+'\n')
        f.close()


    def avgch(self,ws):
        total = reduce(lambda x,y: x+len(y), ws,0)
        return round(total/(len(ws)+1e-10),2)
    def genfeature(self,ls_x):
        '''
        a. Shallow features
	        1. number of words in the sentence (normalize)
	        2. average number of characters in the words
            3. percentage of stop words
	        4. minimum, maximum and average inverse document frequency
        :param ls_x: sencences X without label
        :return:
        '''

        vectorizer = TfidfVectorizer(stop_words='english', min_df=5,smooth_idf=True, sublinear_tf=False,
                 use_idf=True)
        tfidf = vectorizer.fit_transform(ls_x)
        array = tfidf.toarray()
        X = []
        append = X.append
        maxtoken = 0
        for idx,l in enumerate(ls_x):
            ws = l.split()
            maxtoken = max(len(ws),maxtoken)
            stops = round(reduce(lambda x,y: x+1 if y in self.tweetmanager.stop else x, ws,0)/(len(ws)+1e-10),2)
            append( [len(ws),self.avgch(ws),stops
                 , min(array[idx]), max(array[idx]), sum(array[idx])/len(array[idx])])

        return [[round(x[0]*1.0/maxtoken,2)] + x[1:]  for x in X]

    def crossvalidation(self, rawX, Y):
        trainF = self.genfeature(rawX)
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(trainF, Y, test_size=0.4, random_state=0)
        clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
        print 'svc linear', clf.score(X_test, y_test),clf.coef_
        clf = SGDClassifier(loss="hinge", penalty="l2").fit(X_train,y_train)
        print 'SGDC hinge/l2',clf.score(X_test,y_test),clf.coef_
        clf = neighbors.KNeighborsClassifier(5 , weights='uniform').fit(X_train,y_train)
        print 'KNN 5/uniform',clf.score(X_test,y_test)

    def genParaphrase(self, fname):
        tweet = {}
        ret = []
        with open(fname) as f:
            for l in f.readlines():
                if len(l.strip()) == 0:
                    sorted_x = dict(sorted(tweet.items(), key=operator.itemgetter(1)))
                    ret.append([k for k,v in sorted_x.items() if v > 1])
                    tweet.clear()
                    continue
                try:
                    tweet[l] += 1
                except:
                    tweet[l] = 1
        return ret

