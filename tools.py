import numpy as np
import random as rd
import copy as cop
import functions as fc
import genetique as g
import population_initiale as pop
import paretoFront as pf


def choixParents(fitness):
    # fonction qui choisit les parents à partir de leur fitness (decroissante) et renvoie les indices des parents
    """
    Choix par roulette des parents
    """
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


def choixKill(fitness):
    """
    Choix par roulette des parents
    """
    nbSol = len(fitness)
    ponde = np.zeros(nbSol)
    somme = 0
    for i in range(nbSol):
        somme += fitness[i]
    for i in range(nbSol):
        ponde[i] = (fitness[i] / somme)
    kill1 = rd.choices(range(nbSol), weights=ponde, k=1)
    return (kill1[0])


def reproduction(solution1, solution2, ligDebut, ligFin, colDebut,
                 colFin):  # fonction qui realise la reproduction entre deux solutions
    """
    Retourne la solution fille
    Attention : la ligne de fin et col de fin a eu un +1 pour palier au range qui fait -1
    """
    nblig = len(solution1)
    nbcol = len(solution1[0])
    fille = cop.deepcopy(solution1)
    for i in range(ligDebut, ligFin + 1):
        for j in range(colDebut, colFin + 1):
            fille[i][j] = solution2[i][j]
    return fille


def tri_langage(Mission):
    """
    Tri les missions par le langage des étudiants
    """
    LPC = []
    LSF = []
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
    rdLine1 = rd.randint(0, nblig - 1)
    rdCol = rd.randint(0, nbcol - 1)
    rdLine2 = rd.randint(0, nblig - 1)
    (solution[rdLine1][rdCol], solution[rdLine2][rdCol]) = (solution[rdLine2][rdCol], solution[rdLine1][rdCol])
    return solution


def moyenneFitness_Norma(fitness1, fitness2, fitness3):
    """
    Retourne la moyenne des tableaux des Fitness
    """
    nbSol = len(fitness1)
    moyenne = np.zeros(nbSol)
    fitness1_norma = normalisationTableaux(fitness1)
    fitness2_norma = normalisationTableaux(fitness2)
    fitness3_norma = normalisationTableaux(fitness3)
    for i in range(nbSol):
        moyenne[i] = (fitness1_norma[i] + fitness2_norma[i] + fitness3_norma[i]) / 3
    return moyenne


def moyenneFitness(fitness1, fitness2, fitness3):
    """
    Retourne la moyenne des tableaux des Fitness
    """
    nbSol = len(fitness1)
    moyenne = np.zeros(nbSol)
    for i in range(nbSol):
        moyenne[i] = (fitness1[i] + fitness2[i] + fitness3[i]) / 3
    return moyenne


def moyenneFit_1(mission, intervenants, solution_1, distances):
    empl = g.choixFitness_1("employe", mission, intervenants, solution_1, distances)
    etu = g.choixFitness_1("etudiant", mission, intervenants, solution_1, distances)
    sess = g.choixFitness_1("SESSAD", mission, intervenants, solution_1, distances)
    return (empl + etu + sess) / 3


def normalisationTableaux(fitness):
    """
    Retourne le tableau normalisé
    """
    nbSol = len(fitness)
    normalise = np.zeros(nbSol)
    maximum = max(fitness)
    minimum = min(fitness)
    for i in range(nbSol):
        if maximum == minimum:
            normalise[i] = 1
        else:
            normalise[i] = (fitness[i] - minimum) / (maximum - minimum) + 1
    return normalise


def remplacement(fitness_tab, sol, intervenants, missions, matrice_distance):
    solution = cop.deepcopy(sol)
    mediane = np.median(fitness_tab)
    nbSol = len(fitness_tab)
    nbIndividu = nbSol // 2 + 1
    j = 0
    population_remplacement = pop.gen_n_solutions_uniques(nbIndividu, intervenants, missions, matrice_distance)
    for i in range(nbSol):
        if fitness_tab[i] > mediane:
            solution[i] = population_remplacement[j]
            j += 1
    return solution


