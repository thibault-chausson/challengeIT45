import json as js
import statistics as st
import numpy as np

MATRICE_DISTANCE = []
INTERVENANTS = []
MISSIONS = []

SOLUTIONS = []  # Les lignes representent les formateurs (interfaces) et les colones les missions


def charge_fichier_csv(dossier):
    """
    Charge le contenue du fichier csv dans les variables globales
    """
    with open(f"Instances/{dossier}/Distances.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            MATRICE_DISTANCE.append(list(map(float, ligne.split(','))))

    with open(f"Instances/{dossier}/Intervenants.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            INTERVENANTS.append(ligne.split(','))

    with open(f"Instances/{dossier}/Missions.csv", 'r') as fichier:
        lignes = fichier.read().split('\n')
        if lignes[-1] == '':
            lignes = lignes[:-1]
        for ligne in lignes:
            MISSIONS.append(ligne.split(','))

    # Changements des chiffres de types str en type int
    for i in range(len(INTERVENANTS)):
        for j in range(len(INTERVENANTS[i])):
            try:
                INTERVENANTS[i][j] = int(INTERVENANTS[i][j])
            except:
                pass

    for i in range(len(MISSIONS)):
        for j in range(len(MISSIONS[i])):
            try:
                MISSIONS[i][j] = int(MISSIONS[i][j])
            except:
                pass

    return (MATRICE_DISTANCE, INTERVENANTS, MISSIONS)


def charger_solution(dossier):
    with open(f"./{dossier}", 'r') as f:
        fich = f.read().split('\n\n')[:-1]
    SOLUTIONS = [js.loads(i) for i in fich]
    return SOLUTIONS


def nombre_heures_travaillée(missions, inter, solution_1_planning): #tableau des heures travaillées pour un planning (tableau pour chaque inter)
    nbInter = len(inter)
    nbSol = len(missions)
    nbMiss = len(missions)
    nbHeuresTravaille = np.zeros(nbInter)
    for j in range(nbInter):
        for k in range(nbMiss):
            if (solution_1_planning[j][k] == 1):
                nbHeuresTravaille[j] += (missions[k][3] - missions[k][2]) / 60
    return nbHeuresTravaille


def nombre_heures_non_travaillée_et_sup(nbHeuresTravaille, inter):
    nbInter = len(inter)
    nbHeuresNonTravaillee = np.zeros(nbInter)
    nbHeuresSup = np.zeros(nbInter)
    for j in range(nbInter):
        heure = inter[j][3] - nbHeuresTravaille[j]
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



def activites_intervenants(solution,inter,mis):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(inter)):
        missions = {1: [], 2: [], 3: [], 4: [], 5: []}
        edt = {1: [], 2: [], 3: [], 4: [], 5: []}
        for j in range(len(mis)):
            if solution[i][j] == 1:
                missions[mis[j][1]].append((j, mis[j][2]))
        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)

    return miss_intervenants



def distance_employé (DISTANCES, planning_1_mission):
    nbInter = len(planning_1_mission)
    nbJour=len(planning_1_mission[0])
    distance = np.zeros(nbInter) #distance par semaine pour un intervenant
    for i in range(nbInter):
        for j in range(1,nbJour+1):
            nbMissionsJournal = len(planning_1_mission[i][j])
            for k in range(nbMissionsJournal+1):
                if k ==0 :
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += DISTANCES[0][planning_1_mission[i][j][k]]
                elif k==nbMissionsJournal:
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += DISTANCES[planning_1_mission[i][j][k-1]][0]
                else:
                    if len(planning_1_mission[i][j])==0:
                        distance[i]+=0
                    else:
                        distance[i] += DISTANCES[planning_1_mission[i][j][k-1]][planning_1_mission[i][j][k]]
    return distance

def distance_employs_toutes_missions (solutions, DISTANCES,inter,mis):
    distance_employe = []
    for i in range(len(solutions)):
        planning = activites_intervenants(solutions[i],inter,mis)
        distance_employe.append(distance_employé(DISTANCES, planning))
    return distance_employe


def moyenne_toutes_distances(DISTANCES,inter): #DISTANCES est une matrice carrée
    nbInter = len(inter)
    nbMission = len(DISTANCES)
    somme=0
    for i in range(nbMission):
        somme += DISTANCES[i][0]+DISTANCES[0][i]
    return somme/nbInter


def kapa(DISTANCES,inter):
    moy = moyenne_toutes_distances(DISTANCES, inter)
    kapa = 100 / moy
    return kapa

def gama(inter):
    nbInter = len(inter)
    sumHeureTrav = 0
    for i in range(nbInter):
        sumHeureTrav += inter[i][3]
    gamma = 100 / sumHeureTrav
    return gamma


def fitnessEm(ecart_WH, ecart_OH, ecart_D, inter, DISTANCES): #Pour une seule solution
    zeta = 10
    ga=gama(inter)
    kap = kapa(DISTANCES, inter)
    fitness = (zeta * ecart_WH + ga * ecart_OH + kap * ecart_D) / 3
    return fitness


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print(SOLUTIONS[0])
    nb_tra = nombre_heures_travaillée(MISSIONS, INTERVENANTS, SOLUTIONS[0])
    nb_non_tra, nb_sup = nombre_heures_non_travaillée_et_sup(nb_tra, INTERVENANTS)
    print(nb_tra)
    print(nb_non_tra, nb_sup)
    #print(activites_intervenants(SOLUTIONS[0]))
    #print(distance_employé(MATRICE_DISTANCE, activites_intervenants(SOLUTIONS[0])))
    #print(ordre_mission(SOLUTIONS, MISSIONS, INTERVENANTS))
    ecart_dis = st.pstdev(distance_employé(MATRICE_DISTANCE, activites_intervenants(SOLUTIONS[0], INTERVENANTS, MISSIONS)))
    ecart_WH = st.pstdev(nb_non_tra)
    ecart_OH = st.pstdev(nb_sup)
    #for k in range(len(ecart_WH)):
    print(fitnessEm(ecart_WH, ecart_OH, ecart_dis, INTERVENANTS, MATRICE_DISTANCE))


if __name__ == "__main__":
    main()
