import json as js
import statistics as st
import numpy as np

import functions as fn




def stats_heures(solution, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoies des informations sur le nombre d'heures travaillées par les intervenants
    """
    inters = len(INTERVENANTS)
    nb_heuresTravaille = np.zeros(inters)
    nb_heuresNonTravaille = np.zeros(inters)
    nb_heureSup = np.zeros(inters)


    for i in range(inters):
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                nb_heuresTravaille[i] += (MISSIONS[j][3] - MISSIONS[j][2]) / 60

        tps = nb_heuresTravaille[i] - INTERVENANTS[i][3]
        if tps < 0:
            nb_heuresNonTravaille[i] += abs(tps)
        else:
            nb_heureSup[i] = abs(tps)
    
    return nb_heuresTravaille, nb_heuresNonTravaille, nb_heureSup




"""
def 

(missions, inter, solution_1_planning): #tableau des heures travaillées pour un planning (tableau pour chaque inter)
    nbHeuresTravaille = np.zeros(len(inter))
    for j in range(len(inter)):
        for k in range(len(missions)):
            if (solution_1_planning[j][k] == 1):
                nbHeuresTravaille[j] += (missions[k][3] - missions[k][2]) / 60
    return nbHeuresTravaille


def nombre_heures_non_travaillée_et_sup(nbHeuresTravaille, inter):
    nbHeuresNonTravaillee = np.zeros(len(INTERVENANTS))
    nbHeuresSup = np.zeros(len(INTERVENANTS))
    for j in range(len(INTERVENANTS)):
        heure = INTERVENANTS[j][3] - nbHeuresTravaille[j]
        if (heure > 0):
            nbHeuresNonTravaillee[j] = heure
        else:
            nbHeuresSup[j] = abs(heure)
    return nbHeuresNonTravaillee, nbHeuresSup


def ecart_type(tableau):
    nb = len(tableau)
    sol = np.zeros(nb)
    for i in range(nb):
        sol[i] = st.pstdev(tableau[i])
    return sol

def distance_employs_toutes_missions (solutions, DISTANCES,inter,mis):
    distance_employe = []
    for i in range(len(solutions)):
        planning = activites_intervenants(solutions[i],inter,mis)
        distance_employe.append(distance_employé(DISTANCES, planning))
    return distance_employe
"""


def activites_intervenants(solution, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(INTERVENANTS)):
        missions = {1:[], 2:[], 3:[], 4:[], 5:[]}
        edt = {1:[], 2:[], 3:[], 4:[], 5:[]}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                missions[MISSIONS[j][1]].append((j, MISSIONS[j][2]))

        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)
    
    return miss_intervenants



def distance_employe(planning_1_mission, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie la distance effectuée par les employés
    Prend en argument un planning (tableau de tableaux de missions classé par jour et par intervenant)
    Retourne un tableau des distances par semaine pour chaque employé
    """
    nbInter = len(planning_1_mission)
    nbJour = len(planning_1_mission[0])
    distance = np.zeros(nbInter) #distance par semaine pour un intervenant
    for i in range(nbInter):
        for j in range(1,nbJour+1):
            nbMissionsJournal = len(planning_1_mission[i][j])
            for k in range(nbMissionsJournal+1):
                if k ==0 :
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += MATRICE_DISTANCE[0][planning_1_mission[i][j][k]]
                elif k==nbMissionsJournal:
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += MATRICE_DISTANCE[planning_1_mission[i][j][k-1]][0]
                else:
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += MATRICE_DISTANCE[planning_1_mission[i][j][k-1]][planning_1_mission[i][j][k]]
    return distance


def moyenne_toutes_distances(MATRICE_DISTANCE, INTERVENANTS, MISSIONS): #DISTANCES est une matrice carrée
    """
    Renvoie la moyenne de toutes les distances entre le centre et les étudiants, et entre les étudiants et le centre
    """
    somme = 0
    for i in range(len(MATRICE_DISTANCE)):
        somme += MATRICE_DISTANCE[i][0] + MATRICE_DISTANCE[0][i]
    return somme / len(INTERVENANTS)


def kapa(MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie la valeur de kapa
    """
    return 100 / moyenne_toutes_distances(MATRICE_DISTANCE, INTERVENANTS, MISSIONS)

def zeta(MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie la valeur de zeta
    """
    return 100 / sum([INTERVENANTS[i][3] for i in range(len(INTERVENANTS))])

def gamma():
    """
    Renvoie la valeur de gamma
    """
    return 10

def fitnessEm(ecart_WH, ecart_OH, ecart_D, MATRICE_DISTANCE, INTERVENANTS, MISSIONS):
    """
    Renvoie la valeur de la fonction de fitness pour les employés
    """
    return (zeta(MATRICE_DISTANCE, INTERVENANTS, MISSIONS) * ecart_WH + gamma() * ecart_OH + kapa(MATRICE_DISTANCE, INTERVENANTS, MISSIONS) * ecart_D) / 3


def main():
    SOLUTIONS = fn.charger_solutions("45-4")
    MATRICE_DISTANCE, INTERVENANTS, MISSIONS = fn.charger_fichier_csv("45-4")
    nb_tra, nb_non_tra, nb_sup = stats_heures(SOLUTIONS)
    ecart_dis = st.pstdev(distance_employe(activites_intervenants(SOLUTIONS[0])))
    ecart_WH = st.pstdev(nb_non_tra)
    ecart_OH = st.pstdev(nb_sup)
    print(fitnessEm(ecart_WH, ecart_OH, ecart_dis))

if __name__ == "__main__":
    main()
