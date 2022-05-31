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


def ordre_mission(SOLUTIONS, MISSIONS, INTERVENANTS):   #Il y a un problème
    nbSol=len(SOLUTIONS)
    nbMission=len(MISSIONS)
    nbInter=len(INTERVENANTS)
    nbJour=5
    ordre=[]
    for i in range(nbSol):
        auxUser = []
        for j in range(nbInter):

            aux2 = []
            auxL=[]
            auxM = []
            auxMe = []
            auxJ = []
            auxV = []
            for k in range(nbMission):
                if (SOLUTIONS[i][j][k]==1):
                    if (MISSIONS[k][1]==1):
                        auxL.append((MISSIONS[k][0], MISSIONS[k][2]))
                    if (MISSIONS[k][1] == 2):
                        auxM.append((MISSIONS[k][0], MISSIONS[k][2]))
                    if (MISSIONS[k][1]==3):
                        auxMe.append((MISSIONS[k][0], MISSIONS[k][2]))
                    if (MISSIONS[k][1]==4):
                        auxJ.append((MISSIONS[k][0], MISSIONS[k][2]))
                    if (MISSIONS[k][1]==5):
                        auxV.append((MISSIONS[k][0], MISSIONS[k][2]))
            aux2.append(auxL)
            aux2.append(auxM)
            aux2.append(auxMe)
            aux2.append(auxJ)
            aux2.append(auxV)
        ordre.append(aux2)
    print(ordre)
    for i in range(nbSol):
        for j in range(nbInter):
            for k in range(nbJour):
                ordre[i][j][k].sort(key=lambda x: x[1])
    return ordre




def distance_employé (SOLUTIONS, DISTANCES, ORDRE): #Non testée
    nbSol = len(SOLUTIONS)
    nbMiss = len(SOLUTIONS[0])
    nbInter = len(SOLUTIONS[0][0])
    nbJour=5
    distance = np.zeros((nbSol, nbInter))
    for i in range(nbSol):
        for j in range (nbInter):
            for k in range(nbJour):
                nbOrdre = len(ORDRE[i][j][k])
                for l in range(nbOrdre):
                    if (l == 0):
                        distance[i][j] += DISTANCES[0][ORDRE[i][j][k][l]]
                    elif (l==nbOrdre-1):
                        distance[i][j] += DISTANCES[ORDRE[i][j][k][l]][0]
                    else:
                        distance[i][j] += DISTANCES[ORDRE[i][j][k][l]][ORDRE[i][j][k][l+1]]
    return distance


def moyenne_toutes_distances(DISTANCES,INTERVENANTS): #DISTANCES est une matrice carrée
    nbInter = len(INTERVENANTS)
    nbMission = len(DISTANCES)
    somme=0
    for i in range(nbMission):
        somme += DISTANCES[i][0]+DISTANCES[0][i]
    return somme/nbInter



def fitnessEm(ecart_WH, ecart_OH, ecart_D, INTERVENANTS, DISTANCES): #Non testée
    zeta = 10
    nbInter = len(INTERVENANTS)
    sumHeureTrav = 0
    for i in range(nbInter):
        sumHeureTrav += INTERVENANTS[i][3]
    gamma = 100 / sumHeureTrav
    moy = moyenne_toutes_distances(DISTANCES,INTERVENANTS)
    kapa = 100 / moy
    fitness = (zeta * ecart_WH + gamma * ecart_OH + kapa * ecart_D) / 3
    return fitness


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    nb_tra = nombre_heures_travaillée(MISSIONS, INTERVENANTS, SOLUTIONS)
    nb_non_tra, nb_sup = nombre_heures_non_travaillée_et_sup(nb_tra, INTERVENANTS)
    print(ordre_mission(SOLUTIONS,MISSIONS,INTERVENANTS))
    #print(ordre_mission(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
