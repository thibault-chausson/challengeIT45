import numpy as np
import fitnessEmployes as fE
import functions as f


def sumWOH_1(solution, inter, mis):
    """
    Renvoie la somme des WOH (heures non travaillées) des missions effectues par chaque intervenant
    """
    somme = 0

    nbTrav, nbNonTravvvv, nbSup = fE.stats_heures(solution, inter, mis)
    nbHeuresTrav = nbTrav
    nbNonTrav = nbNonTravvvv
    for j in range(len(solution)):
        somme += nbNonTrav[j] + nbHeuresTrav[j]
    return (somme)


def sumWOH_tous(solutions):
    nbSol = len(solutions)
    somme = np.zeros(nbSol)
    for i in range(nbSol):
        somme[i] = sumWOH_1(solutions[i])
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


def fitnessSESSAD(solution, dist_1_Semaine, inter, mis, matrice_distance):
    """
    Renvoie la fitness SESSAD pour une solution solution
    """
    somme = sumWOH_1(solution, inter, mis)
    kap = fE.kapa(matrice_distance, inter)
    bet = beta()
    moyDis = moyDist(dist_1_Semaine)
    maxDis = maxDist(dist_1_Semaine)
    f = (bet * somme + kap * moyDis + kap * maxDis) / 3
    return f


def fitnessSESSAD_tout(mission, inter, solutions, dist):
    """
    Renvoie la fitness SESSAD pour toutes les solutions
    """
    nbSol = len(solutions)
    fit = np.zeros(nbSol)
    for i in range(nbSol):
        dis1 = fE.distance_employe(f.activites_intervenants(solutions[i], inter, mission), dist)
        fit[i] = fitnessSESSAD(solutions[i], dis1, inter, mission, dist)
    return fit
