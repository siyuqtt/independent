__author__ = 'siyuqiu'
import re
import operator
from nltk.corpus import stopwords
import string
from nltk import bigrams


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
regex_str = [
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

#build dictionary to find frequent used words
freqwords = {}
URLINTEXT_PAT = \
    re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
total = 0
terms_stop = []
for l in open('formaltweets.txt','r').readlines():
    nl = re.sub(URLINTEXT_PAT, '', l.lower())
    ws = tokens_re.findall(nl)
    terms_only = [term for term in ws
              if term not in stop and
              not term.startswith(('#', '@'))]
    terms_stop += terms_only
    for w in terms_only:
        try:
            freqwords[w] += 1
        except:
            freqwords[w] = 1
        total += 1
print total
sorted_fre = sorted(freqwords.items(), key=operator.itemgetter(1))
f  = open('formalworddic.txt','w')

for (k, v) in sorted_fre[::-1]:
    try:
        f.write(k.encode('utf-8')+" ||| " +str(v) + " "+ str(round(v*1.0/total,2))+"\n")
    except:
        pass

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
sorted_bi_fre = sorted(fre_bi.items(),key=operator.itemgetter(1))
for (k, v) in sorted_bi_fre[::-1]:
    try:
        f.write(k[0].encode('utf-8')+" "+k[1].encode('utf-8')+" ||| "+str(v) + " "+ str(round(v*1.0/total_bi,2))+"\n")
    except:
        pass
f.close()