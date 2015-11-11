__author__ = 'siyuqiu'
from util import *
from sklearn.linear_model import LogisticRegressionCV
data_feature = dataprepare()
data_semi    =sentenceSimilarity()
logreg = LogisticRegressionCV(cv = 10, solver='newton-cg',multi_class='multinomial')

def getXY(fname):
    Y = []
    features =  []
    with open(fname) as f:
        candi =[]
        for line in f:
            if line.strip() == "" and len(candi) > 0:
                candi_features = data_feature.genfeature(candi)[:-1]
                '''
                    last sentence is the pivot
                '''
                pivot = candi[-1]

                '''
                    exact word over lap
                '''
                exact_word_score = [data_semi.excatWordscore(pivot, l) for l in candi[:-1]]

                '''
                    word net lca
                '''
                clean_pivot = re.sub(r'[^\w\s]+','',pivot)
                lca_score = [wordnetutil.similarity(clean_pivot, re.sub(r'[^\w\s]+', '', l), True) for l in candi[:-1]]
                features += [cf + [s1,s2]for cf,s1,s2 in zip(candi_features,exact_word_score,lca_score)]
                candi = []
                Y.pop()
            elif line.strip() == "":
                continue
            else:
                [tw, label] = line.strip().split('\t')
                candi.append(tw)
                Y.append(int(label))
    return features,Y
X, Y = getXY('files/train.txt')
logreg.fit(X, Y)
test_X, text_Y = getXY('files/test.txt')
print logreg.score(test_X,text_Y)



