__author__ = 'siyuqiu'
from util import *
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import f1_score,precision_score,recall_score
from nltk.stem import porter
from nltk.tokenize import word_tokenize
from nltk.metrics.distance import edit_distance
data_feature = dataprepare()
data_semi    =sentenceSimilarity()
#logreg = LogisticRegressionCV(cv = 10, solver='newton-cg',multi_class='multinomial')
logreg = LogisticRegressionCV(cv = 10, solver='liblinear')
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

def getY(fname):
    Y = []
    lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
    count = 0
    count2 = 0
    candi =[]
    for line in lines:
        if line == "" and len(candi) > 0:
            count2 += len(candi)
            candi = []
            Y.pop()
            count += 1
        elif line.strip() == "":
            continue
        else:
            try:
                [tw, label] = line.strip().split('\t')
            except:
                print 'err'
            candi.append(tw)
            Y.append(int(label))
    if len(candi) > 0:
        count += 1
        count2 += len(candi)
        Y.pop()
    print count,count2, count2 - count
    return Y

# def getXY(fname):
#     Y = []
#     features =  []
#     lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
#     count = 0
#     count2 = 0
#     candi =[]
#     for line in lines:
#         if line == "" and len(candi) > 0:
#             '''
#             Das_genfeature : wei's code
#             gengeafeature: my code
#
#             '''
#             count2 += len(candi)
#             features += Das_genfeature(candi)
#             candi = []
#             Y.pop()
#             count += 1
#         elif line.strip() == "":
#             continue
#         else:
#             [tw, label] = line.strip().split('\t')
#             candi.append(tw)
#             Y.append(int(label))
#     if len(candi) > 0:
#         '''
#             Das_genfeature : wei's code
#             gengeafeature: my code
#
#         '''
#         features += Das_genfeature(candi)
#         count += 1
#         count2 += len(candi)
#         Y.pop()
#     print count,count2, count2 - count
#     return features,Y
def getXY(fname):
    Y = []
    X = []
    lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
    countGroup = 0
    countTweets = 0
    candiX = []
    candiY = []
    for line in lines:
        if line == "" and len(candiX) > 0:

            countTweets += len(candiX)
            X.append(candiX)
            Y.append(candiY)
            candiX = []
            candiY = []
            countGroup += 1
        elif line.strip() == "":
            continue
        else:
            [tw, label] = line.strip().split('\t')
            candiX.append(tw)
            candiY.append(int(label))
    if len(candiX) > 0:

        X.append(candiX)
        Y.append(candiY)
        countGroup += 1
        countTweets += len(candiX)

    print "group: ",countGroup, "tweets: ",countTweets
    return X,Y
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

def EditDistane(candi):
    source = candi[-1]
    features = []
    for t in candi[:-1]:
        features.append(edit_distance(source, t))
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


def OrMFGenFeature(vfilename):
    count = 0
    pivot = None # even line
    sample = None

    vfeatures = []

    for vline in open(vfilename).readlines():
        count += 1
        vline = vline.strip()

        if count % 2 != 0 : #odd line number
            sample = vline.split()
        else:
            pivot = vline.split()
            vsum = [float(i) + float(j) for i, j in zip(pivot, sample)]
            vsub = [abs(float(i) - float(j)) for i, j in zip(pivot, sample)]
            vtogether = vsum + vsub
            vfeatures.append(vtogether)

    return vfeatures

def getOrMF(fname):
    return [float(line.strip()) for line in open(fname).readlines()]



def dropFeatureClass(X,labels, todrop=2):
    newX = []
    newLabels = []
    for (x,y) in zip(X,labels):
        if y == todrop:
            continue
        newX.append(x)
        newLabels.append(y)
    print len(newX)
    return newX,newLabels


def colapTwoClass(labels, l1,l2):
    newLabels= []
    for l in labels:
        if l == l2:
            newLabels.append(l1)
        else:
            newLabels.append(l)
    return newLabels



def combineTwoPrediction(pred1, pred2):
    comPred = []
    for (p1,p2) in zip(pred1,pred2):
        if p1 == 3:
            comPred.append(p1)
        else:
            comPred.append(p2)
    return comPred


def genGoal(arr, goal, other):
    return [other if y != goal else y for y in arr]


def result(method,rule,pred):
    print method,'\t',f1_score(rule, pred, average='binary'),\
        '\t',precision_score(rule, pred,average='binary'),\
        '\t', recall_score(rule, pred, average='binary')

