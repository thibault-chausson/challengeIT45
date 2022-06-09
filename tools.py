import json as js
import statistics as st
import numpy as np
import random as rd
import copy as cop
import functions as fc
import genetique as g





"""VALEURS TEST"""

exempleFitness = [[12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989]
                  ]

exemple=[[1,2,3,4],
         [5,6,7,8],
         [9,10,11,12],
        [13,14,15,16]]

exempleFitness2 = [[112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989]
                   ]

def choixParents(fitness): #fonction qui choisit les parents à partir de leur fitness (decroissante) et renvoie les indices des parents
    """
    Choix par roulette des parents
    """
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


def choixKill(fitness):
    """
    Choix par roulette des parents
    """
    nbSol = len(fitness)
    ponde = np.zeros(nbSol)
    somme = 0
    for i in range(nbSol):
        somme += fitness[i]
    for i in range(nbSol):
        ponde[i] = (fitness[i] / somme)
    kill1 = rd.choices(range(nbSol), weights=ponde, k=1)
    return (kill1[0])


def reproduction (solution1, solution2, ligDebut, ligFin, colDebut, colFin): #fonction qui realise la reproduction entre deux solutions
    """
    Retourne la solution fille
    Attention : la ligne de fin et col de fin a eu un +1 pour palier au range qui fait -1
    """
    nblig = len(solution1)
    nbcol = len(solution1[0])
    fille = cop.deepcopy(solution1)
    for i in range(ligDebut, ligFin+1):
        for j in range(colDebut, colFin+1):
            fille[i][j] = solution2[i][j]
    return fille

def tri_langage(Mission):
    """
    Tri les missions par le langage des étudiants
    """
    LPC = []
    LSF= []
    for i in range(len(Mission)):
        if Mission[i][4] == "LPC":
            LPC.append(Mission[i])
        else:
            LSF.append(Mission[i])
    return LPC, LSF


def mutation(solution):
    """
    Retourne la solution mutée
    """
    nblig = len(solution)
    nbcol = len(solution[0])
    rdLine1 = rd.randint(0, nblig-1)
    rdCol = rd.randint(0, nbcol-1)
    rdLine2 = rd.randint(0, nblig-1)
    (solution[rdLine1][rdCol], solution[rdLine2][rdCol]) = (solution[rdLine2][rdCol], solution[rdLine1][rdCol])
    return solution

def moyenneFitness(fitness1, fitness2, fitness3):
    """
    Retourne la moyenne des tableaux des Fitness
    """
    nbSol = len(fitness1)
    moyenne = np.zeros(nbSol)
    for i in range(nbSol):
        moyenne[i] = (fitness1[i] + fitness2[i] + fitness3[i]) / 3
    return moyenne

def moyenneFit_1(mission, intervenants, solution_1,distances):
    return (g.choixFitness_1("employe", mission, intervenants, solution_1,distances) + g.choixFitness_1("etudiant", mission, intervenants, solution_1,distances) + g.choixFitness_1("SESSAD", mission, intervenants, solution_1,distances))/3



def main():
    matrice_distance, intervenants, missions = fc.charge_fichier_csv("45-4")
    print(choixKill(exempleFitness2[0]))



if __name__ == "__main__":
    main()