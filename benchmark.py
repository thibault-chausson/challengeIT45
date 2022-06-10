import genetique as gene
import fitnessSESSAD as fS
import time as ti

import json as js
import numpy as np
import fitnessEmployes as fE

import matplotlib.pyplot as plt

import population_initiale as pI

import functions as f

import population_initiale as pop

import copy as copy





def duree(deb, nbPopMax, pas, matrice_distance, intervenants, missions, type, sol):
    """
    Fonction qui permet de calculer le temps d'exécution de X générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit le temps d'exécution de la génération de X générations en secondes dans un tableau
    """
    print(len(sol[0]))
    temps = [0]
    x = [0]

    for i in range(deb, nbPopMax, pas):
        sol2 = copy.deepcopy(sol)
        debut = ti.time()
        gene.genetiquePareto(sol2, i, 0.1, matrice_distance, intervenants, missions, 0.0)
        fin = ti.time()
        x.append(i)
        temps.append(fin - debut)

    plt.plot(x, temps)
    plt.xlabel("Générations")
    plt.ylabel("Temps en secondes")
    plt.title("Evolution du temps de calcul en fonction du nombre de générations")
    plt.savefig('test' + '.pdf')
    plt.show()

    return x, temps


def evolutionFit(deb, nbPopMax, pas, type, matrice_distance, intervenants, missions):
    """
    Fonction qui permet de calculer l'évolution de la fitness des générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit la fitness de la génération de X générations dans un tableau
    """
    sol = f.charger_solution("solutions.txt")
    print(len(sol[0]))
    fit = [min(gene.choixFitness_tableau(type, missions, intervenants, sol, matrice_distance))]
    x = [0]
    indice = 0
    for i in range(deb, nbPopMax + pas, pas):
        sol2 = copy.deepcopy(sol)
        gene.genetique(sol2, i, 0.07, matrice_distance, intervenants, missions, 0.00, type, True)
        finFit = min(gene.choixFitness_tableau(type, missions, intervenants, sol, matrice_distance))
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


def tempsGenePopu (geneMin, geneMax, pas, intervenants, missions, distance):
    x=[]
    temps=[]
    for i in range(geneMin, geneMax, pas):
        start_time = ti.time()
        pI.gen_n_solutions_uniques(i, intervenants, missions, distance)
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

    distance, intervenants, missions = f.charge_fichier_csv("45-4")
    solutions = pop.gen_n_solutions_uniques(100, intervenants, missions, distance)
    #tempsGenePopu(5, 150, 10)
    deb, nbPopMax, pas = 100, 4000, 200
    print(nbSolutionnn(deb, nbPopMax, pas))
    x, y = duree(deb, nbPopMax, pas, distance, intervenants, missions, "employe", solutions)


if __name__ == "__main__":
    main()
