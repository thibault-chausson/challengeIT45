import json as js
import statistics as st
import numpy as np
import random as rd

import fitnessEmployes as fEm
import fitnessEtudiants as fEt
import fitnessSESSAD as fS

import tools as tls
import functions as fct

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





def genetique_employes(solutions, nbGeneration, probaMutation, distances, intervenants, mission, probaMissionEmpire, type_fit):
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
                if empire > probaMissionEmpire:
                    fitnessMutate = choixFitness_1(type_fit, mission, intervenants, mutate, distances)
                    if fitnessMutate < fitnessChoisiePourMutation:
                        solutions[solutionChoisie] = mutate
                        tableau_fit[solutionChoisie] = fitnessMutate
                else:
                    solutions[solutionChoisie] = mutate

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


def main():
    charge_fichier_csv("45-4")
    SOLUTIONS = charger_solution("TRUE_res.txt")
    print(min(tableau_fitnessEM(MISSIONS, INTERVENANTS, SOLUTIONS, MATRICE_DISTANCE)))
    apres = genetique_employes(SOLUTIONS, 1000, 0.05, MATRICE_DISTANCE, INTERVENANTS, MISSIONS, 0.01, "SESSAD")
    print(min(tableau_fitnessEM(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE)))

    indi, petit = mini(tableau_fitnessEM(MISSIONS, INTERVENANTS, apres, MATRICE_DISTANCE))

    print(fEm.activites_intervenants(apres[indi]))


if __name__ == "__main__":
    main()
