__author__ = 'siyuqiu'
from tweetsManager import textManager

mymanager = textManager()
ff = open('formaltweets_cleaned.txt','w')
with open('formaltweets.txt') as f:
    for l in f.readlines():
        tokens = mymanager.tokenizefromstring(l)
        for t in tokens:
            try:
                ff.write(t.encode('utf-8')+" ")
            except:
                pass
        ff.write('\n')
f.close()
ff.close()


ff = open('informaltweets_cleaned.txt','w')
with open('informaltweets.txt') as f:
    for l in f.readlines():
        tokens = mymanager.tokenizefromstring(l)
        for t in tokens:
            try:
                ff.write(t.encode('utf-8')+" ")
            except:
                pass
        ff.write('\n')
f.close()
ff.close()