def dropMethod():

    dropOrMFFeatureTrain, dropTrainY = dropFeatureClass(OrMFFeatureTrain,trainY,2)
    dropOrMFFeatureTest, dropTestY = dropFeatureClass(OrMFFeatureTest,testY,2)

    dropOrMFFeatureTrainSim, dropTrainY = dropFeatureClass(OrMFFeaturetrainSim,trainY,2)
    dropOrMFFeatureTestSim, dropTestY = dropFeatureClass(OrMFFeaturetestSim,testY,2)
    dropOrMFFeatureTrainSim = np.array(dropOrMFFeatureTrainSim).reshape(-1,1).tolist()
    dropOrMFFeatureTestSim = np.array(dropOrMFFeatureTestSim).reshape(-1,1).tolist()

    dropLRfeatureTrainX,dropTrainY = dropFeatureClass(featureLRTrainX,trainY,2)
    dropLRfeatureTestX,dropTestY = dropFeatureClass(featureLRTestX,testY,2)

    dropEditfeatureTrainX,dropTrainY = dropFeatureClass(featureEditTrainX,trainY,2)
    dropEditfeatureTestX,dropTestY = dropFeatureClass(featureEditTestX,testY,2)

    dropLexfeatureTrainX,dropTrainY = dropFeatureClass(featureLexTrain,trainY,2)
    dropLexfeatureTestX,dropTestY = dropFeatureClass(featureLexTest,testY,2)
    dropLexfeatureTrainXSim,dropTrainY = dropFeatureClass(featureLexTrainSim,trainY,2)
    dropLexfeatureTestXSim,dropTestY = dropFeatureClass(featureLexTestSim,testY,2)

    dropEmbfeatureTrainX,dropTrainY = dropFeatureClass(featureEmbTrainX,trainY,2)
    dropEmbfeatureTestX,dropTestY = dropFeatureClass(featureEmbTestX,testY,2)
    dropEmbfeatureTrainX = np.array(dropEmbfeatureTrainX).reshape(-1,1).tolist()
    dropEmbfeatureTestX = np.array(dropEmbfeatureTestX).reshape(-1,1).tolist()

    ruleTrainY = genGoal(dropTrainY,1,0)
    ruleTestY = genGoal(dropTestY,1,0)


    logreg.fit(dropOrMFFeatureTrain, ruleTrainY)
    predOrMF = logreg.predict(dropOrMFFeatureTest)
    result('OrMF(vec)',ruleTestY,predOrMF)
    logreg.fit(dropOrMFFeatureTrainSim, ruleTrainY)
    predOrMF = logreg.predict(dropOrMFFeatureTestSim)
    result('OrMF(sim)',ruleTestY,predOrMF)


    logreg.fit(dropLRfeatureTrainX,ruleTrainY)
    predLR = logreg.predict(dropLRfeatureTestX)
    result('LR',ruleTestY,predLR)

    logreg.fit(dropEditfeatureTrainX,ruleTrainY)
    predEdit = logreg.predict(dropEditfeatureTestX)
    result('Edit',ruleTestY,predEdit)

    logreg.fit(dropLexfeatureTrainX,ruleTrainY)
    predLex = logreg.predict(dropLexfeatureTestX)
    result('Lex(vec)',ruleTestY,predLex)
    logreg.fit(dropLexfeatureTrainXSim,ruleTrainY)
    predLex = logreg.predict(dropLexfeatureTestXSim)
    result('Lex(sim)',ruleTestY,predLex)

    logreg.fit(dropEmbfeatureTrainX, ruleTrainY)
    predEm = logreg.predict(dropEmbfeatureTestX)
    result('Embed',ruleTestY,predEm)

