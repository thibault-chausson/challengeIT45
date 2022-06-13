import statistics as st
import numpy as np
import random as rd

import fitnessEmployes as fEm
import fitnessEtudiants as fEt
import fitnessSESSAD as fS

import tools as tls
import functions as fct

import copy as cp

import paretoFront as pf
import population_initiale as pop

import time as ti


def fitnessEmInitialisation(mission, inter, solution_1, distances):
    """
    Fonction qui initialise la fitness employé pour une solution
    """
    nbTrav, nbNon, nbSup = fEm.stats_heures(solution_1, inter, mission)
    solution_1_planning = fct.activites_intervenants(solution_1, inter, mission)
    nbDis = fEm.distance_employe(solution_1_planning, distances)
    fitnessEmplo_1_sol = fEm.fitnessEm(st.pstdev(nbNon), st.pstdev(nbSup), st.pstdev(nbDis), inter, distances)
    return fitnessEmplo_1_sol


def tableau_fitnessEM(mission, inter, solution, distances):
    """
    Fonction qui calcule la fitness employé pour toutes les solutions
    """
    nbSol = len(solution)
    tableau = np.zeros(nbSol)
    for i in range(nbSol):
        tableau[i] = fitnessEmInitialisation(mission, inter, solution[i], distances)
    return tableau


def maxiFit(tableau):
    """
    Fonction qui renvoie la pire fitness d'un tableau et son indice
    """
    indice = 0
    maxi = tableau[0]
    for i in range(len(tableau)):
        if tableau[i] > maxi:
            maxi = tableau[i]
            indice = i
    return indice, maxi


def choixFitness_1(fit, mission, intervenants, fille, distances):
    """
    Fonction qui renvoie la fitness d'une solution dont on a explicitement demandé le type de fitness
    """
    if fit == "etudiant":
        return fEt.fitnessEtudiants_1(fille, mission, intervenants)
    elif fit == "employe":
        return fitnessEmInitialisation(mission, intervenants, fille, distances)
    elif fit == "SESSAD":
        dis1 = fEm.distance_employe(fct.activites_intervenants(fille, intervenants, mission), distances)
        return fS.fitnessSESSAD(fille, dis1, intervenants, mission, distances)
    else:
        return "erreur"


def choixFitness_tableau(fit, mission, intervenants, solutions, distances):
    """
    Fonction qui renvoie la fitness de la population dont on a explicitement demandé le type de fitness
    """
    if fit == "etudiant":
        return fEt.fitnessEtudiants_tout(solutions, mission, intervenants)
    elif fit == "employe":
        return tableau_fitnessEM(mission, intervenants, solutions, distances)
    elif fit == "SESSAD":
        return fS.fitnessSESSAD_tout(mission, intervenants, solutions, distances)
    else:
        return "erreur"


