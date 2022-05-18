from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

#                     A  B  C  D  E
DATABASE = np.array([[1, 1, 1, 0, 0],
                     [1, 0, 0, 0, 1],
                     [0, 1, 0, 1, 1],
                     [1, 0, 0, 1, 1],
                     [1, 1, 1, 0, 0],
                     [1, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0],
                     [0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 1],
                     [1, 1, 1, 0, 1],
                     ],)

SingleItems = np.array(["A", "B", "C", "D", "E"])
# ------------------------------------------------------------------------------

def ConstructTree(DATABASE, OCCS, SingleItems, MinAbsSupp):
    supports = np.sum(DATABASE*OCCS.reshape(-1, 1), axis=0)
    I = np.argsort(-supports)
    DATABASE = DATABASE[:, I]
    SingleItems = SingleItems[I]
    supports = supports[I]
    NODES = np.array([-1])
    treeItems = np.array([-1])
    counts = np.array([-1])
    I = np.nonzero(MinAbsSupp <= supports)[0]
    if I.shape[0] > 0:
        for trind in range(0, DATABASE.shape[0]):
            transaction = DATABASE[trind, :]
            if sum(transaction) > 0:
                transactionIndices = np.nonzero(transaction == 1)[0]
                if trind == 0:
                    NODES = np.array([-1])
                    treeItems = np.array([-1])
                    counts = np.array([-1])
                    for j in range(0, len(transactionIndices)):
                        NODES = np.hstack((NODES, [j]))
                        treeItems = np.hstack(
                            (treeItems, [transactionIndices[j]]))
                        counts = np.hstack((counts, [OCCS[trind]]))
                else:
                    parentIndex = 0
                    index = 0
                    loop = 1
                    while loop:
                        I = np.nonzero(NODES == parentIndex)[0]
                        childNodeItems = []
                        childNodeIndices = []
                        for i in I:
                            childNodeItems.append(treeItems[i])
                            childNodeIndices.append(i)
                        I = np.nonzero(
                            transactionIndices[index] == childNodeItems)[0]
                        if I.shape[0] > 0:
                            counts[childNodeIndices[I[0]]] += OCCS[trind]
                            parentIndex = childNodeIndices[I[0]]
                            index += 1
                        else:
                            loop = 0
                        if index == transactionIndices.shape[0]:
                            loop = 0

                    for i in range(index, transactionIndices.shape[0]):
                        NODES = np.hstack((NODES, [parentIndex]))
                        treeItems = np.hstack(
                            (treeItems, [transactionIndices[i]]))
                        counts = np.hstack((counts, [OCCS[trind]]))
                        parentIndex = len(NODES) - 1
            PlotTree(NODES, treeItems, counts, SingleItems)
    return NODES, treeItems, counts, DATABASE, SingleItems


# ------------------------------------------------------------------------------


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
# ------------------------------------------------------------------------------


def FindEqualTo(itm, X):
    I = [i for i in range(0, len(X)) if X[i] == itm]
    return I
# ------------------------------------------------------------------------------


def FindTheLeavesInTheTree(parent, Leaves, dpth, DEPTH, NODES):
    IndexOfChilds = np.array(FindEqualTo(parent, NODES))
    if len(IndexOfChilds) == 0:
        Leaves.append(parent)
    else:
        dpth = dpth + 1
        DEPTH[IndexOfChilds] = dpth
        for i in range(0, IndexOfChilds.size):
            parent = IndexOfChilds[i]
            [Leaves, DEPTH] = FindTheLeavesInTheTree(
                parent, Leaves, dpth, DEPTH, NODES)
    return Leaves, DEPTH
# ------------------------------------------------------------------------------


def treelayout(NODES):
    parent = 0
    Leaves = []
    dpth = 1
    DEPTH = np.ones((len(NODES)), dtype=int)
    [Leaves, DEPTH] = FindTheLeavesInTheTree(
        parent, Leaves, dpth, DEPTH, NODES)
    MaxDepth = max(DEPTH)

    dx = 1/(len(Leaves)+1)
    dy = 1/(MaxDepth+1)

    # ...vertical coordinates
    y = 1-DEPTH*dy

    # ...horizontal coordinates of the leaves
    x = np.zeros(len(y), dtype='float64')
    for i in range(0, len(Leaves)):
        itm = Leaves[i]
        x[itm] = (i+1)*dx

    # ...horizontal coordinates of remaining nodes
    for dpth in range(MaxDepth-1, 0, -1):
        items = np.array(FindEqualTo(dpth, DEPTH))
        for i in range(0, len(items)):
            parent = items[i]
            IndexOfChilds = np.array(FindEqualTo(parent, NODES))
            if DEPTH[parent] == dpth:
                if len(IndexOfChilds) > 0:
                    x[parent] = mean(x[IndexOfChilds])
    return x, y
# ------------------------------------------------------------------------------


def PlotTree(NODES, TREEITEMS, COUNTS, SingleItems):
    fig, ax = plt.subplots()

    [x, y] = treelayout(NODES)
    plot_loop(0, x, y, NODES)

    circle_facecolor = [.2, .8, 1, 1]
    circle_edgecolor = [.2, .8, 1, 1]
    nodeindex_color = [0, 0, 0, 1]
    circle = Circle((x[0], y[0]), 0.03, fc=circle_facecolor,
                    ec=circle_edgecolor, fill=True, linewidth=0.5)
    ax.add_patch(circle)
    plt.text(x[0], y[0], 'root', weight='bold', color=nodeindex_color, fontsize=10,
             family='calibri', style='normal', horizontalalignment='center', verticalalignment='center')
    for j in range(1, len(x)):
        circle = Circle((x[j], y[j]), 0.03, fc=circle_facecolor,
                        ec=circle_edgecolor, fill=True, linewidth=0.5)
        ax.add_patch(circle)
        plt.text(x[j], y[j], str(j), weight='bold', color=nodeindex_color, fontsize=10,
                 family='calibri', style='normal', horizontalalignment='center', verticalalignment='center')

    for j in range(1, len(x)):
        tmp = SingleItems[TREEITEMS[j]]
        plt.text(x[j]+0.03, y[j], tmp+':'+str(COUNTS[j]), color=[1, 0, 0, 1], fontsize=10,
                 family='consolas', style='normal', horizontalalignment='left', verticalalignment='center')
        plt.text(x[j]+0.03, y[j], tmp, color=[0, 0, 0, 1], fontsize=10, family='consolas',
                 style='normal', horizontalalignment='left', verticalalignment='center')

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
    return
# -----------------------------------------------------------------------------


def plot_loop(parent, x, y, NODES):
    IndexOfChilds = np.array(FindEqualTo(parent, NODES))
    for i in range(0, len(IndexOfChilds)):
        child = IndexOfChilds[i]
        plt.plot(x[[parent, child]], y[[parent, child]],
                 color=[.2, .8, 1, 1], linewidth=0.5)
        plot_loop(child, x, y, NODES)
    return
# ------------------------------------------------------------------------------


OCCS = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
MinAbsSupp = 2
ConstructTree(DATABASE, OCCS, SingleItems, MinAbsSupp)