def affichageClassique(solution, type, Mission, Intervenants, Distances, type_algo):
    """
    Affiche la solution et le fitness
    """
    if type_algo == "cascade":
        fit_SE = g.choixFitness_tableau("SESSAD", Mission, Intervenants, solution, Distances)
        fit_EM = g.choixFitness_tableau("employe", Mission, Intervenants, solution, Distances)
        fit_ET = g.choixFitness_tableau("etudiant", Mission, Intervenants, solution, Distances)

        indiceSE, bestFitSE = g.mini(fit_SE)
        planningSE = fc.activites_intervenants(solution[indiceSE], Intervenants, Mission)
        print("La fitness de SESSAD est : ", bestFitSE)
        print("La solution de SESSAD est : ", solution[indiceSE])
        print("Le planning de SESSADest :", planningSE)
        print("\n")

        indiceEM, bestFitEM = g.mini(fit_EM)
        planning = fc.activites_intervenants(solution[indiceEM], Intervenants, Mission)
        print("La fitness de employés est : ", bestFitEM)
        print("La solution de employés est : ", solution[indiceEM])
        print("Le planning de employés est:", planning)
        print("\n")

        indiceET, bestFitET = g.mini(fit_ET)

        planning = fc.activites_intervenants(solution[indiceET], Intervenants, Mission)
        print("La fitness de étudiants est : ", bestFitET)
        print("La solution de étudiants est : ", solution[indiceET])
        print("Le planning de étudiants est :", planning)
        print("\n")

    else:
        if type_algo == "classique":
            fit = g.choixFitness_tableau(type, Mission, Intervenants, solution, Distances)
        if type_algo == "moyenne":
            fit = moyenneFitness(g.choixFitness_tableau("employe", Mission, Intervenants, solution, Distances),
                                 g.choixFitness_tableau("SESSAD", Mission, Intervenants, solution, Distances),
                                 g.choixFitness_tableau("etudiant", Mission, Intervenants, solution, Distances))
        if type_algo == "normal":
            fit = moyenneFitness_Norma(g.choixFitness_tableau("employe", Mission, Intervenants, solution, Distances),
                                       g.choixFitness_tableau("SESSAD", Mission, Intervenants, solution, Distances),
                                       g.choixFitness_tableau("etudiant", Mission, Intervenants, solution, Distances))

        indice, bestFit = g.mini(fit)
        planning = fc.activites_intervenants(solution[indice], Intervenants, Mission)
        print("La fitness de est : ", bestFit)
        print("La solution de est : ", solution[indice])
        print("Le planning est :", planning)
        print("\n")


def affichagePareto(solution, Mission, Intervenants, Distances):
    fit_SE = g.choixFitness_tableau("SESSAD", Mission, Intervenants, solution, Distances)
    fit_EM = g.choixFitness_tableau("employe", Mission, Intervenants, solution, Distances)
    fit_ET = g.choixFitness_tableau("etudiant", Mission, Intervenants, solution, Distances)
    pare = pf.pareto_frontier_multi(fit_ET, fit_EM, fit_SE)
    sol = pare[3]
    print(solution[sol[1]])
    for i in range(len(sol)):
        fit_SE = g.choixFitness_1("SESSAD", Mission, Intervenants, solution[sol[i]], Distances)
        fit_EM = g.choixFitness_1("employe", Mission, Intervenants, solution[sol[i]], Distances)
        fit_ET = g.choixFitness_1("etudiant", Mission, Intervenants, solution[sol[i]], Distances)
        planning = fc.activites_intervenants(solution[sol[i]], Intervenants, Mission)
        print("La fitness de SESSAD est : ", fit_SE)
        print("La fitness de étudiants est : ", fit_ET)
        print("La fitness de employés est : ", fit_EM)
        print("La solution est : ", solution[sol[i]])
        print("Le planning est :", planning)
        print("\n")


def affichageCascadeFit(solutions, Mission, Intervenants, Distances):
    fit_SE = g.choixFitness_tableau("SESSAD", Mission, Intervenants, solutions, Distances)
    fit_EM = g.choixFitness_tableau("employe", Mission, Intervenants, solutions, Distances)
    fit_ET = g.choixFitness_tableau("etudiant", Mission, Intervenants, solutions, Distances)

    sols = []

    fit_SE_trie = sorted(fit_SE)
    fit_EM_trie = sorted(fit_EM)
    fit_ET_trie = sorted(fit_ET)


    for i in range(len(solutions)):
        index = fit_SE_trie.index(fit_SE[i]) + fit_EM_trie.index(fit_EM[i]) + fit_ET_trie.index(fit_ET[i])
        sols.append((index, solutions[i], (fit_SE[i], fit_EM[i], fit_ET[i])))

    sols_sorted = sorted(sols, key=lambda x: x[0])

    print("Fitness meilleure solution: ")
    print("\tSESSAD:", sols_sorted[0][2][0])
    print("\temployé:", sols_sorted[0][2][1])
    print("\tétudiant:", sols_sorted[0][2][2])

    print("Meilleure solution: ")
    for i in sols_sorted[0][1]:
        print(i)

 
