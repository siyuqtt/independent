__author__ = 'siyuqiu'
import re
import operator
from nltk.corpus import stopwords
import string
from nltk import bigrams

class textManager:
    def __init__(self):
        self.punctuation = list(string.punctuation)
        self.stop = stopwords.words('english') + self.punctuation + ['rt', 'via']
        self.regex_str = [
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)' # anything else
            ]
        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def tokenizefromstring(self,l):

        nl = re.sub(self.URLINTEXT_PAT, '', l.lower())
        ws = self.tokens_re.findall(nl)
        return [term for term in ws
                  if term not in self.stop and
                  not term.startswith(('#', '@'))]

    def tokenize(self, f):
        #build dictionary to find frequent used words
        terms_stop = []
        for l in open(f,'r').readlines():
            nl = re.sub(self.URLINTEXT_PAT, '', l.lower())
            ws = self.tokens_re.findall(nl)
            terms_only = [term for term in ws
                      if term not in self.stop and
                      not term.startswith(('#', '@'))]
            terms_stop += terms_only
        return terms_stop

    def getfreword(self,terms_stop):
        freqwords={}
        total = 0
        for w in terms_stop:
            try:
                freqwords[w] += 1
            except:
                freqwords[w] = 1
            total += 1
        print total
        return (total,sorted(freqwords.items(), key=operator.itemgetter(1)) )

    def getfrebigram(self,terms_stop):
        terms_bigram = bigrams(terms_stop)
        fre_bi = {}
        total_bi = 0
        for tp in terms_bigram:
            try:
                fre_bi[tp] += 1
            except:
                fre_bi[tp] = 1
            total_bi += 1
        print total_bi
        return(total_bi,sorted(fre_bi.items(),key=operator.itemgetter(1)))


    def writetofile(self,f,sorted_fre,total,sorted_bi_fre,total_bi):
# f  = open('formalworddic.txt','w')
#
        for (k, v) in sorted_fre[::-1]:
            try:
                f.write(k.encode('utf-8')+" ||| " +str(v) + " "+ str(round(v*1.0/total,2))+"\n")
            except:
                pass

        for (k, v) in sorted_bi_fre[::-1]:
            try:
                f.write(k[0].encode('utf-8')+" "+k[1].encode('utf-8')+" ||| "+str(v) + " "+ str(round(v*1.0/total_bi,2))+"\n")
            except:
                pass
# f.close()