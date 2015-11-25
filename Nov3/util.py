__author__ = 'siyuqiu'
import numpy as np
from scipy.stats import norm
from tweetsManager import textManager
from random import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn import neighbors
from sklearn import cross_validation
import string
import re
from math import *
from collections import Counter
import operator
import wordnetutil
from sklearn.cluster import KMeans
from collections import defaultdict
import warnings

warnings.simplefilter("error")
class statis:

    def __init__(self, arr):
        if arr:
            self.array = np.array(arr)
        self.plain_arr = []

    def setArray(self,arr):
        self.array = np.array(arr)

    def appendArray(self,num):
        self.plain_arr.append(num)

    def getPlainArr(self):
        return self.plain_arr

    def setFromPlainArr(self):
        self.array = np.array(self.plain_arr)

    def getavg(self):
        try:
            return np.mean(self.array)
        except:
            return  0

    def getstd(self):
        try:
            return np.std(self.array)
        except:
            return 0

    def getmin(self):
        try:
            return np.min(self.array)
        except:
            return 0

    def getmax(self):
        try:
            return np.max(self.array)
        except:
            return 0

    def getreport(self):
        f ={'avg':self.getavg, 'std':self.getstd, 'max':self.getmax, 'min':self.getmin}
        ret = ""
        for k, v in f.items():
            ret += k+": "+ str(v())+'\n'
        return ret

    def getvalue(self,x, mean, std):
        return norm.pdf(x, mean, std)


class dataprepare:
    def __init__(self):
        self.tweetmanager = textManager()
        self.punctuation = list(string.punctuation)
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
        return ff.name.__str__()
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
    def genfeature(self, ls_x):
        '''
        a. Shallow features
	        1. number of words in the sentence (normalize)
	        2. average number of characters in the words
            3. percentage of stop words
	        4. minimum, maximum and average inverse document frequency
        :param ls_x: sencences X without label
        :return:
        '''

        vectorizer = TfidfVectorizer(stop_words='english',smooth_idf=True, sublinear_tf=False,
                 use_idf=True)
        tfidf = vectorizer.fit_transform(ls_x)
        array = tfidf.toarray()
        X = []
        append = X.append
        maxtoken = 0
        for idx,l in enumerate(ls_x):
            ws = l.split()
            maxtoken = max(len(ws),maxtoken)
            try:
                stops = round(reduce(lambda x,y: x+1 if y in self.tweetmanager.stop else x, ws,0)/(len(ws)+1e-10),2)
            except:
                pass

            append([len(ws),self.avgch(ws), stops,
                    min(array[idx]), max(array[idx]), sum(array[idx])/len(array[idx])])

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
                nl = ''.join(ch for ch in l if ch not in self.punctuation)
                if len(nl.strip()) == 0:
                    sorted_x = dict(sorted(tweet.items(), key=operator.itemgetter(1)))
                    ret.append([k for k,v in sorted_x.items() if v > 1])
                    tweet.clear()
                    continue
                try:
                    tweet[nl] += 1
                except:
                    tweet[nl] = 1
        return ret

    def genParaterm(self,fname):
        terms = {}
        result = []
        with open(fname) as f:
            for l in f.readlines():

                if len(l.strip()) == 0:
                    sorted_x = dict(sorted(terms.items(), key=operator.itemgetter(1)))
                    result.append([k for k,v in sorted_x.items() if v > 1])
                    terms.clear()
                    continue
                ret = self.tweetmanager.tokenizefromstring(l)
                for v, w in zip(ret[:-1], ret[1:]):
                    try:
                        terms[v+" "+w] += 1
                    except:
                        terms[v+" "+w] = 1
        return result

