__author__ = 'siyuqiu'


from twitter_sentence_spliter import *
from metric import *
from tokenize import *
from util import statis
import re


class ParaPrase:
    def __init__(self):
        self.pink = 0
        self.jacquard = 0
        self.origCandi = []
        self.filteredCandi = []


    def setorigCandi(self, org):
        self.origCandi = org

    def setfilterCandi(self,filt):
        self.filteredCandi = filt

    def getOriLen(self):
        return len(self.origCandi)

    def getFilLen(self):
        return len(self.filteredCandi)

    def Pink(self):
        l = self.getFilLen()
        score = []
        for i in xrange(l-1):
            for j in xrange(i+1, l):
                score.append(pinc(self.filteredCandi[i], self.filteredCandi[j]))

        if len(score) != 0:
            self.pink = sum(score)*1.0/len(score)
        return self.pink

    def Jacquard(self):
        l = self.getFilLen()
        score = []
        for i in xrange(l-1):
            tk_i = tokenizeRawTweetText(self.filteredCandi[i])
            for j in xrange(i+1, l):
                tk_j = tokenizeRawTweetText(self.filteredCandi[j])
                score.append(JaccardSimToken(tk_i,tk_j))

        if len(score) != 0:
            self.jacquard = sum(score)*1.0/len(score)
        return self.jacquard


p = re.compile(r'@(.*)_(.*)_urlcounts.txt')
from os import listdir
from os.path import isfile, join
formalaccount = ['@nytimes','@cnnbrk','@BBCBreaking','@CNN','@ABC','@NBCNews']
mypath = "files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
acnt_para = {}
for acnt in formalaccount:
    acnt_para[acnt]={}
    acnt_para[acnt]['pink'] = statis(None)
    acnt_para[acnt]['jacquard'] = statis(None)
    for fn in onlyfiles:
        if fn.startswith('urltweets_acnt_'+acnt):
            with open(join(mypath, fn)) as f:
                candi =[]
                for l in f:
                    if len(l.strip()) > 0:
                        candi.append(l.strip())
                    else:
                        filtered_candi = filterUniqSentSet(candi)
                        tmpParaObj = ParaPrase()
                        tmpParaObj.setfilterCandi(filtered_candi)
                        tmpParaObj.setorigCandi(candi)
                        acnt_para[acnt]['pink'].appendArray(tmpParaObj.Pink())
                        acnt_para[acnt]['jacquard'].appendArray(tmpParaObj.Jacquard())
                        candi =[]
    acnt_para[acnt]['pink'].setFromPlainArr()
    acnt_para[acnt]['jacquard'].setFromPlainArr()
    print acnt
    print "pink"
    print acnt_para[acnt]['pink'].getreport()
    print "jacquard"
    print acnt_para[acnt]['jacquard'].getreport()

