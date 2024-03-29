import genetique as gene
import fitnessSESSAD as fS
import time as ti

import json as js
import numpy as np
import fitnessEmployes as fE

import matplotlib.pyplot as plt

import population_initiale as pI

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


def duree(deb, nbPopMax, pas):
    """
    Fonction qui permet de calculer le temps d'exécution de X générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit le temps d'exécution de la génération de X générations en secondes dans un tableau
    """
    sol = charger_solution("solutions.txt")
    print(len(sol[0]))
    temps = [0]
    x = [0]
    indice = 0
    debut = ti.time()
    for i in range(deb, nbPopMax + pas, pas):
        sol = gene.genetique(sol, i, 0.07, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, 0.00, "employe")
        fin = ti.time()
        x.append(x[indice] + i)
        indice += 1
        temps.append(fin - debut)

    plt.plot(x, temps)
    plt.xlabel("Générations")
    plt.ylabel("Temps en secondes")
    plt.title("Evolution du temps de calcul en fonction du nombre de générations")
    plt.savefig('test' + '.pdf')
    plt.show()

    return x, temps


def evolutionFit(deb, nbPopMax, pas, type):
    """
    Fonction qui permet de calculer l'évolution de la fitness des générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit la fitness de la génération de X générations dans un tableau
    """
    sol = charger_solution("solutions.txt")
    print(len(sol[0]))
    fit = [min(gene.choixFitness_tableau(type, MISSIONS, INTERVENANTS, sol, MATRICE_DISTANCE))]
    x = [0]
    indice = 0
    for i in range(deb, nbPopMax + pas, pas):
        sol = gene.genetique(sol, i, 0.07, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, 0.00, type)
        finFit = min(gene.choixFitness_tableau(type, MISSIONS, INTERVENANTS, sol, MATRICE_DISTANCE))
        fit.append(finFit)
        x.append(x[indice] + i)
        indice += 1

    plt.plot(x, fit)
    plt.xlabel("Générations")
    plt.ylabel("Fitness")
    plt.title("Évolution de la fitness " + type + " en fonction du nombre de générations")
    plt.savefig('test' + '.pdf')
    plt.show()

    return x, fit


def nbSolutionnn(deb, nbPopMax, pas):
    """
    Fonction qui permet de calculer le nombre de génération en donnant le nombre minimal de génération, le pas entre chaque génération
    """
    x = [0]
    indice = 0
    for i in range(deb, nbPopMax + pas, pas):
        x.append(x[indice] + i)
        indice += 1

    return x[-1]


def tempsGenePopu (geneMin, geneMax, pas):
    x=[]
    temps=[]
    for i in range(geneMin, geneMax, pas):
        start_time = ti.time()
        pI.gen_n_solutions_uniques(i)
        end_time = ti.time()
        x.append(i)
        temps.append(end_time-start_time)

    plt.plot(x, temps)
    plt.xlabel("Taille de la population")
    plt.ylabel("Temps en secondes")
    plt.title("Évolution du temps pour générer une population initiale")
    plt.savefig('test' + '.pdf')
    plt.show()
    return x, temps






def main():
    charge_fichier_csv("45-4")
    #tempsGenePopu(5, 150, 10)
    SOLUTIONS = charger_solution("solutions.txt")
    deb, nbPopMax, pas = 10, 230, 2
    print(nbSolutionnn(deb, nbPopMax, pas))
    x, y = duree(deb, nbPopMax, pas)


if __name__ == "__main__":
    main()
