import numpy as np
import pickle 

def DoesExist(itm, transaction):
    if sum(transaction[itm]) == len(itm):
        E = 1
    else:
        E = 0
    return E


def CalcAbsSupp(itm, DATABASE):
    absSupp = 0
    for i in range(0, DATABASE.shape[0]):
        transaction = DATABASE[i, :]
        if DoesExist(itm, transaction):
            absSupp += 1
    return absSupp


def CandidateGeneration(fkm1):
    ck = []
    for i in range(0, len(fkm1) - 1):
        for j in range(i + 1, len(fkm1)):

            itemset1 = fkm1[i]
            itemset2 = fkm1[j]

            if all(itemset1[1:] == itemset2[:-1]):
                NewItem = np.hstack((np.array(itemset1), np.array(itemset2[-1])))
                ck.append(NewItem)

    return ck


def ShowDATABASE(DATABASE, SingleItems):
    for i in range(DATABASE.shape[0]):
        tr = DATABASE[i, :]
        I = np.nonzero(tr > 0)[0]
        print(i, ':', SingleItems[I])
    return


DATABASE = np.array([[1, 0, 1, 0, 0, 1],
                     [0, 1, 0, 1, 1, 0],
                     [0, 0, 1, 1, 1, 0],
                     [1, 0, 1, 0, 1, 1],
                     [1, 1, 0, 1, 0, 0],
                     [1, 0, 1, 0, 1, 1],
                     [1, 0, 1, 1, 1, 1],
                     [1, 1, 0, 1, 1, 0],
                     [0, 1, 1, 0, 1, 0],
                     [1, 0, 0, 1, 0, 1],
                     [0, 1, 1, 1, 0, 0]])

SingleItems = np.array(["A", "B", "C", "D", "E", "F"])
minsupp = 4


NumOfTransaction = DATABASE.shape[0]
initial_SUPPORTSs = np.sum(DATABASE, axis=0)
ItemsToBeRemained = np.nonzero(minsupp <= initial_SUPPORTSs)[0]
DATABASE = DATABASE[:, ItemsToBeRemained]
SingleItems = SingleItems[ItemsToBeRemained]

FREQUENTITEMSETS = []
SUPPORTS = []
fk = []

NumOfItems = DATABASE.shape[1]
NumOfTrs = DATABASE.shape[0]

ItemsetIndices = np.arange(0, NumOfItems)

# k=1
for i in range(0, NumOfItems):
    itm = np.array([i])
    abssupp = CalcAbsSupp(itm, DATABASE)
    if abssupp >= minsupp:
        fk.append(itm)
        FREQUENTITEMSETS.append(itm)
        SUPPORTS.append(abssupp)
        # print(FREQUENTITEMSETS[i], abssupp)

# print(fk)
# k=2
loop = 1

while loop:
    fkm1 = fk
    fk = []
    ck = CandidateGeneration(fkm1)
    for i in range(0, len(ck)):
        adayOgeseti = ck[i]
        abssupp = CalcAbsSupp(adayOgeseti, DATABASE)
        if abssupp >= minsupp:
            fk.append(adayOgeseti)
            FREQUENTITEMSETS.append(adayOgeseti)
            SUPPORTS.append(abssupp)
            # k += 1
    if len(ck) * len(fk) == 0:
        loop = 0

I = np.argsort(-np.array(SUPPORTS))
FREQUENTITEMSETS = [FREQUENTITEMSETS[i] for i in I]
SUPPORTS = [SUPPORTS[i] for i in I]
for i in range(0, len(FREQUENTITEMSETS)):
    itemset = FREQUENTITEMSETS[i]
    tmp = " "
    for j in itemset:
        tmp = tmp + SingleItems[j]

    print('#', i + 1, tmp, 'Supp:', SUPPORTS[i])

import pickle

with open('FIMresults', 'wb') as f:
    pickle.dump([FREQUENTITEMSETS, SUPPORTS, SingleItems, DATABASE], f)


import numpy as np
from itertools import combinations
import pickle


try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

def ShowDatabase(DATABASE,SingleItems):
    for i in range(0,DATABASE.shape[0]):
        tr = DATABASE[i,:]
        I = np.nonzero(tr>0)[0]
        itemset = ''
        for itm in SingleItems[I]:
            itemset = itemset + str(itm)
        print(i,':',itemset)
    return

def FindIndex(itemset, FREQUENTITEMSETS):
    I = []
    for k in range(0,len(FREQUENTITEMSETS)):
        tmp = FREQUENTITEMSETS[k]
        if tmp.shape[0] == itemset.shape[0]:
            if all(itemset==tmp):
                I = k
                break
    return I

with open('FIMresults','rb') as f:
    FREQUENTITEMSETS, SUPPORTS, SingleItems, DATABASE = pickle.load(f)
NumOfTransaction = DATABASE.shape[0]
SUPPORTS = [support/ NumOfTransaction for support in SUPPORTS]


MinKulc = 0.50
MinConf = 0.60


for itemset in FREQUENTITEMSETS:
    L = itemset.shape[0]
    if 1 < L:
        I = FindIndex(itemset, FREQUENTITEMSETS)
        SUPPORTitemset = SUPPORTS[I]
        for j in range(1, L):
            CBMN = list(combinations(np.arange(0, L), j))
            CBMN = np.matrix(CBMN)
            for k in range(0, len(CBMN)):
                PrefixIndex = np.array(CBMN[k, :])[0]
                tmp = np.ones(L, dtype='int8')
                tmp[PrefixIndex] = 0
                SuffixIndex = np.nonzero(tmp == 1)[0]
                Prefix = itemset[PrefixIndex]
                Suffix = itemset[SuffixIndex]

                tmpPrefix = ''
                for kk in range(0, np.size(Prefix)):
                    tmpPrefix = tmpPrefix + SingleItems[Prefix[kk]]

                tmpSuffix = ''
                for kk in range(0, np.size(Suffix)):
                    tmpSuffix = tmpSuffix + SingleItems[Suffix[kk]]

                I = FindIndex(Prefix, FREQUENTITEMSETS)
                SUPPORTPrefix = SUPPORTS[I]
                Confidence = SUPPORTitemset / SUPPORTPrefix

                I = FindIndex(Suffix, FREQUENTITEMSETS)
                SUPPORTSuffix = SUPPORTS[I]

                Kulc = 0.5 * (SUPPORTitemset / SUPPORTPrefix + SUPPORTitemset / SUPPORTSuffix)
                Kulc = 2 * (Kulc - 0.5)
                if MinKulc <= Kulc:
                    if MinConf <= Confidence:
                        print(tmpPrefix, '-->', tmpSuffix, '  supp.:' ,"{:.3f}".format(SUPPORTitemset), 'conf.:', "{:.3f}".format(Confidence), 'Kulc.:', "{:.3f}".format(Kulc))