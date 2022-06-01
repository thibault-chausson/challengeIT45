import numpy as np
import random as rd

exempleFitness = [[12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989]
                  ]

exempleFitness2 = [[112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989]
                   ]

def choixParents(fitness): #fonction qui choisit les parents à partir de leur fitness (decroissante) et renvoie les indices des parents
    nbSol = len(fitness)
    ponde = np.zeros(nbSol)
    aux = np.zeros(nbSol)
    for i in range(nbSol):
        aux[i] = 1 / fitness[i]
    for i in range(nbSol):
        ponde[i] = (aux[i] / np.sum(aux))
    Parent1 = rd.choices(range(nbSol), weights=ponde, k=1)
    ponde[Parent1[0]] = 0
    Parent2 = rd.choices(range(nbSol), weights=ponde, k=1)
    return (Parent1[0], Parent2[0])




def reproduction (solution1, solution2, ligDebut, ligFin, colDebut, colFin): #fonction qui realise la reproduction entre deux solutions
    """
    Retourne la solution fille
    Attention : la ligne de fin et col de fin a eu un +1 pour palier au range qui fait -1
    """
    nblig = len(solution1)
    nbcol = len(solution1[0])
    fille = solution1.copy()
    for i in range(ligDebut, ligFin+1):
        for j in range(colDebut, colFin+1):
            fille[i][j] = solution2[i][j]
    return fille

print(reproduction(exempleFitness, exempleFitness2, 1,2,3,6 ))
