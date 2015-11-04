# __author__ = 'siyuqiu'
# from tweetsManager import textManager
#
# mymanager = textManager()
# ff = open('formaltweets_cleaned.txt','w')
# with open('formaltweets.txt') as f:
#     for l in f.readlines():
#         tokens = mymanager.tokenizefromstring(l)
#         for t in tokens:
#             try:
#                 ff.write(t.encode('utf-8')+" ")
#             except:
#                 pass
#         ff.write('\n')
# f.close()
# ff.close()
#
#
# ff = open('informaltweets_cleaned.txt','w')
# with open('informaltweets.txt') as f:
#     for l in f.readlines():
#         tokens = mymanager.tokenizefromstring(l)
#         for t in tokens:
#             try:
#                 ff.write(t.encode('utf-8')+" ")
#             except:
#                 pass
#         ff.write('\n')
# f.close()
# ff.close()


from twitter_sentence_spliter import *
p = re.compile(r'urltweets_acnt_@(.*)_(.*)_auto.txt')
from os import listdir
from os.path import isfile, join
mypath = "files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for fn in onlyfiles:
    m = p.match(fn)
    if m:
        fout = open(m.group(1)+'_'+m.group(2)+'_auto_cleaned.txt','w')
        with open(join(mypath, fn)) as f:
            candi =[]
            for l in f:
                if len(l.strip()) > 0:
                    candi.append(l.strip())
                else:
                    filtered_candi = filterUniqSentSet(candi)
                    for c in filtered_candi:
                        fout.write(c.strip()+'\n')
                    fout.write('\n')
                    candi =[]
        fout.close()