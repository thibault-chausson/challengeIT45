import json as js
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


def fitnessEmInitialisation(mission, inter, solution_1, distances):
    nbTrav, nbNon, nbSup = fEm.stats_heures(solution_1)
    solution_1_planning = fEm.activites_intervenants(solution_1)
    nbDis = fEm.distance_employe(solution_1_planning)
    fitnessEmplo_1_sol = fEm.fitnessEm(st.pstdev(nbNon), st.pstdev(nbSup), st.pstdev(nbDis))
    return fitnessEmplo_1_sol


def tableau_fitnessEM(mission, inter, solution, distances):
    nbSol = len(solution)
    tableau = np.zeros(nbSol)
    for i in range(nbSol):
        tableau[i] = fitnessEmInitialisation(mission, inter, solution[i], distances)
    return tableau


def maxiFit(tableau):
    indice = 0
    maxi = tableau[0]
    for i in range(len(tableau)):
        if tableau[i] > maxi:
            maxi = tableau[i]
            indice = i
    return indice, maxi


def choixFitness_1 (fit, mission, intervenants, fille, distances):
    if fit=="etudiant":
        return fEt.fitnessEtudiants_1(fille, mission, intervenants)
    elif fit=="employe":
        return fitnessEmInitialisation(mission, intervenants, fille, distances)
    elif fit=="SESSAD":
        dis1 = fEm.distance_employe(fS.activites_intervenants(fille))
        return fS.fitnessSESSAD(mission, intervenants, fille, dis1)
    else:
        return "erreur"


def choixFitness_tableau (fit, mission, intervenants, solutions, distances):
    if fit=="etudiant":
        return fEt.fitnessEtudiants_tout(solutions, mission,intervenants)
    elif fit=="employe":
        return tableau_fitnessEM(mission, intervenants, solutions, distances)
    elif fit=="SESSAD":
        return fS.fitnessSESSAD_tout(mission, intervenants, solutions, distances)
    else:
        return "erreur"





def genetique(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, type_fit):
    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    tableau_fit = choixFitness_tableau(type_fit, mission, intervenants, solutions, distances)
    while nbGene < nbGeneration:
        # On choisie les deux parents
        parent1, parent2 = tls.choixParents(tableau_fit)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants

        valideFille1 = fct.contraintes(fille1)
        valideFille2 = fct.contraintes(fille2)

        if valideFille1:
            #fitnessFille1 = fitnessEmInitialisation(mission, intervenants, fille1, distances)
            fitnessFille1 = choixFitness_1(type_fit, mission, intervenants, fille1, distances)
            indice, max = maxiFit(tableau_fit)
            if fitnessFille1 < max:
                solutions[indice] = fille1
                tableau_fit[indice] = fitnessFille1

        if valideFille2:
            fitnessFille2 = choixFitness_1(type_fit, mission, intervenants, fille2, distances)
            indice, max = maxiFit(tableau_fit)
            if fitnessFille2 < max:
                solutions[indice] = fille2
                tableau_fit[indice] = fitnessFille2

        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutation = choixFitness_1(type_fit, mission, intervenants, solutions[solutionChoisie], distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate)
            if valideMutate:
                empire = rd.random()
                fitnessMutate = choixFitness_1(type_fit, mission, intervenants, mutate, distances)
                if empire > probaMissionEmpire:
                    if fitnessMutate < fitnessChoisiePourMutation:
                        solutions[solutionChoisie] = mutate
                        tableau_fit[solutionChoisie] = fitnessMutate
                else:
                    solutions[solutionChoisie] = mutate
                    tableau_fit[solutionChoisie] = fitnessMutate

        if valideFille1 or valideFille2:
            nbGene += 1
        else:
            nbGene = nbGene

    return solutions


def mini(tab):
    mini = tab[0]
    indice = 0
    for i in range(len(tab)):
        if tab[i] < mini:
            mini = tab[i]
            indice = i
    return indice, mini


def genetiqueCascade(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire):
    sol=cp.deepcopy(solutions)
    sol1=genetique(sol, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, "employe")
    sol2=genetique(sol1, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, "etudiant")
    print(min(fS.fitnessSESSAD_tout(MISSIONS, INTERVENANTS, sol2, MATRICE_DISTANCE)))
    sol3=genetique(sol2, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, "SESSAD")
    return sol3


