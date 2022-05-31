import json as js
import numpy as np
import fitnessEmployes as fE

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


def sumWOH(MISSIONS, INTERVENANTS, SOLUTIONS):
    nbSol=len(SOLUTIONS)
    somme=np.zeros(nbSol)
    nbHeuresTrav = fE.nombre_heures_travaillée(MISSIONS, INTERVENANTS, SOLUTIONS)
    nbNonTrav=(fE.nombre_heures_non_travaillée_et_sup(nbHeuresTrav, INTERVENANTS))[0]
    for i in range(nbSol):
        for j in range(len(INTERVENANTS)):
            somme[i]+=nbNonTrav[i][j]+nbHeuresTrav[i][j]
    return (somme)


def beta():
    return 100/45

def fitnessSESSAD(MISSIONS, INTERVENANTS, SOLUTIONS,DISTANCE):
    summe = sumWOH(MISSIONS, INTERVENANTS, SOLUTIONS)
    kap=fE.kapa(DISTANCE,INTERVENANTS)
    bet=beta()
    moyDis= ###Pas encore de fonction
    maxDis= ###Pas encore de fonction
    f=(bet*summe+kap*moyDis+kap*maxDis)/3
    return f



def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print(sumWOH(MISSIONS, INTERVENANTS, SOLUTIONS))


if __name__ == "__main__":
    main()