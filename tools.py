import json as js
import statistics as st
import numpy as np
import random as rd
import copy as cop

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







exempleFitness = [[12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989],
                  [12, 98, 56, 9, 152, 64, 567, 74, 989]
                  ]

exemple=[[1,2,3,4],
         [5,6,7,8],
         [9,10,11,12],
        [13,14,15,16]]

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
    fille = cop.deepcopy(solution1)
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


def mutation(solution):
    """
    Retourne la solution mutée
    """
    nblig = len(solution)
    nbcol = len(solution[0])
    rdLine1 = rd.randint(0, nblig-1)
    rdCol = rd.randint(0, nbcol-1)
    rdLine2 = rd.randint(0, nblig-1)
    (solution[rdLine1][rdCol], solution[rdLine2][rdCol]) = (solution[rdLine2][rdCol], solution[rdLine1][rdCol])
    return solution




def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print(SOLUTIONS)


if __name__ == "__main__":
    main()