def hierachyMethod():
    '''
    step one classing 1&2 with 3
     step two drop class 3
    '''
    colapTestY = colapTwoClass(testY,1,2)
    colapTrainY = colapTwoClass(trainY,1,2)



    dropOrMFFeatureTrain, dropTrainY = dropFeatureClass(OrMFFeatureTrain,trainY,3)
    dropOrMFFeatureTest, dropTestY = dropFeatureClass(OrMFFeatureTest,testY,3)

    dropOrMFFeatureTrainSim, dropTrainY = dropFeatureClass(OrMFFeaturetrainSim,trainY,3)
    dropOrMFFeatureTestSim, dropTestY = dropFeatureClass(OrMFFeaturetestSim,testY,3)
    dropOrMFFeatureTrainSim = np.array(dropOrMFFeatureTrainSim).reshape(-1,1).tolist()
    dropOrMFFeatureTestSim = np.array(dropOrMFFeatureTestSim).reshape(-1,1).tolist()

    dropLRfeatureTrainX,dropTrainY = dropFeatureClass(featureLRTrainX,trainY,3)
    dropLRfeatureTestX,dropTestY = dropFeatureClass(featureLRTestX,testY,3)

    dropEditfeatureTrainX,dropTrainY = dropFeatureClass(featureEditTrainX,trainY,3)
    dropEditfeatureTestX,dropTestY = dropFeatureClass(featureEditTestX,testY,3)

    dropLexfeatureTrainX,dropTrainY = dropFeatureClass(featureLexTrain,trainY,3)
    dropLexfeatureTestX,dropTestY = dropFeatureClass(featureLexTest,testY,3)
    dropLexfeatureTrainXSim,dropTrainY = dropFeatureClass(featureLexTrainSim,trainY,3)
    dropLexfeatureTestXSim,dropTestY = dropFeatureClass(featureLexTestSim,testY,3)

    dropEmbfeatureTrainX,dropTrainY = dropFeatureClass(featureEmbTrainX,trainY,3)
    dropEmbfeatureTestX,dropTestY = dropFeatureClass(featureEmbTestX,testY,3)
    dropEmbfeatureTrainX = np.array(dropEmbfeatureTrainX).reshape(-1,1).tolist()
    dropEmbfeatureTestX = np.array(dropEmbfeatureTestX).reshape(-1,1).tolist()

    def reconstruct(pred):
        ret = []
        idx = 0
        for y in testY:
            if y == 3:
                ret.append(y)
            else:
                ret.append(pred[idx])
                idx += 1
        return ret
    ruleTestY = genGoal(testY,1,0)

    stepOnePredYOrMF = logreg.fit(OrMFFeatureTrain, colapTrainY).predict(OrMFFeatureTest)
    logreg.fit(dropOrMFFeatureTrain, dropTrainY)
    predOrMF = reconstruct(logreg.predict(dropOrMFFeatureTest))
    predOrMF = genGoal(combineTwoPrediction(stepOnePredYOrMF,predOrMF),1,0)
    result('OrMF(vec)',ruleTestY,predOrMF)
    stepOnePredYOrMF = logreg.fit(OrMFFeaturetrainSim, colapTrainY).predict(OrMFFeaturetestSim)
    logreg.fit(dropOrMFFeatureTrainSim, dropTrainY)
    predOrMF = reconstruct(logreg.predict(dropOrMFFeatureTestSim))
    predOrMF = genGoal(combineTwoPrediction(stepOnePredYOrMF,predOrMF),1,0)
    result('OrMF(vec)',ruleTestY,predOrMF)

    stepOnePredYLR = logreg.fit(featureLRTrainX, colapTrainY).predict(featureLRTestX)
    logreg.fit(dropLRfeatureTrainX, dropTrainY)
    predLR = reconstruct(logreg.predict(dropLRfeatureTestX))
    predLR = genGoal(combineTwoPrediction(stepOnePredYLR,predLR),1,0)
    result('LR',ruleTestY,predLR)

    stepOnePredYEdit = logreg.fit(featureEditTrainX, colapTrainY).predict(featureEditTestX)
    logreg.fit(dropEditfeatureTrainX, dropTrainY)
    predEdit = reconstruct(logreg.predict(dropLRfeatureTestX))
    predEdit = genGoal(combineTwoPrediction(stepOnePredYEdit,predEdit),1,0)
    result('LR',ruleTestY,predEdit)

    stepOnePredYLex = logreg.fit(featureLexTrain, colapTrainY).predict(featureLexTest)
    logreg.fit(dropLexfeatureTrainX, dropTrainY)
    predLex = reconstruct(logreg.predict(dropLexfeatureTestX))
    predLex = genGoal(combineTwoPrediction(stepOnePredYLex,predLex),1,0)
    result('Lex(vec)',ruleTestY,predLex)
    stepOnePredYLexSim = logreg.fit(featureLexTrainSim, colapTrainY).predict(featureLexTestSim)
    logreg.fit(dropLexfeatureTrainXSim, dropTrainY)
    predLex = reconstruct(logreg.predict(dropLexfeatureTestXSim))
    predLex = genGoal(combineTwoPrediction(stepOnePredYLexSim,predLex),1,0)
    result('Lex(sim)',ruleTestY,predLex)


    stepOnePredYEm = logreg.fit(featureEmbTrainX, colapTrainY).predict(featureEmbTestX)
    logreg.fit(dropEmbfeatureTrainX, dropTrainY)
    predEmb = reconstruct(logreg.predict(dropEmbfeatureTestX))
    predEmb = genGoal(combineTwoPrediction(stepOnePredYEm,predEmb),1,0)
    result('Embed',ruleTestY,predEmb)