def genetique(solution, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, type_fit, colon):
    # Initialisation de la population

    solutions = cp.deepcopy(solution)
    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    tableau_fit = choixFitness_tableau(type_fit, mission, intervenants, solutions, distances)
    secu = 0
    geneCons = 0
    while nbGene < nbGeneration and secu < nbGeneration:
        print(f"Génération:\t{nbGene}/{nbGeneration}", end='\r')
        # On choisie les deux parents
        parent1, parent2 = tls.choixParents(tableau_fit)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants, s'il est valide ou non

        valideFille1 = fct.contraintes(fille1, mission, intervenants, distances)
        valideFille2 = fct.contraintes(fille2, mission, intervenants, distances)

        if valideFille1:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille1 = choixFitness_1(type_fit, mission, intervenants, fille1, distances)
            indice = tls.choixKill(tableau_fit)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille1 < max:
            if fitnessFille1 < tableau_fit[indice]:
                solutions[indice] = fille1
                tableau_fit[indice] = fitnessFille1
                geneCons += 1

        if valideFille2:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille2 = choixFitness_1(type_fit, mission, intervenants, fille2, distances)
            indice = tls.choixKill(tableau_fit)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille2 < max:
            if fitnessFille2 < tableau_fit[indice]:
                solutions[indice] = fille2
                tableau_fit[indice] = fitnessFille2
                geneCons += 1

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            # On choisit de faire une mutation
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutation = choixFitness_1(type_fit, mission, intervenants, solutions[solutionChoisie],
                                                        distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate, mission, intervenants, distances)
            if valideMutate:
                # Si la mutation est valide
                empire = rd.random()
                fitnessMutate = choixFitness_1(type_fit, mission, intervenants, mutate, distances)
                if empire > probaMissionEmpire:
                    # Si elle améliore le fitness de la solution choisie on met à jour la solution
                    if fitnessMutate < fitnessChoisiePourMutation:
                        solutions[solutionChoisie] = mutate
                        tableau_fit[solutionChoisie] = fitnessMutate
                else:
                    # Si elle n'améliore pas le fitness de la solution choisie on met à jour seulement si on a le
                    # droit d'empirer la solution
                    solutions[solutionChoisie] = mutate
                    tableau_fit[solutionChoisie] = fitnessMutate

        if valideFille1 or valideFille2:
            nbGene += 1
            secu = 0
        else:
            nbGene = nbGene
            secu += 1


        if secu > nbGeneration*0.5 and colon:
            solutions = cp.deepcopy(tls.remplacement(tableau_fit, solutions, intervenants, mission, distances))
            tableau_fit = cp.deepcopy(choixFitness_tableau(type_fit, mission, intervenants, solutions, distances))
            print("Nouvelle population, des colons arrivent")
            secu = 0


    if secu > nbGeneration-2:
        print("Nombre de générations faites :", nbGene)
        print("Arret de la recherche")

    print("Nombre de générations conservées :", geneCons)

    return solutions


def mini(tab):
    mini = tab[0]
    indice = 0
    for i in range(len(tab)):
        if tab[i] < mini:
            mini = tab[i]
            indice = i
    return indice, mini


def genetiqueCascade(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire,
                     nbTour , colon):
    """
    Algorithme génétique en cascade
    """
    sol = cp.deepcopy(solutions)
    for i in range(1, nbTour + 1):
        sol1 = genetique(sol, nbGeneration * (1 / (i + 1)), probaMutation, distances, intervenants, mission,
                         probaMissionEmpire, "employe", colon)
        sol2 = genetique(sol1, nbGeneration * (1 + i / (nbTour)) * 1.1 * (1 / i), probaMutation, distances,
                         intervenants, mission, probaMissionEmpire,
                         "etudiant", colon)
        sol = genetique(sol2, nbGeneration * (1 + i / (nbTour)) * 0.9 * (1 / i), probaMutation, distances, intervenants,
                        mission, probaMissionEmpire, "SESSAD", colon)

    return sol


