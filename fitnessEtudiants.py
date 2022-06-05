import json as js
import numpy as np
from functions import *



def alpha(mission):
    """
    Retourne le coefficient alpha de la fonction de cout
    """
    nbMiss = len(mission)
    alpha = 100 / nbMiss
    return alpha


def penalite_1(solution, MISSION, INTERVENANT):
    """
    Retourne la penalite de la solution
    """
    nbMiss = len(MISSION)
    nbInter = len(INTERVENANT)
    penalite = 0
    for i in range(nbInter):
        for j in range(nbMiss):
            if solution[i][j] == 1:
                if MISSION[j][5] != INTERVENANT[i][2]:
                    penalite += 1
    return penalite

def penalite_toutes_solution(SOLUTIONS, MISSION,INTERVENANT):
    """
    Retourne la penalite de chaque solution, en utilisant la fonction penalite_1 qui calcule la pénalité d'une solution
    """
    nbSol= len(SOLUTIONS)
    pen=np.zeros(nbSol)
    for i in range (nbSol):
        pen[i]=penalite_1(SOLUTIONS[i],MISSION,INTERVENANT)
    return pen


def fitnessEtudiants_1(solution, MISSIONS, INTERVENANTS):
    """
    Retourne le fitness d'un solution
    """
    al = alpha(MISSIONS)
    pe = penalite_1(solution, MISSIONS, INTERVENANTS)
    fitness = al * pe
    return fitness

def fitnessEtudiants_tout(solutions, MISSIONS,INTERVENANTS):
    """
    Retourne le fitness de chaque solution pour les étudiants
    """
    nbSol=len(solutions)
    fit=np.zeros(nbSol)
    for i in range(nbSol):
        fit[i]=fitnessEtudiants_1(solutions[i], MISSIONS, INTERVENANTS)
    return fit


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = read_sols("TRUE_res.txt")
    print(fitnessEtudiants_tout(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
