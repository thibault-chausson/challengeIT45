import genetique as gene
import fitnessSESSAD as fS
import time as ti

import json as js
import numpy as np
import fitnessEmployes as fE

import matplotlib.pyplot as plt

from functions import *


def duree(deb, nbPopMax, pas):
    """
    Fonction qui permet de calculer le temps d'exécution de X générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit le temps d'exécution de la génération de X générations en secondes dans un tableau
    """
    sol = read_sols("TRUE_res.txt")
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
    plt.show()

    return x, temps


def evolutionFit(deb, nbPopMax, pas, type):
    """
    Fonction qui permet de calculer l'évolution de la fitness des générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit la fitness de la génération de X générations dans un tableau
    """
    sol = read_sols("TRUE_res.txt")
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


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = read_sols("TRUE_res.txt")
    deb, nbPopMax, pas = 10, 230, 2
    print(nbSolutionnn(deb, nbPopMax, pas))
    x, y = duree(deb, nbPopMax, pas)


if __name__ == "__main__":
    main()