def choixParentsPareto(tableau_fit1, tableau_fit2, tableau_fit3, solutions):
    """
    On execute le font de Pareto et on choisit les parents dans ce front
    """
    x, y, z, sol = pf.pareto_frontier_multi(tableau_fit1, tableau_fit2, tableau_fit3)
    if len(sol) == 1 or len(sol) == 0:
        nbSolution = len(solutions)
        indiceParent1 = rd.randint(0, nbSolution // 2)
        indiceParent2 = rd.randint(nbSolution // 2, nbSolution - 1)
    else:
        indiceParent1 = sol[rd.randint(0, len(sol) - 1)]
        sol.remove(indiceParent1)
        indiceParent2 = sol[rd.randint(0, len(sol) - 1)]
        # indiceParent1Test = sol[-1]
        # indiceParent2Test = sol[-2]
    return indiceParent1, indiceParent2


def choixParentsParetoKill(tableau_fit1, tableau_fit2, tableau_fit3, solutions):
    """
    On execute le font de Pareto et on choisit les parents dans ce front
    """
    x, y, z, sol = pf.pareto_frontier_multi_kill(tableau_fit1, tableau_fit2, tableau_fit3)
    if len(sol) == 0:
        nbSolution = len(solutions)
        indiceKill1 = rd.randint(0, nbSolution // 2)
    else:
        indiceKill1 = sol[rd.randint(0, len(sol) - 1)]
        # indiceParent1Test = sol[-1]
        # indiceParent2Test = sol[-2]
    return indiceKill1


def choixParentsParetoKill2(tableau_fit1, tableau_fit2, tableau_fit3, solutions):
    """
    On execute le font de Pareto et on choisit les parents dans ce front
    """
    x, y, z, sol = pf.pareto_frontier_multi(tableau_fit1, tableau_fit2, tableau_fit3)
    solFinale = []
    for i in range(len(solutions)):
        if i not in sol:
            solFinale.append(i)
    taille = len(solFinale)
    indice = rd.randint(0, taille - 1)
    return solFinale[indice]


def genetiquePareto(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire):
    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    tableau_fit_Et = choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)
    tableau_fit_Em = choixFitness_tableau("employe", mission, intervenants, solutions, distances)
    tableau_fit_Se = choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances)
    secu = 0
    geneCons = 0

    while nbGene < nbGeneration and secu < nbGeneration:
        print(f"Génération:\t{nbGene}/{nbGeneration}", end='\r')
        # On choisie les deux parents
        parent1, parent2 = choixParentsPareto(tableau_fit_Em, tableau_fit_Et, tableau_fit_Se, solutions)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants

        valideFille1 = fct.contraintes(fille1, mission, intervenants, distances)
        valideFille2 = fct.contraintes(fille2, mission, intervenants, distances)

        if valideFille1:
            # fitnessFille1 = fitnessEmInitialisation(mission, intervenants, fille1, distances)

            fitnessFille1_EM = choixFitness_1("employe", mission, intervenants, fille1, distances)
            fitnessFille1_Et = choixFitness_1("etudiant", mission, intervenants, fille1, distances)
            fitnessFille1_SE = choixFitness_1("SESSAD", mission, intervenants, fille1, distances)

            ran1 = rd.randint(1, 3)
            if ran1 == 1:
                indice = tls.choixKill(tableau_fit_Em)
                if fitnessFille1_EM < tableau_fit_Em[indice] and fitnessFille1_Et < tableau_fit_Et[
                    indice] and fitnessFille1_SE < tableau_fit_Se[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille1_EM
                    tableau_fit_Et[indice] = fitnessFille1_Et
                    tableau_fit_Se[indice] = fitnessFille1_SE
                    geneCons += 1
            if ran1 == 2:
                indice = tls.choixKill(tableau_fit_Et)
                if fitnessFille1_Et < tableau_fit_Et[indice] and fitnessFille1_EM < tableau_fit_Em[
                    indice] and fitnessFille1_SE < tableau_fit_Se[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille1_EM
                    tableau_fit_Et[indice] = fitnessFille1_Et
                    tableau_fit_Se[indice] = fitnessFille1_SE
                    geneCons += 1

            if ran1 == 3:
                indice = tls.choixKill(tableau_fit_Se)
                if fitnessFille1_SE < tableau_fit_Se[indice] and fitnessFille1_Et < tableau_fit_Et[
                    indice] and fitnessFille1_EM < tableau_fit_Em[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille1_EM
                    tableau_fit_Et[indice] = fitnessFille1_Et
                    tableau_fit_Se[indice] = fitnessFille1_SE
                    geneCons += 1

        if valideFille2:
            fitnessFille2_EM = choixFitness_1("employe", mission, intervenants, fille2, distances)
            fitnessFille2_Et = choixFitness_1("etudiant", mission, intervenants, fille2, distances)
            fitnessFille2_SE = choixFitness_1("SESSAD", mission, intervenants, fille2, distances)

            ran2 = rd.randint(1, 3)
            if ran2 == 1:
                indice = tls.choixKill(tableau_fit_Em)
                if fitnessFille2_EM < tableau_fit_Em[indice] and fitnessFille2_Et < tableau_fit_Et[
                    indice] and fitnessFille2_SE < tableau_fit_Se[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille2_EM
                    tableau_fit_Et[indice] = fitnessFille2_Et
                    tableau_fit_Se[indice] = fitnessFille2_SE
                    geneCons += 1
            if ran2 == 2:
                indice = tls.choixKill(tableau_fit_Et)
                if fitnessFille2_Et < tableau_fit_Et[indice] and fitnessFille2_EM < tableau_fit_Em[
                    indice] and fitnessFille2_SE < tableau_fit_Se[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille2_EM
                    tableau_fit_Et[indice] = fitnessFille2_Et
                    tableau_fit_Se[indice] = fitnessFille2_SE
                    geneCons += 1

            if ran2 == 3:
                indice = tls.choixKill(tableau_fit_Se)
                if fitnessFille2_SE < tableau_fit_Se[indice] and fitnessFille2_EM < tableau_fit_Em[
                    indice] and fitnessFille2_Et < tableau_fit_Et[indice]:
                    solutions[indice] = fille1
                    tableau_fit_Em[indice] = fitnessFille2_EM
                    tableau_fit_Et[indice] = fitnessFille2_Et
                    tableau_fit_Se[indice] = fitnessFille2_SE
                    geneCons += 1

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutation_EM = choixFitness_1("employe", mission, intervenants, solutions[solutionChoisie],
                                                           distances)
            fitnessChoisiePourMutation_Et = choixFitness_1("etudiant", mission, intervenants,
                                                           solutions[solutionChoisie], distances)
            fitnessChoisiePourMutation_SE = choixFitness_1("SESSAD", mission, intervenants, solutions[solutionChoisie],
                                                           distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate, mission, intervenants, distances)
            # Le mutant fonctionne comme dans n'importe quel algo génétique
            if valideMutate:
                empire = rd.random()
                fitnessMutate_Em = choixFitness_1("employe", mission, intervenants, mutate, distances)
                fitnessMutate_ET = choixFitness_1("etudiant", mission, intervenants, mutate, distances)
                fitnessMutate_SE = choixFitness_1("SESSAD", mission, intervenants, mutate, distances)
                if empire > probaMissionEmpire:
                    if fitnessMutate_Em < fitnessChoisiePourMutation_EM and fitnessMutate_ET < fitnessChoisiePourMutation_Et and fitnessMutate_SE < fitnessChoisiePourMutation_SE:
                        solutions[solutionChoisie] = mutate
                        tableau_fit_Em[solutionChoisie] = fitnessMutate_Em
                        tableau_fit_Et[solutionChoisie] = fitnessMutate_ET
                        tableau_fit_Se[solutionChoisie] = fitnessMutate_SE
                else:
                    solutions[solutionChoisie] = mutate
                    tableau_fit_Em[solutionChoisie] = fitnessMutate_Em
                    tableau_fit_Et[solutionChoisie] = fitnessMutate_ET
                    tableau_fit_Se[solutionChoisie] = fitnessMutate_SE

        if valideFille1 or valideFille2:
            nbGene += 1
            secu = 0
        else:
            nbGene = nbGene
            secu += 1
    if secu > nbGeneration-2:
        print("Nombre de générations faites :", nbGene)
        print("Arret de la recherche")

    print("Nombre de générations conservées :", geneCons)

    return solutions


def genetiqueMoyenneNorma(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, colon):
    # Initialisation de la population

    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    secu = 0
    geneCons = 0
    fitnessEm = choixFitness_tableau("employe", mission, intervenants, solutions, distances)
    fitnessSe =choixFitness_tableau("SESSAD",mission,intervenants,solutions,distances)
    fitnessEt = choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)

    while nbGene < nbGeneration and secu < nbGeneration*0.7:
        print(f"Génération:\t{nbGene}/{nbGeneration}", end='\r')
        # On choisie les deux parents
        normalise = tls.moyenneFitness_Norma(fitnessEm, fitnessEt, fitnessSe)
        parent1, parent2 = tls.choixParents(normalise)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants, s'il est valide ou non

        valideFille1 = fct.contraintes(fille1, mission, intervenants, distances)
        valideFille2 = fct.contraintes(fille2, mission, intervenants, distances)

        if valideFille1:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille1Em = choixFitness_1("employe", mission, intervenants, fille1, distances)
            fitnessFille1Et = choixFitness_1("etudiant", mission, intervenants, fille1, distances)
            fitnessFille1Se = choixFitness_1("SESSAD", mission, intervenants, fille1, distances)
            auxEm = np.append(fitnessEm, fitnessFille1Em)
            auxEt = np.append(fitnessEt, fitnessFille1Et)
            auxSe = np.append(fitnessSe, fitnessFille1Se)
            aux_norma = tls.moyenneFitness_Norma(auxEm, auxEt, auxSe)
            fitnessFille1_norma = aux_norma[-1]
            aux_norma_sans = np.delete(aux_norma, -1)
            indice = tls.choixKill(aux_norma_sans)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille1 < max:
            if fitnessFille1_norma < aux_norma_sans[indice]:
                solutions[indice] = fille1
                fitnessEm[indice] = fitnessFille1Em
                fitnessEt[indice] = fitnessFille1Et
                fitnessSe[indice] = fitnessFille1Se
                geneCons += 1

        if valideFille2:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille2Em = choixFitness_1("employe", mission, intervenants, fille2, distances)
            fitnessFille2Et = choixFitness_1("etudiant", mission, intervenants, fille2, distances)
            fitnessFille2Se = choixFitness_1("SESSAD", mission, intervenants, fille2, distances)
            auxEm = np.append(fitnessEm, fitnessFille2Em)
            auxEt = np.append(fitnessEt, fitnessFille2Et)
            auxSe = np.append(fitnessSe, fitnessFille2Se)
            aux_norma = tls.moyenneFitness_Norma(auxEm, auxEt, auxSe)
            fitnessFille2_norma = aux_norma[-1]
            aux_norma_sans = np.delete(aux_norma, -1)
            indice = tls.choixKill(aux_norma_sans)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille2 < max:
            if fitnessFille2_norma < aux_norma_sans[indice]:
                solutions[indice] = fille2
                fitnessEm[indice] = fitnessFille2Em
                fitnessEt[indice] = fitnessFille2Et
                fitnessSe[indice] = fitnessFille2Se
                geneCons += 1

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            # On choisit de faire une mutation
            solutionChoisie = rd.randint(0, nbPlanning - 1)

            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate, mission, intervenants, distances)

            if valideMutate:

                fitnessMutaEm = choixFitness_1("employe", mission, intervenants, fille2, distances)
                fitnessMutaEt = choixFitness_1("etudiant", mission, intervenants, fille2, distances)
                fitnessMutaSe = choixFitness_1("SESSAD", mission, intervenants, fille2, distances)
                auxEmMuta = np.append(fitnessEm, fitnessMutaEm)
                auxEtMuta = np.append(fitnessEt, fitnessMutaEt)
                auxSeMuta = np.append(fitnessSe, fitnessMutaSe)
                aux_normaMuta = tls.moyenneFitness_Norma(auxEmMuta, auxEtMuta, auxSeMuta)
                fitnessMutation_norma = aux_normaMuta[-1]
                aux_norma_sans = np.delete(aux_normaMuta, -1)
                fitnessChoisiePourMutationNorma = aux_norma_sans[solutionChoisie]

                # Si la mutation est valide
                empire = rd.random()

                if empire > probaMissionEmpire:
                    # Si elle améliore le fitness de la solution choisie on met à jour la solution
                    if fitnessMutation_norma < fitnessChoisiePourMutationNorma:
                        solutions[solutionChoisie] = mutate
                        fitnessEm[solutionChoisie] = fitnessMutaEm
                        fitnessEt[solutionChoisie] = fitnessMutaEt
                        fitnessSe[solutionChoisie] = fitnessMutaSe
                else:
                    # Si elle n'améliore pas le fitness de la solution choisie on met à jour seulement si on a le droit d'empirer la solution
                    solutions[solutionChoisie] = mutate
                    fitnessEm[solutionChoisie] = fitnessMutaEm
                    fitnessEt[solutionChoisie] = fitnessMutaEt
                    fitnessSe[solutionChoisie] = fitnessMutaSe

        if secu > nbGeneration*0.5 and colon:
            solutions = cp.deepcopy(tls.remplacement(normalise, solutions, intervenants, mission, distances))
            fitnessEm = choixFitness_tableau("employe", mission, intervenants, solutions, distances)
            fitnessSe = choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances)
            fitnessEt = choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)
            print("Nouvelle population, des colons arrivent")
            secu = 0

        if valideFille1 or valideFille2:
            nbGene += 1
            secu = 0
        else:
            nbGene = nbGene
            secu += 1

    if secu > nbGeneration-2:

        print("Nombre de générations faites :", nbGene)
        print("Arret de la recherche")

    print("Nombre de générations conservées :", geneCons)

    return solutions


def genetiqueMoyenne(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, colon):
    # Initialisation de la population

    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    tableau_fit_moy = tls.moyenneFitness(choixFitness_tableau("employe", mission, intervenants, solutions, distances), choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances), choixFitness_tableau("etudiant", mission, intervenants, solutions, distances))
    secu = 0
    geneCons = 0
    while nbGene < nbGeneration and secu < nbGeneration:
        print(f"Génération:\t{nbGene}/{nbGeneration}", end='\r')
        # On choisie les deux parents
        parent1, parent2 = tls.choixParents(tableau_fit_moy)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants, s'il est valide ou non

        valideFille1 = fct.contraintes(fille1, mission, intervenants, distances)
        valideFille2 = fct.contraintes(fille2, mission, intervenants, distances)

        if valideFille1:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille1 = tls.moyenneFit_1(mission, intervenants, fille1,distances)
            indice = tls.choixKill(tableau_fit_moy)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille1 < max:
            if fitnessFille1 < tableau_fit_moy[indice]:
                solutions[indice] = fille1
                tableau_fit_moy[indice] = fitnessFille1
                geneCons += 1

        if valideFille2:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille2 = tls.moyenneFit_1(mission, intervenants, fille2,distances)
            indice = tls.choixKill(tableau_fit_moy)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille2 < max:
            if fitnessFille2 < tableau_fit_moy[indice]:
                solutions[indice] = fille2
                tableau_fit_moy[indice] = fitnessFille2
                geneCons += 1

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            # On choisit de faire une mutation
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutation = tls.moyenneFit_1(mission, intervenants, solutions[solutionChoisie], distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate, mission, intervenants, distances)
            if valideMutate:
                # Si la mutation est valide
                empire = rd.random()
                fitnessMutate = tls.moyenneFit_1(mission, intervenants, mutate, distances)
                if empire > probaMissionEmpire:
                    # Si elle améliore le fitness de la solution choisie on met à jour la solution
                    if fitnessMutate < fitnessChoisiePourMutation:
                        solutions[solutionChoisie] = mutate
                        tableau_fit_moy[solutionChoisie] = fitnessMutate
                else:
                    # Si elle n'améliore pas le fitness de la solution choisie on met à jour seulement si on a le
                    # droit d'empirer la solution
                    solutions[solutionChoisie] = mutate
                    tableau_fit_moy[solutionChoisie] = fitnessMutate

        if secu > nbGeneration*0.5 and colon:
            solutions = cp.deepcopy(tls.remplacement(tableau_fit_moy, solutions, intervenants, mission, distances))
            tableau_fit_moy = cp.deepcopy(tls.moyenneFitness(choixFitness_tableau("employe", mission, intervenants, solutions, distances), choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances), choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)))
            print("Nouvelle population, des colons arrivent")
            secu = 0

        if valideFille1 or valideFille2:
            nbGene += 1
            secu = 0
        else:
            nbGene = nbGene
            secu += 1

    if secu > nbGeneration-2:
        print("Nombre de générations faites :", nbGene)
        print("Arret de la recherche")

    print("Nombre de générations conservées :", geneCons)

    return solutions



