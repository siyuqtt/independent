__author__ = 'siyuqiu'
'''
    the test file format of OrMF is
    calculate the similarity score of two adjacent sentences
    each sentence for each line
    A example will be
    t1
    pivot
    t2
    pivot
    t1'
    pivot'
    t2'
    pivot'

'''


def getXY(fname):
    X = []

    lines = [line.decode('utf-8').strip() for line in open(fname).readlines()]
    count = 0
    count2 = 0
    candi =[]
    for line in lines:
        if line == "" and len(candi) > 0:
            count2 += len(candi)-1
            X += [itt for it in zip(candi[:-1],[candi[-1]]*(len(candi)-1)) for itt in it]
            candi = []
            count += 1
        elif line.strip() == "":
            continue
        else:
            [tw, _] = line.strip().split('\t')
            candi.append(tw)

    if len(candi) > 0:
        X += [itt for it in zip(candi[:-1],[candi[-1]]*(len(candi) -1)) for itt in it]
        count2 += len(candi)-1
        count += 1

    print count
    print count2
    return X
X = getXY('files/test.txt')
f = open('files/test_OrMF.txt','w')
for l in X:
    f.write(l.encode('utf-8')+'\n')
f.close()