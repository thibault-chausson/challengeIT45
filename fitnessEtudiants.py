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


def alpha(sol):
    """
    Retourne le coefficient alpha de la fonction de cout
    """
    nbMiss = len(sol[0])
    alpha = 100 / nbMiss
    return alpha


def penalite_1(solution, mis, inter):
    """
    Retourne la penalite de la solution
    """
    nbMiss = len(mis)
    nbInter = len(inter)
    penalite = 0
    for i in range(nbInter):
        for j in range(nbMiss):
            if solution[i][j] == 1:
                if mis[j][5] != inter[i][2]:
                    penalite += 1
    return penalite

def toute_pena (solutions, mis, inter):
    nbSol = len(solutions)
    pena=np.zeros(nbSol)
    for i in range(nbSol):
        pena[i] = penalite_1(solutions[i], mis, inter)
    return pena


def fitnessEtudiants_1(solution, mis, inter):
    """
    Retourne le fitness de chaque solution
    """
    al = alpha(solution)
    pe = penalite_1(solution, mis, inter)
    fitness = al * pe
    return fitness

def fitnessEtudiants_tableau(solution, mis, inter):
    fitness = np.zeros(len(solution))
    for i in range(len(solution)):
        fitness[i] = fitnessEtudiants_1(solution[i], mis, inter)
    return fitness



def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    #print(SOLUTIONS[0])
    print(fitnessEtudiants_tableau(SOLUTIONS, MISSIONS, INTERVENANTS))


if __name__ == "__main__":
    main()
