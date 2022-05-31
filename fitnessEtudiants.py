import json as js
import numpy as np

MATRICE_DISTANCE = []
INTERVENANTS = []
MISSIONS = []

SOLUTIONS = []


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


def alpha(SOLUTIONS):
    """
    Retourne le coefficient alpha de la fonction de coût
    """
    nbMiss = len(SOLUTIONS[0][0])
    alpha = 100 / nbMiss
    return alpha


def penalite(SOLUTIONS, MISSION, INTERVENANT):
    """
    Retourne la penalité de la solution
    """
    nbMiss = len(MISSION)
    nbInter = len(INTERVENANT)
    nbSol = len(SOLUTIONS)
    penalite = np.zeros(nbSol)
    for k in range(nbSol):
        for i in range(nbInter):
            for j in range(nbMiss):
                if SOLUTIONS[k][i][j] == 1:
                    if MISSION[j][5] != INTERVENANT[i][2]:
                        penalite[k] += 1
    return penalite


def fitnessEtudiants(SOLUTIONS, MISSIONS, INTERVENANTS):
    """
    Retourne le fitness de chaque solution
    """
    al = alpha(SOLUTIONS)
    pe = penalite(SOLUTIONS, MISSIONS, INTERVENANTS)
    nbSol = len(SOLUTIONS)
    fitness = np.zeros(nbSol)
    for i in range(nbSol):
        fitness[i] = al * pe[i]
    return fitness


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print(fitnessEtudiants(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
