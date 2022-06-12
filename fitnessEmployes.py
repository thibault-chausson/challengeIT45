import numpy as np


def stats_heures(solution, intervenant, mission):
    """
    Renvoies des informations sur le nombre d'heures travaillées par les intervenants
    """
    inters = len(intervenant)
    nb_heuresTravaille = np.zeros(inters)
    nb_heuresNonTravaille = np.zeros(inters)
    nb_heureSup = np.zeros(inters)

    for i in range(inters):
        for j in range(len(mission)):
            if solution[i][j] == 1:
                nb_heuresTravaille[i] += (mission[j][3] - mission[j][2]) / 60

        tps = nb_heuresTravaille[i] - intervenant[i][3]
        if tps < 0:
            nb_heuresNonTravaille[i] += abs(tps)
        else:
            nb_heureSup[i] = abs(tps)

    return nb_heuresTravaille, nb_heuresNonTravaille, nb_heureSup


def distance_employe(planning_1_mission, distance_matrice):
    """
    Renvoie la distance effectuée par les employés
    Prend en argument un planning (tableau de tableaux de missions classé par jour et par intervenant)
    Retourne un tableau des distances par semaine pour chaque employé
    """
    nbInter = len(planning_1_mission)
    nbJour = len(planning_1_mission[0])
    distance = np.zeros(nbInter)  # distance par semaine pour un intervenant
    for i in range(nbInter):
        for j in range(1, nbJour + 1):
            nbMissionsJournal = len(planning_1_mission[i][j])
            for k in range(nbMissionsJournal + 1):
                if k == 0:
                    if len(planning_1_mission[i][j]) == 0:
                        distance[i] += 0
                    else:
                        distance[i] += distance_matrice[0][planning_1_mission[i][j][k]]
                elif k == nbMissionsJournal:
                    if len(planning_1_mission[i][j]) == 0:
                        distance[i] += 0
                    else:
                        distance[i] += distance_matrice[planning_1_mission[i][j][k - 1]][0]
                else:
                    if len(planning_1_mission[i][j]) == 0:
                        distance[i] += 0
                    else:
                        distance[i] += distance_matrice[planning_1_mission[i][j][k - 1]][planning_1_mission[i][j][k]]
    return distance


def moyenne_toutes_distances(distance_mat, interve):  # DISTANCES est une matrice carrée
    """
    Renvoie la moyenne de toutes les distances entre le centre et les étudiants, et entre les étudiants et le centre
    """
    somme = 0
    for i in range(len(distance_mat)):
        somme += distance_mat[i][0] + distance_mat[0][i]
    return somme / len(interve)


def kapa(matrice_distance, interve):
    """
    Renvoie la valeur de kapa
    """
    return 100 / moyenne_toutes_distances(matrice_distance, interve)


def zeta(interve):
    """
    Renvoie la valeur de zeta
    """
    return 100 / sum([interve[i][3] for i in range(len(interve))])


def gamma():
    """
    Renvoie la valeur de gamma
    """
    return 10


def fitnessEm(ecart_WH, ecart_OH, ecart_D, intervenants, distance):
    """
    Renvoie la valeur de la fonction de fitness pour les employés
    """
    return (zeta(intervenants) * ecart_WH + gamma() * ecart_OH + kapa(distance, intervenants) * ecart_D) / 3
