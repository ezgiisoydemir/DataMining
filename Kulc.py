import numpy as np
from itertools import combinations
import pickle 
#--------------------------------------------------------
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass
#-----------------------------------------------------------
def ShowDatabase(DATABASE, SingleItems):
    for i in range(0, DATABASE.shape[0]):
        tr = DATABASE[i,:]
        I = np.nonzero