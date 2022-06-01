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

def moyDist(disEmploy):
    moy=0
    for i in range(len(disEmploy)):
        moy+=disEmploy[i]
    return moy/len(disEmploy)

def maxDist(disEmploy):
    maxi=0
    for i in range(len(disEmploy)):
        if disEmploy[i]>maxi:
            maxi=disEmploy[i]
    return maxi

def fitnessSESSAD(MISSIONS, INTERVENANTS, SOLUTIONS,DISTANCE, dist_1_Semaine):
    summe = sumWOH(MISSIONS, INTERVENANTS, SOLUTIONS)
    kap=fE.kapa(DISTANCE,INTERVENANTS)
    bet=beta()
    moyDis= moyDist(dist_1_Semaine)
    maxDis= maxDist(dist_1_Semaine)
    f=(bet*summe+kap*moyDis+kap*maxDis)/3
    return f


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


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    #print(activites_intervenants(SOLUTIONS[0]))
    dis1=fE.distance_employé(MATRICE_DISTANCE, activites_intervenants(SOLUTIONS[0]))
    print(fitnessSESSAD(MISSIONS, INTERVENANTS, SOLUTIONS,MATRICE_DISTANCE,dis1))


if __name__ == "__main__":
    main()