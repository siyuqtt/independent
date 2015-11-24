__author__ = 'siyuqiu'
from util import *
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import f1_score
from nltk.stem import porter
from nltk.tokenize import word_tokenize
data_feature = dataprepare()
data_semi    =sentenceSimilarity()
logreg = LogisticRegressionCV(cv = 10, solver='newton-cg',multi_class='multinomial')

def genfeature(candi):
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
    return [cf + [s1,s2]for cf,s1,s2 in zip(candi_features,exact_word_score,lca_score)]

def getXY(fname):
    Y = []
    features =  []
    lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
    count = 0
    count2 = 0
    candi =[]
    for line in lines:
        if line == "" and len(candi) > 0:
            '''
            Das_genfeature : wei's code
            gengeafeature: my code

            '''
            count2 += len(candi)
            features += Das_genfeature(candi)
            candi = []
            Y.pop()
            count += 1
        elif line.strip() == "":
            continue
        else:
            [tw, label] = line.strip().split('\t')
            candi.append(tw)
            Y.append(int(label))
    if len(candi) > 0:
        '''
            Das_genfeature : wei's code
            gengeafeature: my code

        '''
        features += Das_genfeature(candi)
        count += 1
        count2 += len(candi)
        Y.pop()
    print count,count2, count2 - count
    return features,Y

def intersect (list1, list2) :
    cnt1 = Counter()
    cnt2 = Counter()
    for tk1 in list1:
        cnt1[tk1] += 1
    for tk2 in list2:
        cnt2[tk2] += 1
    inter = cnt1 & cnt2
    return list(inter.elements())

def Das_genfeature(candi):
    source = candi[-1]
    features = []
    for t in candi[:-1]:
        features += [paraphrase_Das_features(source, t).values()]
    return features


