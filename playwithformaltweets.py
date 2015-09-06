__author__ = 'siyuqiu'


from tweetstext import textManager

mytextmanager = textManager()
terms_stop=mytextmanager.tokenize('formaltweets.txt')
(total, sorted_fre) = mytextmanager.getfreword(terms_stop)
(total_bi, sorted_fre_bi) = mytextmanager.getfrebigram(terms_stop)
f = open('formalworddic.txt','w')
mytextmanager.writetofile(f,sorted_fre,total,sorted_fre_bi,total_bi)
f.close()