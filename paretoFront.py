'''
Method to take three equally-sized lists and return just the elements which lie
on the Pareto frontier, sorted into order.
'''

import numpy as np

def pareto_frontier_multi(X, Y, Z):
    myListe = [[X[i], Y[i], Z[i]] for i in range(len(X))]
    myArray = np.zeros((len(X), 3))
    for i in range(len(X)):
        myArray[i][0] = X[i]
        myArray[i][1] = Y[i]
        myArray[i][2] = Z[i]
    # Sort on first dimension
    myArray = myArray[myArray[:, 0].argsort()]
    # Add first row to pareto_frontier
    pareto_frontier = myArray[0:1, :]
    # Test next row against the last row in pareto_frontier
    for row in myArray[1:, :]:
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
        solution_correspondante.append(myListe.index(i))

    return pX, pY, pZ, solution_correspondante





#import matplotlib.pyplot as plt
#Xs, Ys = # get your data from somewhere to go here

#Ys =[132.94335445, 137.72940963, 137.01104522, 133.5484552,  135.61765744, 133.26613336, 134.46457897, 133.3384147,  140.35968568, 136.06612801]

#Xs = [ 5.16478757,  6.17605695,  5.98117115,  4.34084136,  6.26172972 , 5.69453693, 5.96983248,  3.88568802, 10.48808275,  6.53983584 ]

#Zs = [77.77777778, 73.33333333, 84.44444444, 71.11111111, 73.33333333, 64.44444444, 68.88888889, 84.44444444, 75.55555556, 80.    ]


# Find lowest values for cost and highest for savings
#p_front = pareto_frontier(Xs, Ys, Zs, minX= False, minY= True, minZ= True)
# Plot a scatter graph of all results
#fig = plt.figure()
#ax = fig.gca(projection='3d')  # Affichage en 3D
#ax.scatter(Xs, Ys, Zs, label='Courbe', marker='d')  # Tracé des points 3D
# Then plot the Pareto frontier on top
#plt.plot(p_front[0], p_front[1],p_front[2], color='red')
#plt.show()

#print(p_front)





