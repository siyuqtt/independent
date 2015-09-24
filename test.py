from util import dataprepare
from tweetsManager import textManager
dp = dataprepare()

mg = textManager()

'''
    play wiht forml tweets
    after run tweetsAccount.py
    1.build dictionary of frequent used words in formal tweets
    2. clean tweets
'''
# from tweetsManager import textManager
# formalfname = 'formaltweets.txt'
# mytextmanager = textManager()
# terms_stop=mytextmanager.tokenize(formalfname)
# (total, sorted_fre) = mytextmanager.getfreword(terms_stop)
# (total_bi, sorted_fre_bi) = mytextmanager.getfrebigram(terms_stop)
# f = open('formalworddic.txt','w')
# mytextmanager.writetofile(f,sorted_fre,total,sorted_fre_bi,total_bi)
# f.close()
# dp.cleantext(formalfname)

'''
    play with informal tweets
    after run tweetsReply
    clean tweets
'''
# informalfname = 'informaltweets.txt'
# dp.cleantext(informalfname)


'''
    genetate labeled data for training

'''
# dp.labeldata(formalfname.split('.')[0]+'_cleaned.txt',
#              informalfname.split('.')[0]+'_cleaned.txt')
#
# alllines = open('train.txt')
# tmp  = [l.split('\t') for l in alllines]
# ls_x = [x[0] for x in tmp]
# Y = [int(x[1]) for x in tmp]
# F = dp.genfeature(ls_x)
# dp.crossvalidation(ls_x,Y)


'''
 try generate paraphrase
'''

# fname = dp.cleantext('urltweets.txt')
# ret = dp.genParaterm(fname)
# f = open('paraterms.txt','w')
# for it in ret:
#     for itt in it:
#         f.write(itt+'\n')
#     f.write('\n')


'''
 filter tweets
 if two have coverage over 90%
 delete the shorter one
'''
def filter(lines):
    todelet =  set()
    for i  in xrange(len(lines)):
        pivot = lines[i]
        for j in xrange(i+1, len(lines)):
            l = lines[j]
            tokens1 = mg.tokenizefromstring(pivot)
            tokens2 = mg.tokenizefromstring(l)
            set1 = set(tokens1)
            set2 = set(tokens2)
            coverage = len(set1 & set2)*1.0/ (max(len(set1),len(set2))+1e-10)
            if coverage > 0.9:
                if len(pivot) < len(l):
                    todelet.add(pivot)
                    pivot = l
                else:
                    todelet.add(l)
    return [l for l in lines if l not in todelet]

with open('files/urltweets_stream.txt') as f:
    lines = f.readlines()
    pivot = None
    group = []
    fout = open('files/urltweets_stream_rm_substr.txt','w')
    for l in lines:
        if len(l.strip()) == 0:
            ret = filter(group)
            for ll in ret:
                fout.write(ll)
            fout.write('\n')
            group = []
            continue
        group.append(l)
    fout.close()



