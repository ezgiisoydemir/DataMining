import numpy as np
# ---------------------------------
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset-f')
except:
    pass
#-------------------------------------------------------------
def dfs_loop(itm,NumOfItems,ITEMSETS):
    tmp = itm[-1]
    for itx in range(tmp+1,NumOfItems):
        NewItem = np.hstack((itm,itx))
        ITEMSETS.append(SingleItems[NewItem])
        print('itemset:', ITEMSETS[-1])
        (ITEMSETS) = dfs_loop(NewItem,NumOfItems,ITEMSETS)
    return ITEMSETS
#---------------------------------------------------------------
SingleItems = np.array(["A","B","C","D","E","F"])
NumOfItems = SingleItems.shape[0]
#---------------------------------------------------------------
ITEMSETS = []
for itm in range(0,NumOfItems):
    itm = np.array([itm])
    ITEMSETS.append(SingleItems[itm])
    print('itemset: ',ITEMSETS[-1])
    (ITEMSETS) = dfs_loop(itm,NumOfItems,ITEMSETS)