def paraphrase_Das_features(source, target):
    source_words = word_tokenize(source)
    target_words = word_tokenize(target)
    eitha = 1e-20
    features = {}

    ###### Word Features ########

    s1grams = [w.lower() for w in source_words]
    t1grams = [w.lower() for w in target_words]
    s2grams = []
    t2grams = []
    s3grams = []
    t3grams = []

    for i in range(0, len(s1grams)-1) :
        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i+1]
            s2grams.append(s2gram)
        if i < len(s1grams)-2:
            s3gram = s1grams[i] + " " + s1grams[i+1] + " " + s1grams[i+2]
            s3grams.append(s3gram)

    for i in range(0, len(t1grams)-1) :
        if i < len(t1grams) - 1:
            t2gram = t1grams[i] + " " + t1grams[i+1]
            t2grams.append(t2gram)
        if i < len(t1grams)-2:
            t3gram = t1grams[i] + " " + t1grams[i+1] + " " + t1grams[i+2]
            t3grams.append(t3gram)

    f1gram = 0
    precision1gram = len(set(intersect(s1grams, t1grams))) / (len(set(s1grams))+eitha)
    recall1gram    = len(set(intersect(s1grams, t1grams))) / (len(set(t1grams))+eitha)
    if (precision1gram + recall1gram) > 0:
        f1gram = 2 * precision1gram * recall1gram / ((precision1gram + recall1gram)+eitha)
    precision2gram = len(set(intersect(s2grams, t2grams))) / (len(set(s2grams))+eitha)
    recall2gram    = len(set(intersect(s2grams, t2grams))) / (len(set(t2grams))+eitha)
    f2gram = 0
    if (precision2gram + recall2gram) > 0:
        f2gram = 2 * precision1gram * recall2gram / (precision2gram + recall2gram +eitha)
    precision3gram = len(set(intersect(s3grams, t3grams))) / (len(set(s3grams))+eitha)
    recall3gram    = len(set(intersect(s3grams, t3grams))) / (len(set(t3grams))+eitha)
    f3gram = 0
    if (precision3gram + recall3gram) > 0:
        f3gram = 2 * precision3gram * recall3gram /(precision3gram + recall3gram +eitha)

    features["precision1gram"] = precision1gram
    features["recall1gram"] = recall1gram
    features["f1gram"] = f1gram
    features["precision2gram"] = precision2gram
    features["recall2gram"] = recall2gram
    features["f2gram"] = f2gram
    features["precision3gram"] = precision3gram
    features["recall3gram"] = recall3gram
    features["f3gram"] = f3gram

    ###### Stemmed Word Features ########

    porterstemmer = porter.PorterStemmer()
    s1stems = [porterstemmer.stem(w.lower()) for w in source_words]
    t1stems = [porterstemmer.stem(w.lower()) for w in target_words]
    s2stems = []
    t2stems = []
    s3stems = []
    t3stems = []

    for i in range(0, len(s1stems)-1) :
        if i < len(s1stems) - 1:
            s2stem = s1stems[i] + " " + s1stems[i+1]
            s2stems.append(s2stem)
        if i < len(s1stems)-2:
            s3stem = s1stems[i] + " " + s1stems[i+1] + " " + s1stems[i+2]
            s3stems.append(s3stem)

    for i in range(0, len(t1stems)-1) :
        if i < len(t1stems) - 1:
            t2stem = t1stems[i] + " " + t1stems[i+1]
            t2stems.append(t2stem)
        if i < len(t1stems)-2:
            t3stem = t1stems[i] + " " + t1stems[i+1] + " " + t1stems[i+2]
            t3stems.append(t3stem)

    precision1stem = len(set(intersect(s1stems, t1stems))) / (len(set(s1stems))+eitha)
    recall1stem    = len(set(intersect(s1stems, t1stems))) / (len(set(t1stems))+eitha)
    f1stem = 0
    if (precision1stem + recall1stem) > 0:
        f1stem = 2 * precision1stem * recall1stem / (precision1stem + recall1stem+eitha)
    precision2stem = len(set(intersect(s2stems, t2stems))) / (len(set(s2stems))+eitha)
    recall2stem    = len(set(intersect(s2stems, t2stems))) / (len(set(t2stems))+eitha)
    f2stem = 0
    if (precision2stem + recall2stem) > 0:
        f2stem = 2 * precision2stem * recall2stem / (precision2stem + recall2stem +eitha)
    precision3stem = len(set(intersect(s3stems, t3stems))) / (len(set(s3stems))+eitha)
    recall3stem    = len(set(intersect(s3stems, t3stems))) / (len(set(t3stems))+eitha)
    f3stem = 0
    if (precision3stem + recall3stem) > 0:
        f3stem = 2 * precision3stem * recall3stem / (precision3stem + recall3stem +eitha)

    features["precision1stem"] = precision1stem
    features["recall1stem"] = recall1stem
    features["f1stem"] = f1stem
    features["precision2stem"] = precision2stem
    features["recall2stem"] = recall2stem
    features["f2stem"] = f2stem
    features["precision3stem"] = precision3stem
    features["recall3stem"] = recall3stem
    features["f3stem"] = f3stem

    return features


def getOrMF(fname):
    return [float(line.strip()) for line in open(fname).readlines()]

X, Y = getXY('files/train.txt')
OrMF_train = getOrMF('files/train_OrMF.sim')
OrMF_test = getOrMF('files/test_OrMF.sim')
for idx,x in enumerate(X):
    x.append(OrMF_train[idx])
test_X, test_Y = getXY('files/test.txt')
for idx,x in enumerate(test_X):
    x.append(OrMF_test[idx])

logreg.fit(X, Y)
pred_Y = logreg.predict(test_X)
fout = open('result.txt','w')
for y in pred_Y:
    fout.write(str(y)+'\n')
fout.close()

print 'f1 score'
print f1_score(test_Y, pred_Y, average='micro')
print logreg.score(test_X,test_Y)

'''
    random guessing : 1,2 3

'''
from random import randint
pred_Y = []
for i in xrange(len(test_Y)):
    pred_Y.append(randint(1,3))
print f1_score(test_Y, pred_Y, average='micro')

'''
    majority guess

'''
def most_common(lst):
    return max(set(lst), key=lst.count)
maj = most_common(Y)
pred_Y = [maj for _ in xrange(len(test_Y))]
print f1_score(test_Y, pred_Y, average='micro')


