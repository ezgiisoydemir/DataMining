import numpy as np
import pickle

# with open('DATABASE_863144x42.pckl', 'rb') as f:
#     DATABASE, SingleItems = pickle.load(f)
    
# database = DATABASE
# singleItems = SingleItems    
def showDatabase(database, singleItems):
    for i in range(database.shape[0]):
        tr = database[i, :]
        I = np.nonzero(tr > 0)[0]
        print(i, ':', singleItems[I])
    return


def transposeDB(database, trs, sI):
    transposeTemp = database.T
    for i in range(transposeTemp.shape[0]):
        tr = transposeTemp[i, :]
        idx = np.nonzero(tr > 0)[0]
        print(sI[i], ':', trs[idx])
    return


# -----------------------------------------------------------------------------
 #                   A  B  C  D  E
DATABASE = np.array([[1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1],
                      [1, 1, 1, 0, 1],
                      [0, 1, 0, 0, 1],
                      [1, 1, 1, 0, 1],
                      ],)


singleItems = np.array(["A", "B", "C", "D", "E"])
trsItems = np.array(["T1", "T2", "T3", "T4", "T5"])
minSupp = 2


# -----------------------------------------------------------------------------
def eclatDfsLoop(itemset, itemsetTIDList, TIDList, minSupp, frequentItemSets, supports, numOfItems):
    # print(singleItems[itemset],
    #       '  -->  ', trsItems[itemsetTIDList], '\n')
    print(singleItems[itemset],
          '  -->  ', itemsetTIDList, '\n')
    temp = itemset[-1]
    for i in range(temp+1, numOfItems):

        newItemSet = 1 * itemset
        newItemSet.append(i)
        newItemSetTIDList = []
        suffixTIDList = 1 * TIDList[i]
        newItemSetTIDList = np.intersect1d(itemsetTIDList, suffixTIDList)
        suppOfNewItemSet = len(newItemSetTIDList)
        if minSupp <= suppOfNewItemSet:
            frequentItemSets.append(newItemSet)
            supports.append(suppOfNewItemSet)
            (frequentItemSets, supports) = eclatDfsLoop(newItemSet, newItemSetTIDList,
                                                        TIDList, minSupp, frequentItemSets, supports, numOfItems)
    return frequentItemSets, supports
# -----------------------------------------------------------------------------

TIDList = []
frequentItemSets = []
supports = []
initialSupports = np.sum(DATABASE, axis=0)
numOfItems = DATABASE.shape[1]

# determine TID list
for i in range(0, numOfItems):
    idx = np.nonzero(DATABASE[:, i] > 0)[0]
    TIDList.append(list(idx))
    
print(TIDList)

# preperation frequent item sets and supports
for i in range(0, numOfItems):
    frequentItemSets.append([i])
    supports.append(initialSupports[i])

# eclat dfs starting down here
print('\nItemsets and TID Lists:\n')
for item in range(0, numOfItems):
    itemset = [item]
    itemsetTIDList = TIDList[item]
    print('-----------------------------------------------------------------------------')
    # print('DFS ', item+1, '. döngü', ' - itemset:', itemset,
    #       singleItems[itemset], ' - itemsetTIDList:', itemsetTIDList, trsItems[itemsetTIDList], '\n')
    print('DFS ', item+1, '. döngü', ' - itemset:', itemset,
          singleItems[itemset], ' - itemsetTIDList:', itemsetTIDList, '\n')
    (frequentItemSets, supports) = eclatDfsLoop(itemset, itemsetTIDList,
                                                TIDList, minSupp, frequentItemSets, supports, numOfItems)


I = np.argsort(-np.array(supports))
frequentItemSets = [frequentItemSets[i] for i in I]
supports = [supports[i] for i in I]
print('\nSUPPORTS:\n')
for i in range(0, len(frequentItemSets)):
    itemset = frequentItemSets[i]
    tmp = " "
    for j in itemset:
        tmp = tmp + singleItems[j]
    print('#', i+1, tmp, 'Supp:', (supports[i]*2)/10, ' => ', supports[i])


with open('EclatResults', 'wb') as f:
    pickle.dump([frequentItemSets, supports,
                singleItems, DATABASE, trsItems], f)