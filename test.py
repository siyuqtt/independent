# from util import dataprepare
# from tweetsManager import textManager
# dp = dataprepare()
#
# mg = textManager()
#
# '''
#     play wiht forml tweets
#     after run tweetsAccount.py
#     1.build dictionary of frequent used words in formal tweets
#     2. clean tweets
# '''
# # from tweetsManager import textManager
# # formalfname = 'formaltweets.txt'
# # mytextmanager = textManager()
# # terms_stop=mytextmanager.tokenize(formalfname)
# # (total, sorted_fre) = mytextmanager.getfreword(terms_stop)
# # (total_bi, sorted_fre_bi) = mytextmanager.getfrebigram(terms_stop)
# # f = open('formalworddic.txt','w')
# # mytextmanager.writetofile(f,sorted_fre,total,sorted_fre_bi,total_bi)
# # f.close()
# # dp.cleantext(formalfname)
#
# '''
#     play with informal tweets
#     after run tweetsReply
#     clean tweets
# '''
# # informalfname = 'informaltweets.txt'
# # dp.cleantext(informalfname)
#
#
# '''
#     genetate labeled data for training
#
# '''
# # dp.labeldata(formalfname.split('.')[0]+'_cleaned.txt',
# #              informalfname.split('.')[0]+'_cleaned.txt')
# #
# # alllines = open('train.txt')
# # tmp  = [l.split('\t') for l in alllines]
# # ls_x = [x[0] for x in tmp]
# # Y = [int(x[1]) for x in tmp]
# # F = dp.genfeature(ls_x)
# # dp.crossvalidation(ls_x,Y)
#
#
# '''
#  try generate paraphrase
# '''
#
# # fname = dp.cleantext('urltweets.txt')
# # ret = dp.genParaterm(fname)
# # f = open('paraterms.txt','w')
# # for it in ret:
# #     for itt in it:
# #         f.write(itt+'\n')
# #     f.write('\n')
#
#
# '''
#  filter tweets
#  if two have coverage over 90%
#  delete the shorter one
# '''
# def filter(lines):
#     todelet =  set()
#     for i  in xrange(len(lines)):
#         pivot = lines[i]
#         for j in xrange(i+1, len(lines)):
#             l = lines[j]
#             tokens1 = mg.tokenizefromstring(pivot)
#             tokens2 = mg.tokenizefromstring(l)
#             set1 = set(tokens1)
#             set2 = set(tokens2)
#             coverage = len(set1 & set2)*1.0/ (max(len(set1),len(set2))+1e-10)
#             if coverage > 0.9:
#                 if len(pivot) < len(l):
#                     todelet.add(pivot)
#                     pivot = l
#                 else:
#                     todelet.add(l)
#     return [l for l in lines if l not in todelet]
#
# with open('files/urltweets_stream.txt') as f:
#     lines = f.readlines()
#     pivot = None
#     group = []
#     fout = open('files/urltweets_stream_rm_substr.txt','w')
#     for l in lines:
#         if len(l.strip()) == 0:
#             ret = filter(group)
#             for ll in ret:
#                 fout.write(ll)
#             fout.write('\n')
#             group = []
#             continue
#         group.append(l)
#     fout.close()
#
#
#

# class Solution(object):
#     def threeSum(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[List[int]]
#         """
#
#         ret = []
#         nums.sort()
#         for i in xrange(len(nums)-2):
#             l,r = i+1, len(nums)-1
#             while l < r:
#                 s = nums[i]+nums[l]+nums[r]
#                 if s == 0:
#                     ret.append([nums[i],nums[l],nums[r]])
#                 elif s < 0:
#                     l += 1
#                     continue
#                 else:
#                     r -= 1
#                     continue
#                 l += 1
#                 while l < r and nums[l] == nums[l-1]:
#                     l += 1
#
#
#
#
#         return ret
# s = Solution()
# print s.threeSum([0,0,0,0])

#
#
# def predorder(root):
#     ret = []
#     while root:
#         cur = root.left
#         if cur is not None:
#             while cur.right and cur.right != root:
#                 cur = cur.right
#             if cur.right is None:
#                 cur.right = root
#                 ret.append(root.val)
#                 root = root.left
#             else:
#                 cur.right = None
#                 root = root.right
#         else:
#             ret.append(root.val)
#             root = root.right
#
#     return ret
# class TreeNode:
#     def __init__(self,x):
#         self.val = x
#         self.right = None
#         self.left = None
#
# root = TreeNode(0)
# root.left = TreeNode(1)
# root.left.right = TreeNode(2)
# root.right = TreeNode(3)
# root.right.right = TreeNode(4)
# root.right.left = TreeNode(5)
#
# print predorder(root)
from operator import add
import operator
import wordnetutil
w2v = {}
with open('files/glove.twitter.27B.25d.txt') as f:
    for line in f:
        pts = line.split()
        w2v[pts[0]] = [float(x) for x in pts[1:]]
f.close()

import re

def sentenceEmbedding(line):
    token = line.split()
    count = 0
    ret = [0 for _ in xrange(len(w2v[w2v.keys()[0]]))]
    for t in token:
        try:
            ret = map(add, ret, w2v[t])
            count += 1
        except:
            pass
    if count == 0:
        return ret
    else:
        return [x/count for x in ret]

from math import*

def square_rooted(x):

   return round(sqrt(sum([a*a for a in x])),3)

def similarity(x,y):

 numerator = sum(a*b for a,b in zip(x,y))
 denominator = square_rooted(x)*square_rooted(y)+1e-10
 return round(numerator/float(denominator),3)



# fout = open('files/embedding_wordsolverlap_filtered.txt','w')
# with open('files/embedding_filtered.txt') as f:
#     candi = []
#     for line in f:
#         line = line.strip()
#         if len(line) != 0:
#             candi.append(line)
#         else:
#             scores = {}
#             embed = {}
#             # for idx,c in enumerate(candi):
#             #     embed[idx] = sentenceEmbedding(c)
#
#             l = len(candi)
#             for i in xrange(l):
#                 try:
#                     scores[i] += 0
#                 except:
#                     scores[i] = 0
#                 for j in xrange(i+1, l):
#                     # s1 = similarity(embed[i], embed[j])
#                     c1 = re.sub(r'[^\w\s]+','',candi[i])
#                     c2 = re.sub(r'[^\w\s]+','',candi[j])
#                     s2 = wordnetutil.similarity(c1,c2,True)
#                     t = s2
#                     scores[i] += t
#                     try:
#                         scores[j] += t
#                     except:
#                         scores[j] = t
#             sorted_s = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
#             for k in sorted_s[:l/2+1]:
#                 fout.write(candi[k[0]]+'\n')
#             fout.write('\n')
#             candi = []
# fout.close()
#
#
#
#
#
#
#
count = 0
cover = 0
with open('files/embedding_filtered.txt') as f:

    for line in f:
        tkns = line.strip().split()
        count += len(tkns)
        for t in tkns:
            if w2v.has_key(t):
                cover += 1


print count
print cover
print cover*100.0/count