def genetiqueCascade_fit(solution, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, colon):
    # Initialisation de la population

    solutions = cp.deepcopy(solution)
    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)

    tableau_fitEm = choixFitness_tableau("employe", mission, intervenants, solutions, distances)
    tableau_fitSess = choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances)
    tableau_fitEtu = choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)

    secu = 0
    geneCons = 0
    while nbGene < nbGeneration and secu < nbGeneration:
        print(f"Génération:\t{nbGene}/{nbGeneration}", end='\r')
        # On choisie les deux parents
        parent1, parent2 = tls.choixParents(tableau_fitEm)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants, s'il est valide ou non

        valideFille1 = fct.contraintes(fille1, mission, intervenants, distances)
        valideFille2 = fct.contraintes(fille2, mission, intervenants, distances)

        if valideFille1:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille1Em = choixFitness_1("employe", mission, intervenants, fille1, distances)
            fitnessFille1Sess = choixFitness_1("SESSAD", mission, intervenants, fille1, distances)
            fitnessFille1Etu = choixFitness_1("etudiant", mission, intervenants, fille1, distances)
            indice = tls.choixKill(tableau_fitEm)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille1 < max:
            if fitnessFille1Em < tableau_fitEm[indice] and fitnessFille1Sess < tableau_fitSess[indice] and fitnessFille1Etu < tableau_fitEtu[indice]:
                solutions[indice] = fille1
                tableau_fitEm[indice] = fitnessFille1Em
                tableau_fitSess[indice] = fitnessFille1Sess
                tableau_fitEtu[indice] = fitnessFille1Etu
                geneCons += 1

        if valideFille2:
            # Si l'enfant est valide on remplace le pire de la population par l'enfant
            fitnessFille2Em = choixFitness_1("employe", mission, intervenants, fille2, distances)
            fitnessFille2Sess = choixFitness_1("SESSAD", mission, intervenants, fille2, distances)
            fitnessFille2Etu = choixFitness_1("etudiant", mission, intervenants, fille2, distances)
            indice = tls.choixKill(tableau_fitEm)
            # indice, max = maxiFit(tableau_fit)
            # if fitnessFille2 < max:
            if fitnessFille2Em < tableau_fitEm[indice] and fitnessFille2Sess < tableau_fitSess[indice] and fitnessFille2Etu < tableau_fitEtu[indice]:
                solutions[indice] = fille2
                tableau_fitEm[indice] = fitnessFille2Em
                tableau_fitSess[indice] = fitnessFille2Sess
                tableau_fitEtu[indice] = fitnessFille2Etu
                geneCons += 1

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            # On choisit de faire une mutation
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutationEm = choixFitness_1("employe", mission, intervenants, solutions[solutionChoisie],
                                                        distances)
            fitnessChoisiePourMutationSess = choixFitness_1("SESSAD", mission, intervenants, solutions[solutionChoisie],
                                                            distances)
            fitnessChoisiePourMutationEtu = choixFitness_1("etudiant", mission, intervenants, solutions[solutionChoisie],
                                                              distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate, mission, intervenants, distances)
            if valideMutate:
                # Si la mutation est valide
                empire = rd.random()
                fitnessMutateEm = choixFitness_1("employe", mission, intervenants, mutate, distances)
                fitnessMutateSess = choixFitness_1("SESSAD", mission, intervenants, mutate, distances)
                fitnessMutateEtu = choixFitness_1("etudiant", mission, intervenants, mutate, distances)
                if empire > probaMissionEmpire:
                    # Si elle améliore le fitness de la solution choisie on met à jour la solution
                    if fitnessMutateEm < fitnessChoisiePourMutationEm and fitnessMutateSess < fitnessChoisiePourMutationSess and fitnessMutateEtu < fitnessChoisiePourMutationEtu:
                        solutions[solutionChoisie] = mutate
                        tableau_fitEm[solutionChoisie] = fitnessMutateEm
                        tableau_fitSess[solutionChoisie] = fitnessMutateSess
                        tableau_fitEtu[solutionChoisie] = fitnessMutateEtu
                else:
                    # Si elle n'améliore pas le fitness de la solution choisie on met à jour seulement si on a le
                    # droit d'empirer la solution
                    solutions[solutionChoisie] = mutate
                    tableau_fitEm[solutionChoisie] = fitnessMutateEm
                    tableau_fitSess[solutionChoisie] = fitnessMutateSess
                    tableau_fitEtu[solutionChoisie] = fitnessMutateEtu

        if valideFille1 or valideFille2:
            nbGene += 1
            secu = 0
        else:
            nbGene = nbGene
            secu += 1


        if secu > nbGeneration*0.5 and colon:
            solutions = cp.deepcopy(tls.remplacement(tableau_fitEm, solutions, intervenants, mission, distances))
            tableau_fitEm = cp.deepcopy(choixFitness_tableau("employe", mission, intervenants, solutions, distances))
            tableau_fitSess = cp.deepcopy(choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances))
            tableau_fitEtu = cp.deepcopy(choixFitness_tableau("etudiant", mission, intervenants, solutions, distances))
            print("Nouvelle population, des colons arrivent")
            secu = 0


    if secu > nbGeneration-2:
        print("Nombre de générations faites :", nbGene)
        print("Arret de la recherche")

    print("Nombre de générations conservées :", geneCons)

    return solutions