class sentenceSimilarity:


    def __init__(self):
        self.WORD = re.compile(r'\w+')

    def excatWordscore(self, text1, text2):
        vector1 = self.text_to_vector(text1)
        vector2 = self.text_to_vector(text2)
        return self.get_cosine(vector1, vector2)


    def groupExcatWordscore(self, candi):
        scores = defaultdict(list)
        l = len(candi)
        ret = []
        total = []
        for i in xrange(l):
            for j in xrange(i+1, l):
                t = self.excatWordscore(candi[i], candi[j])
                scores[i].append(t)
                total.append(t)
                scores[j].append(t)

        # sorted_s = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        # for k in sorted_s[:l/2+1]:
        #     fout.write(candi[k[0]]+'\n')
        # fout.write('\n')
        stat = statis(total)
        avg = stat.getavg()
        std = stat.getstd()
        lower = avg-std
        upper = avg+std
        for k,v in scores.items():
            cur = statis(v)
            cur_avg = cur.getavg()
            if cur_avg > upper or cur_avg < lower:
                continue
            ret.append(candi[k])
        return ret

    def get_cosine(self,vec1, vec2):
         intersection = set(vec1.keys()) & set(vec2.keys())
         numerator = sum([vec1[x] * vec2[x] for x in intersection])

         sum1 = sum([vec1[x]**2 for x in vec1.keys()])
         sum2 = sum([vec2[x]**2 for x in vec2.keys()])
         denominator = sqrt(sum1) * sqrt(sum2)

         if not denominator:
            return 0.0
         else:
            return float(numerator) / denominator

    def text_to_vector(self,text):
         words = self.WORD.findall(text)
         return Counter(words)

    def buildEmbedding(self):
        self.w2v = {}
        with open('files/glove.twitter.27B.50d.txt') as f:
            for line in f:
                pts = line.split()
                self.w2v[pts[0]] = [float(x) for x in pts[1:]]
        f.close()


    def sentenceEmbedding(self, line):
        token = line.split()
        count = 0
        ret = [0 for _ in xrange(len(self.w2v[self.w2v.keys()[0]]))]
        for t in token:
            if self.w2v.has_key(t):
                ret = map(operator.add, ret, self.w2v[t])
                count += 1

        if count == 0:
            return ret
        else:
            return [x/count for x in ret]

    def square_rooted(self,x):
        return round(sqrt(sum([a*a for a in x])),3)

    def similarity(self,x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)+1e-10
        return round(numerator/float(denominator),3)

    def embeddingScore(self,  candi):
        scores = {}
        embed = {}
        ret = []
        total = []
        for idx,c in enumerate(candi):
            embed[idx] = self.sentenceEmbedding(c)
        l = len(candi)
        for i in xrange(l):
            try:
                scores[i] += 0
            except:
                scores[i] = 0
            for j in xrange(i+1, l):
                t = self.similarity(embed[i], embed[j])
                # assert t is not None
                scores[i] += t
                total.append(t)
                try:
                    scores[j] += t
                except:
                    scores[j] = t
            try:
                scores[i] /= (l-1)
            except:
                pass
        # sorted_s = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        # for k in sorted_s[:l/2+1]:
        #     fout.write(candi[k[0]]+'\n')
        # fout.write('\n')
        # stat = statis(total)
        # std = stat.getstd()
        # avg = stat.getavg()
        try:
            threshold = sum(total)/len(total)
        except:
            threshold = 0
        print 'embedding',threshold
        for k,v in scores.items():
            if v > threshold:
                ret.append(candi[k])
        return ret

    def wordNetScore(self,candi):

        scores = {}
        l = len(candi)
        ret = []
        total = []
        for i in xrange(l):
            try:
                scores[i] += 0
            except:
                scores[i] = 0
            for j in xrange(i+1, l):
                c1 = re.sub(r'[^\w\s]+','',candi[i])
                c2 = re.sub(r'[^\w\s]+','',candi[j])
                t = wordnetutil.similarity(c1,c2,True)
                total.append(t)
                scores[i] += t
                try:
                    scores[j] += t
                except:
                    scores[j] = t
            try:
                scores[i] /= (l-1)
            except:
                pass
        # sorted_s = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        # for k in sorted_s[:l/2+1]:
        #     fout.write(candi[k[0]]+'\n')
        # fout.write('\n')
        try:
            threshold = sum(total)/len(total)
        except:
            threshold = 0

        print 'wordnet',threshold
        for k,v in scores.items():
            if v > threshold:
                ret.append(candi[k])
        return ret

    def extracAllword(self,candi):
        words = set()
        for s in candi:
            ws = self.WORD.findall(s)
            for w in ws:
                words.add(w)
        return list(words)


    def KnnClassify(self,candi):
        words = self.extracAllword(candi)
        word_dict = {w:idx for idx, w in enumerate(words)}
        x = [[0 for _ in xrange(len(words))] for _ in xrange(len(candi))]
        if len(x) < 3:
            return candi
        for id, s in enumerate(candi):
            tmp = self.text_to_vector(s)
            for k,v in tmp.items():
                x[id][word_dict[k]] = float(v)

        km = KMeans(n_clusters=3)
        km.fit(x)
        samples = {}
        X_new = km.transform(x)
        # try:
        #     X_new = km.transform(x)
        # except:
        #     print 'mooo'
        for idx, l in enumerate(km.labels_):
            try:
                samples[l][idx] = X_new[idx][l]
            except:
                samples[l] ={}
                samples[l][idx] = X_new[idx][l]
        ret = []
        for k, v in samples.items():
            sortedv = sorted(v.items(), key=operator.itemgetter(1), reverse=True)
            for it in sortedv:
                ret.append(candi[it[0]])
        return ret



