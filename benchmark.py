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

import tools as tls





def duree(deb, nbPopMax, pas, matrice_distance, intervenants, missions, type, sol):
    """
    Fonction qui permet de calculer le temps d'exécution de X générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit le temps d'exécution de la génération de X générations en secondes dans un tableau
    """
    print(len(sol[0]))
    temps = [0]
    x = [0]
    indice = 0
    for i in range(deb, nbPopMax, pas):
        sol2 = copy.deepcopy(sol)
        debut = ti.time()
        sol = gene.genetique(sol2, i, 0.1, matrice_distance, intervenants, missions, 0.0, "employe", True)
        fin = ti.time()
        x.append(x[indice] + i)
        temps.append(temps[indice] + fin - debut)
        indice += 1

    plt.scatter(x, temps)
    plt.xlabel("Générations")
    plt.ylabel("Temps en secondes")
    plt.title("Evolution du temps de calcul en fonction du nombre de générations")
    plt.savefig('test' + '.pdf')
    plt.show()

    return x, temps


def evolutionFit(deb, nbPopMax, pas, type, matrice_distance, intervenants, missions, sol):
    """
    Fonction qui permet de calculer l'évolution de la fitness des générations
    A chaque tour dans la boucle for on reprend la solution précédente et ainsi on évite de repartir du début
    On renvoit la fitness de la génération de X générations dans un tableau
    """
    print(len(sol[0]))
    fit_Et = [min( gene.choixFitness_tableau("etudiant", missions, intervenants, sol, matrice_distance))]
    fit_Em = [min(gene.choixFitness_tableau("employe", missions, intervenants, sol, matrice_distance))]
    fit_Se = [min(gene.choixFitness_tableau("SESSAD", missions, intervenants, sol, matrice_distance))]
    x = [0]
    indice = 0
    sol2 = copy.deepcopy(sol)
    for i in range(deb, nbPopMax + pas, pas):
        sol3 = copy.deepcopy(gene.genetique(sol2, i, 0.07, matrice_distance, intervenants, missions, 0.00, "SESSAD", True))
        sol2 = copy.deepcopy(sol3)
        fit_1 = min(gene.choixFitness_tableau("etudiant", missions, intervenants, sol2, matrice_distance))
        fit_2 = min(gene.choixFitness_tableau("employe", missions, intervenants, sol2, matrice_distance))
        fit_3 = min(gene.choixFitness_tableau("SESSAD", missions, intervenants, sol2, matrice_distance))
        fit_Et.append(fit_1)
        fit_Em.append(fit_2)
        fit_Se.append(fit_3)
        x.append(x[indice] + i)
        indice += 1

    fig = plt.figure()

    subplot1 = fig.add_subplot(2, 1, 2)
    subplot1.scatter(x, fit_Et)

    subplot1.set_ylabel('Fitness étudiants')
    subplot1.set_title('Étudiants')
    subplot1.set_xlabel('Générations')


    subplot2 = fig.add_subplot(2, 2, 1)
    subplot2.scatter(x, fit_Em,  color="green")
    subplot2.set_ylabel('Fitness employés')
    subplot2.set_xlabel('Générations')
    subplot2.set_title('Employés')

    subplot3 = fig.add_subplot(2,2,2)
    subplot3.scatter(x, fit_Se,  color="red")
    subplot3.set_ylabel('Fitness SESSAD')
    subplot3.set_xlabel('Générations')
    subplot3.set_title('SESSAD')


    fig.suptitle("Évolution de la fitness SESSAD pour l'agorithme en fonction du nombre de générations")






    plt.savefig('test' + '.pdf')

    plt.show()

    return


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

    plt.scatter(x, temps)
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
    deb, nbPopMax, pas = 10, 600, 20
    print(nbSolutionnn(deb, nbPopMax, pas))
    #duree(deb, nbPopMax, pas, distance, intervenants, missions, "", solutions)
    #tempsGenePopu(deb, nbPopMax, pas, intervenants, missions, distance)
    evolutionFit(deb, nbPopMax, pas, type, distance, intervenants, missions, solutions)



if __name__ == "__main__":
    main()
