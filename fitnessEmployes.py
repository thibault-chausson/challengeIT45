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


def nombre_heures_travaillée(MISSIONS, INTERVENANTS, SOLUTIONS):
    nbInter = len(INTERVENANTS)
    nbSol = len(SOLUTIONS)
    nbMiss = len(MISSIONS)
    nbHeuresTravaille = np.zeros((nbSol, nbInter))
    for i in range(nbSol):
        for j in range(nbInter):
            for k in range(nbMiss):
                if (SOLUTIONS[i][j][k] == 1):
                    nbHeuresTravaille[i][j] += (MISSIONS[k][3] - MISSIONS[k][2]) / 60
    return nbHeuresTravaille


def nombre_heures_non_travaillée_et_sup(nbHeuresTravaille, INTERVENANTS):
    nbInter = len(nbHeuresTravaille[0])
    nbSol = len(nbHeuresTravaille)
    nbHeuresNonTravaillee = np.zeros((nbSol, nbInter))
    nbHeuresSup = np.zeros((nbSol, nbInter))
    for i in range(nbSol):
        for j in range(nbInter):
            heure = INTERVENANTS[j][3] - nbHeuresTravaille[i][j]
            if (heure > 0):
                nbHeuresNonTravaillee[i][j] = heure
            else:
                nbHeuresSup[i][j] = abs(heure)
    return nbHeuresNonTravaillee, nbHeuresSup


def ecart_type(tableau):
    nbSol = len(tableau)
    sol = np.zeros(nbSol)
    for i in range(nbSol):
        sol[i] = st.pstdev(tableau[i])
    return sol



def activites_intervenants(solution):
    """
    Renvoie les id des missions effectues par chaque intervenant, rangés dans l'ordre horaire
    """
    miss_intervenants = []
    for i in range(len(INTERVENANTS)):
        missions = {1: [], 2: [], 3: [], 4: [], 5: []}
        edt = {1: [], 2: [], 3: [], 4: [], 5: []}
        for j in range(len(MISSIONS)):
            if solution[i][j] == 1:
                missions[MISSIONS[j][1]].append((j, MISSIONS[j][2]))
        for jour in missions:
            temp = sorted(missions[jour], key=lambda x: x[1])
            edt[jour] = [i[0] for i in temp]

        miss_intervenants.append(edt)

    return miss_intervenants



def distance_employé (DISTANCES, planning_1_mission): #Non testée
    nbInter = len(planning_1_mission)
    nbJour=len(planning_1_mission[0])
    distance = np.zeros(nbInter) #distance par semaine pour un intervenant
    for i in range(nbInter):
        for j in range(1,nbJour+1):
            nbMissionsJournal = len(planning_1_mission[i][j])
            for k in range(nbMissionsJournal+1):
                if k ==0 :
                    distance[i] += DISTANCES[0][planning_1_mission[i][j][k]]
                elif k==nbMissionsJournal:
                    distance[i] += DISTANCES[planning_1_mission[i][j][k-1]][0]
                else:
                    distance[i] += DISTANCES[planning_1_mission[i][j][k-1]][planning_1_mission[i][j][k]]
    return distance


def moyenne_toutes_distances(DISTANCES,INTERVENANTS): #DISTANCES est une matrice carrée
    nbInter = len(INTERVENANTS)
    nbMission = len(DISTANCES)
    somme=0
    for i in range(nbMission):
        somme += DISTANCES[i][0]+DISTANCES[0][i]
    return somme/nbInter


def kapa(DISTANCES,INTERVENANTS):
    moy = moyenne_toutes_distances(DISTANCES, INTERVENANTS)
    kapa = 100 / moy
    return kapa



def fitnessEm(ecart_WH, ecart_OH, ecart_D, INTERVENANTS, DISTANCES): #Non testée
    zeta = 10
    nbInter = len(INTERVENANTS)
    sumHeureTrav = 0
    for i in range(nbInter):
        sumHeureTrav += INTERVENANTS[i][3]
    gamma = 100 / sumHeureTrav
    kap = kapa(DISTANCES, INTERVENANTS)
    fitness = (zeta * ecart_WH + gamma * ecart_OH + kap * ecart_D) / 3
    return fitness


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    nb_tra = nombre_heures_travaillée(MISSIONS, INTERVENANTS, SOLUTIONS)
    nb_non_tra, nb_sup = nombre_heures_non_travaillée_et_sup(nb_tra, INTERVENANTS)
    #print(activites_intervenants(SOLUTIONS[0]))
    print(distance_employé(MATRICE_DISTANCE, activites_intervenants(SOLUTIONS[0])))
    #print(ordre_mission(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
