import json as js
import statistics as st
import numpy as np
import random as rd

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


exempleFitness = [[12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989]
                  ]

exempleFitness2 = [[112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989],
                   [112, 198, 156, 119, 1152, 164, 1567, 174, 1989]
                   ]

def choixParents(fitness): #fonction qui choisit les parents à partir de leur fitness (decroissante) et renvoie les indices des parents
    nbSol = len(fitness)
    ponde = np.zeros(nbSol)
    aux = np.zeros(nbSol)
    for i in range(nbSol):
        aux[i] = 1 / fitness[i]
    for i in range(nbSol):
        ponde[i] = (aux[i] / np.sum(aux))
    Parent1 = rd.choices(range(nbSol), weights=ponde, k=1)
    ponde[Parent1[0]] = 0
    Parent2 = rd.choices(range(nbSol), weights=ponde, k=1)
    return (Parent1[0], Parent2[0])




def reproduction (solution1, solution2, ligDebut, ligFin, colDebut, colFin): #fonction qui realise la reproduction entre deux solutions
    """
    Retourne la solution fille
    Attention : la ligne de fin et col de fin a eu un +1 pour palier au range qui fait -1
    """
    nblig = len(solution1)
    nbcol = len(solution1[0])
    fille = solution1.copy()
    for i in range(ligDebut, ligFin+1):
        for j in range(colDebut, colFin+1):
            fille[i][j] = solution2[i][j]
    return fille

def tri_langage(Mission):
    LPC = []
    LSF= []
    for i in range(len(Mission)):
        if Mission[i][4] == "LPC":
            LPC.append(Mission[i])
        else:
            LSF.append(Mission[i])
    return LPC, LSF



def main():
    charge_fichier_csv("45-4")
    print(tri_langage(MISSIONS))


if __name__ == "__main__":
    main()