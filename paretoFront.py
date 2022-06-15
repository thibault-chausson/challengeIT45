'''
Method to take three equally-sized lists and return just the elements which lie
on the Pareto frontier, sorted into order.
'''

import numpy as np
import genetique as gen
import matplotlib.pyplot as plt


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

def pareto_frontier_multi_kill(X,Y,Z):
    myList = [[1/X[i], 1/Y[i], 1/Z[i]] for i in range(len(X))]
    myArray = np.zeros((len(X), 3))
    for i in range(len(X)):
        myArray[i][0] = 1/X[i]
        myArray[i][1] = 1/Y[i]
        myArray[i][2] = 1/Z[i]
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




def affichagePareto (solutions, mission, intervenants, distances):
    fitnessEm = gen.choixFitness_tableau("employe", mission, intervenants, solutions, distances)
    fitnessEt = gen.choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)
    fitnessSe = gen.choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances)
    p_front = pareto_frontier_multi(fitnessEm, fitnessEt, fitnessSe)
    # Find lowest values for cost and highest for savings
    # Plot a scatter graph of all results
    fig = plt.figure()
    ax = fig.gca(projection='3d')  # Affichage en 3D
    fitnessEmDel = np.delete(fitnessEm, p_front[3])
    fitnessEtDel = np.delete(fitnessEt, p_front[3])
    fitnessSeDel = np.delete(fitnessSe, p_front[3])
    ax.scatter(fitnessEmDel, fitnessEtDel, fitnessSeDel, label='Courbe', marker='d')  # Tracé des points 3D
    # Then plot the Pareto frontier on top
    ax.scatter(p_front[0], p_front[1], p_front[2], color='red', label='Pareto frontier')
    plt.title("Solution avec le front de Pareto")
    ax.set_xlabel('Fitness employé')
    ax.set_ylabel('Fitness étudiant')
    ax.set_zlabel('Fitness SESSAD')
    plt.tight_layout()
    plt.show()





