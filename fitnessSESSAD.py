import json as js
import numpy as np
import fitnessEmployes as fE

import functions as fn

def sumWOH_1(mission, inter, solution, distance):
    """
    Renvoie la somme des WOH (heures non travaillées) des missions effectues par chaque intervenant
    """
    somme = 0

    nbTrav, nbNonTravvvv, nbSup = fE.stats_heures(solution, distance, inter, mission)
    nbHeuresTrav = nbTrav
    nbNonTrav = nbNonTravvvv
    for j in range(len(solution)):
        somme += nbNonTrav[j] + nbHeuresTrav[j]
    return (somme)


def sumWOH_tous(mission, inter, solutions, distance):
    nbSol = len(solutions)
    somme = np.zeros(nbSol)
    for i in range(nbSol):
        somme[i] = sumWOH_1(mission, inter, solutions[i], distance)
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


def fitnessSESSAD(mission, inter, solution, dist_1_Semaine, distance):
    """
    Renvoie la fitness SESSAD pour une solution solution
    """
    somme = sumWOH_1(mission, inter, solution, distance)
    kap = fE.kapa(distance, inter, mission)
    bet = beta()
    moyDis = moyDist(dist_1_Semaine)
    maxDis = maxDist(dist_1_Semaine)
    f = (bet * somme + kap * moyDis + kap * maxDis) / 3
    return f

def activites_intervenants(solution, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(solution)):
        missions = {1: [], 2: [], 3: [], 4: [], 5: []}
        edt = {1: [], 2: [], 3: [], 4: [], 5: []}
        for j in range(len(solution[0])):
            if solution[i][j] == 1:
                missions[MISSIONS[j][1]].append((j, MISSIONS[j][2]))
        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)

    return miss_intervenants

def fitnessSESSAD_tout(mission, inter, solutions, DISTANCE):
    """
    Renvoie la fitness SESSAD pour toutes les solutions
    """
    nbSol = len(solutions)
    fit = np.zeros(nbSol)
    for i in range(nbSol):
        dis1 = fE.distance_employe(activites_intervenants(solutions[i], DISTANCE, inter, mission), DISTANCE, inter, mission)
        fit[i] = fitnessSESSAD(mission, inter, solutions[i], dis1, DISTANCE)
    return fit




def main():
    MATRICE_DISTANCE, INTERVENANTS, MISSIONS = fn.charge_fichier_csv("45-45")
    SOLUTIONS = fn.charger_solution("TRUE_res.txt")
    #print(SOLUTIONS[0])
    #print(activites_intervenants(SOLUTIONS[0]))
    print(fitnessSESSAD_tout(MISSIONS, INTERVENANTS, SOLUTIONS, MATRICE_DISTANCE))


if __name__ == "__main__":
    main()
