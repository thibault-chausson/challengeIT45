import numpy as np


def alpha(mission):
    """
    Retourne le coefficient alpha de la fonction de cout
    """
    nbMiss = len(mission)
    alpha = 100 / nbMiss
    return alpha


def penalite_1(solution, Mission, Inter):
    """
    Retourne la penalite de la solution
    """
    nbMiss = len(Mission)
    nbInter = len(Inter)
    penalite = 0
    for i in range(nbInter):
        for j in range(nbMiss):
            if solution[i][j] == 1:
                if Mission[j][5] != Inter[i][2]:
                    penalite += 1
    return penalite


def penalite_toutes_solution(Solutions, Mission, Inter):
    """
    Retourne la penalite de chaque solution, en utilisant la fonction penalite_1 qui calcule la pénalité d'une solution
    """
    nbSol = len(Solutions)
    pen = np.zeros(nbSol)
    for i in range(nbSol):
        pen[i] = penalite_1(Solutions[i], Mission, Inter)
    return pen


def fitnessEtudiants_1(solution, Mission, Inter):
    """
    Retourne le fitness d'un solution
    """
    al = alpha(Mission)
    pe = penalite_1(solution, Mission, Inter)
    fitness = al * pe
    return fitness


def fitnessEtudiants_tout(Solutions, Mis, Inter):
    """
    Retourne le fitness de chaque solution pour les étudiants
    """
    nbSol = len(Solutions)
    fit = np.zeros(nbSol)
    for i in range(nbSol):
        fit[i] = fitnessEtudiants_1(Solutions[i], Mis, Inter)
    return fit
