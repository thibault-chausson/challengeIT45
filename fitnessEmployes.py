import json as js
import statistics as st
import numpy as np
from functions import * # EXTREMEMENT IMPORTANT CAR CELA IMPORTE LES VARIABLES GLOBALES



def distance_employe(planning_1_mission):
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


def moyenne_toutes_distances(): #DISTANCES est une matrice carrée
    """
    Renvoie la moyenne de toutes les distances entre le centre et les étudiants, et entre les étudiants et le centre
    """
    somme = 0
    for i in range(len(MATRICE_DISTANCE)):
        somme += MATRICE_DISTANCE[i][0] + MATRICE_DISTANCE[0][i]
    return somme / len(INTERVENANTS)


def kapa():
    """
    Renvoie la valeur de kapa
    """
    return 100 / moyenne_toutes_distances()

def zeta():
    """
    Renvoie la valeur de zeta
    """
    return 100 / sum([INTERVENANTS[i][3] for i in range(len(INTERVENANTS))])

def gamma():
    """
    Renvoie la valeur de gamma
    """
    return 10

def fitnessEm(ecart_WH, ecart_OH, ecart_D):
    """
    Renvoie la valeur de la fonction de fitness pour les employés
    """
    return (zeta() * ecart_WH + gamma() * ecart_OH + kapa() * ecart_D) / 3


def main():
    print(SOLUTIONS[0])
    nb_tra, nb_non_tra, nb_sup = stats_heures(SOLUTIONS[0])
    ecart_dis = st.pstdev(distance_employe(activites_intervenants(SOLUTIONS[0])))
    ecart_WH = st.pstdev(nb_non_tra)
    ecart_OH = st.pstdev(nb_sup)
    print(fitnessEm(ecart_WH, ecart_OH, ecart_dis))

# sorti du main pour pouvoir charger les variables lors de l'import du fichier et lors de l'execution du fichier
# J'ai une technique de gitan pour pouvoir remplacer les arguments que j'implementerais plus tard


if __name__ == "__main__":
    # variables globales à CE programme, pas lors de l'import
    read_sols("TRUE_res.txt")
    charge_fichier_csv("100-10")
    main()