def main():
    matrice_distance, intervenants, missions = fct.charge_fichier_csv("45-4")
    soll = pop.gen_n_solutions_uniques(100, intervenants, missions, matrice_distance)
    #pop.fichier_sol(50, matrice_distance, intervenants, missions)
    #soll = fct.charger_solution("solutions.txt")
    print("emplo avant")
    print(min(tableau_fitnessEM(missions, intervenants, soll, matrice_distance)))
    print("SESSAD avant")
    print(min(fS.fitnessSESSAD_tout(missions, intervenants, soll, matrice_distance)))
    print("etudiant avant")
    print(min(fEt.fitnessEtudiants_tout(soll, missions, intervenants)))
    debut = ti.time()
    apres = genetiqueCascade_fit(soll, 10000, 0.2, matrice_distance, intervenants, missions, 0.0, False)
    fin = ti.time()
    print("emplo apres")
    print(min(tableau_fitnessEM(missions, intervenants, apres, matrice_distance)))
    print("SESSAD apres")
    print(min(fS.fitnessSESSAD_tout(missions, intervenants, apres, matrice_distance)))
    print("etudiant apres")
    print(min(fEt.fitnessEtudiants_tout(apres, missions, intervenants)))
    print("temps")
    print(fin - debut)

    # indi, petit = mini(tableau_fitnessEM(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE))

    # print(fEm.activites_intervenants(apres[indi]))


if __name__ == "__main__":
    main()