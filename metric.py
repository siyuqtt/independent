from __future__ import division
from collections import *

def intersect (list1, list2) :
    cnt1 = Counter()
    cnt2 = Counter()
    for tk1 in list1:
        cnt1[tk1] += 1
    for tk2 in list2:
        cnt2[tk2] += 1    
    inter = cnt1 & cnt2
    return len(list(inter.elements()))

def simple_bleu(translation, reference):
    return 1 - pinc(translation, reference)

def pinc ( ssent, csent) :
    s1grams = ssent.split(" ")
    c1grams = csent.split(" ")
    s2grams = []
    c2grams = []
    s3grams = []
    c3grams = []
    s4grams = []
    c4grams = []
        
    for i in range(0, len(s1grams)-1) :
        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i+1]
            s2grams.append(s2gram)
        if i < len(s1grams)-2:
            s3gram = s1grams[i] + " " + s1grams[i+1] + " " + s1grams[i+2]
            s3grams.append(s3gram)
        if i < len(s1grams)-3:
            s4gram = s1grams[i] + " " + s1grams[i+1] + " " + s1grams[i+2] + " " + s1grams[i+3]
            s4grams.append(s4gram)
            
    for i in range(0, len(c1grams)-1) :
        if i < len(c1grams) - 1:
            c2gram = c1grams[i] + " " + c1grams[i+1]
            c2grams.append(c2gram)
        if i < len(c1grams)-2:
            c3gram = c1grams[i] + " " + c1grams[i+1] + " " + c1grams[i+2]
            c3grams.append(c3gram)
        if i < len(c1grams)-3:
            c4gram = c1grams[i] + " " + c1grams[i+1] + " " + c1grams[i+2] + " " + c1grams[i+3]
            c4grams.append(c4gram)

    score = intersect(s1grams, c1grams) / len(c1grams)
    if len(c2grams) > 0:
        score += intersect(s2grams, c2grams) / len(c2grams)
    if len(c3grams) > 0:
        score += intersect(s3grams, c3grams) / len(c3grams)
    if len(c4grams) > 0:
        score += intersect(s4grams, c4grams) / len(c4grams)
    return 1 - score/4

def JaccardSimToken( tokens1, tokens2):

		v1 = set(tokens1)
		v2 = set(tokens2)
		cSum = len(v1 & v2)
		vSum = len(v1 | v2)
		if vSum == 0 :
			vSum = 1
		return cSum *1.0 / vSum
    #print intersect(s1grams, c1grams)   

#inssent = "i am finished ."
#incsent = "i am done ."
#pinc (inssent, incsent)

# inssent = "come , come away ."
# incsent = "come , come away ."
# pinc (inssent, incsent)