import numpy as np
import pickle

# -----------------------------------------------------------------------------
with open('DATABASE_863144x42.pckl', 'rb') as f:
    DATABASE, SingleItems = pickle.load(f)

database = DATABASE
singleItems = SingleItems 


# -----------------------------------------------------------------------------
def hminLoop(newItem, database, minsupp, frequentItemSets, supports):
    indices = np.nonzero(
        np.sum(database[:, newItem], axis=1) == len(newItem))[0]
    projectedDB = database[indices, :]
    initialSupports = np.sum(projectedDB, axis=0)
    suffixes = np.nonzero(initialSupports >= minsupp)[0]
    suffixes = suffixes[np.nonzero(suffixes > newItem[-1])[0]]
    for suffix in suffixes:
        itemSet = 1 * newItem
        itemSet.append(suffix)
        frequentItemSets.append(itemSet)
        supports.append(initialSupports[suffix])
        (frequentItemSets, supports) = hminLoop(
            itemSet, projectedDB, minsupp, frequentItemSets, supports)
    return (frequentItemSets, supports)


minsupp = 777777
# -----------------------------------------------------------------------------

#
initialSupports = np.sum(database, axis=0)

# items to be remained
itemsToBeRemained = np.nonzero(initialSupports >= minsupp)[0]

# new database with items to be remained
database = database[:, itemsToBeRemained]

# new single items of items to be remained
singleItems = singleItems[itemsToBeRemained]

# initial supports of items to be remained
initialSupports = initialSupports[itemsToBeRemained]

# num of items of to be remained
numOfItems = singleItems.shape[0]

frequentItemSets = []
supports = []


# -----------------------------------------------------------------------------
for item in range(0, numOfItems):
    newItem = [item]
    frequentItemSets.append(newItem)
    supports.append(initialSupports[item])
    (frequentItemSets, supports) = hminLoop(
        newItem, database, minsupp, frequentItemSets, supports)

# -----------------------------------------------------------------------------
I = np.argsort(-np.array(supports))
frequentItemSets = [frequentItemSets[i] for i in I]
supports = [supports[i] for i in I]
for i in range(0, len(frequentItemSets)):
    itemset = frequentItemSets[i]
    tmp = " "
    for j in itemset:
        tmp = tmp + singleItems[j]
    print('#', i+1, tmp, 'Supp:', (supports[i]*2)/10, ' => ', supports[i])


with open('FIMresults', 'wb') as f:
    pickle.dump([frequentItemSets, supports, singleItems, database], f)
