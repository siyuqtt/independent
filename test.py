from util import dataprepare

dp = dataprepare()



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


ret = dp.genParaphrase('urltweets.txt')
f = open('paraphrase.txt','w')
for it in ret:
    for itt in it:
        f.write(itt)
    f.write('\n')