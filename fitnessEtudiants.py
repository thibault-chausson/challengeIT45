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


def alpha(mission):
    """
    Retourne le coefficient alpha de la fonction de cout
    """
    nbMiss = len(mission)
    alpha = 100 / nbMiss
    return alpha


def penalite_1(solution, MISSION, INTERVENANT):
    """
    Retourne la penalite de la solution
    """
    nbMiss = len(MISSION)
    nbInter = len(INTERVENANT)
    penalite = 0
    for i in range(nbInter):
        for j in range(nbMiss):
            if solution[i][j] == 1:
                if MISSION[j][5] != INTERVENANT[i][2]:
                    penalite += 1
    return penalite

def penalite_toutes_solution(SOLUTIONS, MISSION,INTERVENANT):
    """
    Retourne la penalite de chaque solution, en utilisant la fonction penalite_1 qui calcule la pénalité d'une solution
    """
    nbSol= len(SOLUTIONS)
    pen=np.zeros(nbSol)
    for i in range (nbSol):
        pen[i]=penalite_1(SOLUTIONS[i],MISSION,INTERVENANT)
    return pen


def fitnessEtudiants_1(solution, MISSIONS, INTERVENANTS):
    """
    Retourne le fitness d'un solution
    """
    al = alpha(MISSIONS)
    pe = penalite_1(solution, MISSIONS, INTERVENANTS)
    fitness = al * pe
    return fitness

def fitnessEtudiants_tout(SOLUTIONS, MISSIONS,INTERVENANTS):
    """
    Retourne le fitness de chaque solution pour les étudiants
    """
    nbSol=len(SOLUTIONS)
    fit=np.zeros(nbSol)
    for i in range(nbSol):
        fit[i]=fitnessEtudiants_1(SOLUTIONS[i],MISSIONS,INTERVENANTS)
    return fit


def main():
    charge_fichier_csv("100-10")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    #print(SOLUTIONS[0])
    print(fitnessEtudiants_tout(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
