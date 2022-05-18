import numpy as np
# ---------------------------------
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset-f')
except:
    pass
# ---------------------------------
SingleItems = np.array(["A", "B", "C", "D", "E"])
NumOfItems = SingleItems.shape[0]
ITEMSETS = []
tmp = []
for i in range(0,NumOfItems):
    itm = np.array([i])
    tmp.append(itm)
    ITEMSETS.append(SingleItems[itm])
    print('itemset:', ITEMSETS[-1])
for level in range(1,NumOfItems):
    children = tmp; tmp = []
    for prefix in children [:-1]:
        for suffix in range(prefix[-1]+1,NumOfItems):
            itm = np.hstack((np.array(prefix),np.array(suffix)))
            tmp.append(itm)
            ITEMSETS.append(SingleItems[itm])
            print('itemset:',ITEMSETS[-1])