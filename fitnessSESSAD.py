import json as js
import numpy as np
import fitnessEmployes as fE
from functions import *


def sumWOH_1(mission, inter, solution):
    """
    Renvoie la somme des WOH (heures non travaillées) des missions effectues par chaque intervenant
    """
    somme = 0

    nbTrav, nbNonTravvvv, nbSup = stats_heures(solution)
    nbHeuresTrav = nbTrav
    nbNonTrav = nbNonTravvvv
    for j in range(len(solution)):
        somme += nbNonTrav[j] + nbHeuresTrav[j]
    return (somme)


def sumWOH_tous(mission, inter, solutions):
    nbSol = len(solutions)
    somme = np.zeros(nbSol)
    for i in range(nbSol):
        somme[i] = sumWOH_1(mission, inter, solutions[i])
    return somme


def beta():
    """
    Renvoie la valeur de beta
    """
    return 100 / 45


def moyDist(disEmploy):
    """
    Renvoie la moyenne des distances effectuées par les employes
    """
    moy = 0
    for i in range(len(disEmploy)):
        moy += disEmploy[i]
    return moy / len(disEmploy)


def maxDist(disEmploy):
    """
    Renvoie la distance maximale effectuée par les employes (la distance la plus grande réalisée par 1 employé)
    """
    maxi = 0
    for i in range(len(disEmploy)):
        if disEmploy[i] > maxi:
            maxi = disEmploy[i]
    return maxi


def fitnessSESSAD(mission, inter, solution, dist_1_Semaine):
    """
    Renvoie la fitness SESSAD pour une solution solution
    """
    somme = sumWOH_1(mission, inter, solution)
    kap = fE.kapa()
    bet = beta()
    moyDis = moyDist(dist_1_Semaine)
    maxDis = maxDist(dist_1_Semaine)
    f = (bet * somme + kap * moyDis + kap * maxDis) / 3
    return f



def fitnessSESSAD_tout(mission, inter, solutions, DISTANCE):
    """
    Renvoie la fitness SESSAD pour toutes les solutions
    """
    nbSol = len(solutions)
    fit = np.zeros(nbSol)
    for i in range(nbSol):
        dis1 = fE.distance_employe(activites_intervenants(solutions[i]))
        fit[i] = fitnessSESSAD(mission, inter, solutions[i], dis1)
    return fit




def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = read_sols("TRUE_res.txt")
    #print(SOLUTIONS[0])
    #print(activites_intervenants(SOLUTIONS[0]))
    print(fitnessSESSAD_tout(MISSIONS, INTERVENANTS, SOLUTIONS, MATRICE_DISTANCE))

if __name__ == "__main__":
    main()
