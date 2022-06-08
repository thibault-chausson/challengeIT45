'''
Method to take three equally-sized lists and return just the elements which lie
on the Pareto frontier, sorted into order.
'''

import numpy as np

def pareto_frontier_multi(X,Y,Z):
    myList = [[X[i], Y[i], Z[i]] for i in range(len(X))]
    myArray = np.zeros((len(X), 3))
    for i in range(len(X)):
        myArray[i][0] = X[i]
        myArray[i][1] = Y[i]
        myArray[i][2] = Z[i]
    # Sort on first dimension
    myArray = myArray[myArray[:,0].argsort()]
    # Add first row to pareto_frontier
    pareto_frontier = myArray[0:1,:]
    # Test next row against the last row in pareto_frontier
    for row in myArray[1:,:]:
        if sum([row[x] >= pareto_frontier[-1][x]
                for x in range(len(row))]) != len(row):
            # If it is better on all features add the row to pareto_frontier
            pareto_frontier = np.concatenate((pareto_frontier, [row]))

    pX = []
    pY = []
    pZ = []

    for i in range(len(pareto_frontier)):
        pX.append(pareto_frontier[i][0])
        pY.append(pareto_frontier[i][1])
        pZ.append(pareto_frontier[i][2])

    par = [[pX[i], pY[i], pZ[i]] for i in range(len(pX))]

    solution_correspondante = []

    for i in par:
        solution_correspondante.append(myList.index(i))

    return pX, pY, pZ, solution_correspondante