mypath = "oldFiles/"
Y = getY(mypath+'files/train.txt') + getY(mypath+'files/test.txt')
cnt = Counter(Y)
for k,v in cnt.items():
    print k,v, v*1.0/len(Y)



'''
----------
'''
X, Y = getXY(mypath+'files/train.txt')
test_X, test_Y = getXY(mypath+'files/test.txt')
testY =[]
for y in test_Y:
    testY += y[:-1]


trainY = []
for idx, _ in enumerate(Y):
    trainY += Y[idx][:-1]



print 'method\tf1 score\tprecision\trecall'
featureLRTrainX = []
for idx, x in enumerate(X):
    featureLRTrainX += Das_genfeature(x)
featureLRTestX = []
for idx, x in enumerate(test_X):
    featureLRTestX += Das_genfeature(x)

featureEditTrainX = []
for idx, x in enumerate(X):
    featureEditTrainX += EditDistane(x)
featureEditTestX = []
for idx, x in enumerate(test_X):
    featureEditTestX +=  EditDistane(x)

OrMFFeaturetrainSim = getOrMF(mypath+'files/train.sim')
OrMFFeaturetestSim = getOrMF(mypath+'files/test.sim')
OrMFFeaturetrainSim = np.array(OrMFFeaturetrainSim).reshape(-1,1).tolist()
OrMFFeaturetestSim = np.array(OrMFFeaturetestSim).reshape(-1,1).tolist()
OrMFFeatureTrain = OrMFGenFeature(mypath +'files/train_OrMF.txt.ls')
OrMFFeatureTest = OrMFGenFeature(mypath +'files/test_OrMF.txt.ls')

featureLexTrain = []
featureLexTest = []
for idx,x in enumerate(featureLRTrainX):
    featureLexTrain.append(x + OrMFFeatureTrain[idx])
for idx,x in enumerate(featureLRTestX):
    featureLexTest.append(x + OrMFFeatureTest[idx])
featureLexTrainSim = []
featureLexTestSim = []
for idx,x in enumerate(featureLRTrainX):
    featureLexTrainSim.append(x + OrMFFeaturetrainSim[idx])
for idx,x in enumerate(featureLRTestX):
    featureLexTestSim.append(x + OrMFFeaturetestSim[idx])

from util import sentenceSimilarity
mySim = sentenceSimilarity()
mySim.buildEmbedding('glove.twitter.27B.25d.txt')

featureEmbTrainX = []
featureEmbTestX = []
for x in X:
    featureEmbTrainX += mySim.embeddingScore(x)
for x in test_X:
    featureEmbTestX += mySim.embeddingScore(x)


# from sklearn.decomposition import PCA
# pca = PCA(n_components=50)
# OrMFFeatureTrain = (pca.fit_transform(OrMFFeatureTrain)).tolist()
# print(pca.explained_variance_ratio_), sum(pca.explained_variance_ratio_)
# OrMFFeatureTest = pca.transform(OrMFFeatureTest).tolist()




'''

    random guessing : 1,2 3


from random import randint
predY = []
for i in xrange(len(dropTestY)):
    predY.append(randint(1,2))
predY = [0 if y != 1 else 1 for y in predY]
print "random\t",f1_score(goalTestY, predY, average='binary'),'\t',precision_score(goalTestY, predY, average='binary'),
print '\t' , recall_score(goalTestY, predY, average='binary')

'''
'''
    majority guess

'''
# def most_common(lst):
#     return 0 if max(set(lst), key=lst.count) != 1 else 1
# maj = most_common(Y)
# pred_Y = [maj for _ in xrange(len(test_Y))]
# print f1_score(test_Y, pred_Y, average='binary'),'\t',precision_score(test_Y, pred_Y, average='binary'),
# '\t' , recall_score(test_Y, pred_Y, average='binary')
#