def choixParentsPareto(tableau_fit1, tableau_fit2, tableau_fit3, solutions):
    x, y, z, sol = pf.pareto_frontier(tableau_fit1, tableau_fit2, tableau_fit3, minX = False, minY = True, minZ = True)
    if len(sol)==1 or len(sol)==0:
        nbSolution = len(solutions)
        indiceParent1 = rd.randint(0, nbSolution//2)
        indiceParent2 = rd.randint(nbSolution//2, nbSolution-1)
    else:
        indiceParent1 = sol[rd.randint(0, len(sol) - 1)]
        sol.remove(indiceParent1)
        indiceParent2 = sol[rd.randint(0, len(sol) - 1)]
        #indiceParent1Test = sol[-1]
        #indiceParent2Test = sol[-2]
    return indiceParent1, indiceParent2


def genetiquePareto(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire):
    nbGene = 0
    nbPlanning = len(solutions)
    nbInter = len(intervenants)
    nbMis = len(mission)
    tableau_fit_Et = choixFitness_tableau("etudiant", mission, intervenants, solutions, distances)
    tableau_fit_Em = choixFitness_tableau("employe", mission, intervenants, solutions, distances)
    tableau_fit_Se = choixFitness_tableau("SESSAD", mission, intervenants, solutions, distances)
    while nbGene < nbGeneration:
        # On choisie les deux parents
        parent1, parent2 = choixParentsPareto(tableau_fit_Et, tableau_fit_Se, tableau_fit_Em, solutions)
        # On crée un enfant
        finCol = rd.randint(1, nbMis - 1)
        fille1 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, 0, finCol - 1)
        fille2 = tls.reproduction(solutions[parent1], solutions[parent2], 0, nbInter - 1, finCol, nbMis - 1)
        # On choisie ce que l'on va faire avec les enfants

        valideFille1 = fct.contraintes(fille1)
        valideFille2 = fct.contraintes(fille2)

        if valideFille1:
            #fitnessFille1 = fitnessEmInitialisation(mission, intervenants, fille1, distances)
            fitnessFille1_EM = choixFitness_1("employe", mission, intervenants, fille1, distances)
            fitnessFille1_Et = choixFitness_1("etudiant", mission, intervenants, fille1, distances)
            fitnessFille1_SE = choixFitness_1("SESSAD", mission, intervenants, fille1, distances)
            indice_Em, max_Em = maxiFit(tableau_fit_Em)
            indice_Et, max_Et = maxiFit(tableau_fit_Et)
            indice_SE, max_SE = maxiFit(tableau_fit_Se)
            if fitnessFille1_EM < max_Em or fitnessFille1_Et < max_Et or fitnessFille1_SE < max_SE:
                ran1=rd.randint(1,3)
                if ran1==1:
                    solutions[indice_Em] = fille1
                    tableau_fit_Em[indice_Em] = fitnessFille1_EM
                    tableau_fit_Et[indice_Em] = fitnessFille1_Et
                    tableau_fit_Se[indice_Em] = fitnessFille1_SE
                if ran1==2:
                    solutions[indice_Et] = fille1
                    tableau_fit_Em[indice_Et] = fitnessFille1_EM
                    tableau_fit_Et[indice_Et] = fitnessFille1_Et
                    tableau_fit_Se[indice_Et] = fitnessFille1_SE
                if ran1==3:
                    solutions[indice_SE] = fille1
                    tableau_fit_Em[indice_SE] = fitnessFille1_EM
                    tableau_fit_Et[indice_SE] = fitnessFille1_Et
                    tableau_fit_Se[indice_SE] = fitnessFille1_SE



        if valideFille2:
            fitnessFille2_EM = choixFitness_1("employe", mission, intervenants, fille2, distances)
            fitnessFille2_Et = choixFitness_1("etudiant", mission, intervenants, fille2, distances)
            fitnessFille2_SE = choixFitness_1("SESSAD", mission, intervenants, fille2, distances)
            indice2_Em, max2_Em = maxiFit(tableau_fit_Em)
            indice2_Et, max2_Et = maxiFit(tableau_fit_Et)
            indice2_SE, max2_SE = maxiFit(tableau_fit_Se)
            if fitnessFille2_EM < max2_Em and fitnessFille2_Et < max2_Et and fitnessFille2_SE < max2_SE:
                ran=rd.randint(1,3)
                if ran==1:
                    solutions[indice2_Em] = fille2
                    tableau_fit_Em[indice2_Em] = fitnessFille2_EM
                    tableau_fit_Et[indice2_Em] = fitnessFille2_Et
                    tableau_fit_Se[indice2_Em] = fitnessFille2_SE
                if ran==2:
                    solutions[indice2_Et] = fille2
                    tableau_fit_Em[indice2_Et] = fitnessFille2_EM
                    tableau_fit_Et[indice2_Et] = fitnessFille2_Et
                    tableau_fit_Se[indice2_Et] = fitnessFille2_SE
                if ran==3:
                    solutions[indice2_SE] = fille2
                    tableau_fit_Em[indice2_SE] = fitnessFille2_EM
                    tableau_fit_Et[indice2_SE] = fitnessFille2_Et
                    tableau_fit_Se[indice2_SE] = fitnessFille2_SE



        ## On fait une mutation
        # On choisit une solution

        if rd.random() < probaMutation:
            solutionChoisie = rd.randint(0, nbPlanning - 1)
            fitnessChoisiePourMutation_EM = choixFitness_1("employe", mission, intervenants, solutions[solutionChoisie], distances)
            fitnessChoisiePourMutation_Et = choixFitness_1("etudiant", mission, intervenants, solutions[solutionChoisie], distances)
            fitnessChoisiePourMutation_SE = choixFitness_1("SESSAD", mission, intervenants, solutions[solutionChoisie], distances)
            mutate = tls.mutation(solutions[solutionChoisie])
            valideMutate = fct.contraintes(mutate)
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
        else:
            nbGene = nbGene


    return solutions



def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print("emplo avant")
    print(min(tableau_fitnessEM(MISSIONS, INTERVENANTS, SOLUTIONS, MATRICE_DISTANCE)))
    print("SESSAD avant")
    print(min(fS.fitnessSESSAD_tout(MISSIONS, INTERVENANTS, SOLUTIONS, MATRICE_DISTANCE)))
    print("etudiant avant")
    print(min(fEt.fitnessEtudiants_tout(SOLUTIONS, MISSIONS, INTERVENANTS)))
    apres = genetiquePareto(SOLUTIONS, 1000, 0.1, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, 0.0)
    print("emplo apres")
    print(min(tableau_fitnessEM(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE)))
    print("SESSAD apres")
    print(min(fS.fitnessSESSAD_tout(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE)))
    print("etudiant apres")
    print(min(fEt.fitnessEtudiants_tout(apres, MISSIONS, INTERVENANTS)))

    #indi, petit = mini(tableau_fitnessEM(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE))

    #print(fEm.activites_intervenants(apres[indi]))




if __name__ == "__main__":
    main()
