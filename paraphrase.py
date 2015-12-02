__author__ = 'siyuqiu'


from twitter_sentence_spliter import *
from metric import *
from nltk.metrics.distance import edit_distance
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
    def arr2ArrPink(self,tarArr,refArr):
        score = []
        for l1 in tarArr:
            score.append(self.one2ArrPink(l1,refArr))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0

    def arrTokens2ArrTokensJacquard(self,tarArrTokens,refArrTokens):
        score = []
        for l in tarArrTokens:
           score.append(self.oneTokens2ArrTokensJacquard(l,refArrTokens))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0


    def one2ArrPink(self,sent,arr):
        score = []
        for l in arr:
            score.append(pinc(sent,l))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0

    def oneTokens2ArrTokensJacquard(self,tkTarget,arrTokens):
        score = []
        for tkRef in arrTokens:
            score.append(JaccardSimToken(tkTarget,tkRef))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0

    def Pink(self, arr):
        l = len(arr)
        score = []
        for i in xrange(l-1):
            for j in xrange(i+1, l):
                score.append(pinc(arr[i], arr[j]))

        if len(score) != 0:
            self.pink = sum(score)*1.0/len(score)
        return self.pink

    def Jacquard(self,arrTokens):
        l = len(arrTokens)
        score = []
        for i in xrange(l-1):
            for j in xrange(i+1, l):
                score.append(JaccardSimToken(arrTokens[i],arrTokens[j]))

        if len(score) != 0:
            self.jacquard = sum(score)*1.0/len(score)
        return self.jacquard

    def one2ArrEditDistance(self,sen,arr):
        score = []
        for l in arr:
            score.append(edit_distance(sen,l))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0

    def arr2ArrEditDistance(self,tarArr,refArr):
        score = []
        for t in tarArr:
            score.append(self.one2ArrEditDistance(t,refArr))
        if len(score) != 0:
            return sum(score)*1.0/len(score)
        return 0




# p = re.compile(r'@(.*)_(.*)_urlcounts.txt')
# from os import listdir
# from os.path import isfile, join
# formalaccount = ['@nytimes','@cnnbrk','@BBCBreaking','@CNN','@ABC','@NBCNews']
# mypath = "Nov3/files"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# acnt_para = {}
# for acnt in formalaccount:
#     acnt_para[acnt]={}
#     acnt_para[acnt]['pink'] = statis(None)
#     acnt_para[acnt]['jacquard'] = statis(None)
#     for fn in onlyfiles:
#         if fn.startswith('urltweets_acnt_'+acnt):
#             with open(join(mypath, fn)) as f:
#                 candi =[]
#                 for l in f:
#                     if len(l.strip()) > 0:
#                         candi.append(l.strip())
#                     else:
#                         filtered_candi = filterUniqSentSet(candi)
#                         tmpParaObj = ParaPrase()
#                         tmpParaObj.setfilterCandi(filtered_candi)
#                         tmpParaObj.setorigCandi(candi)
#                         acnt_para[acnt]['pink'].appendArray(tmpParaObj.Pink())
#                         acnt_para[acnt]['jacquard'].appendArray(tmpParaObj.Jacquard())
#                         candi =[]
#     acnt_para[acnt]['pink'].setFromPlainArr()
#     acnt_para[acnt]['jacquard'].setFromPlainArr()
#     print acnt
#     print "pink"
#     print acnt_para[acnt]['pink'].getreport()
#     print "jacquard"
#     print acnt_para[acnt]['jacquard'].getreport()
#
